"""
FastMCP-based Knowledge + Action Bot Server
Supports industry-specific health endpoints and hot-swappable configs
"""

import json
import yaml
import logging
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import re

from fastmcp import FastMCP
from starlette.responses import JSONResponse, PlainTextResponse
import httpx

# Load environment variables from .env file manually
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchType:
    TEXT = "text"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"


@dataclass
class IntentDefinition:
    name: str
    description: str
    keywords: List[str]
    fallback: bool = False
    escalate_to_human: bool = False


@dataclass
class ActionConnector:
    name: str
    type: str
    endpoint: Optional[str] = None
    method: str = "POST"
    headers: Optional[Dict[str, str]] = None
    mock_response: Optional[Dict] = None
    description: str = ""


class KnowledgeBase:
    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents
        self.index = {}
        self._build_index()

    def _build_index(self):
        for doc_id, doc in enumerate(self.documents):
            tokens = self._tokenize(doc.get("content", ""))
            for token in tokens:
                if token not in self.index:
                    self.index[token] = []
                self.index[token].append(doc_id)

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def text_search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_tokens = self._tokenize(query)
        scores = {}
        for token in query_tokens:
            if token in self.index:
                for doc_id in self.index[token]:
                    scores[doc_id] = scores.get(doc_id, 0) + 1
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [self.documents[doc_id] for doc_id, _ in sorted_docs]

    def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict]:
        return self.text_search(query, top_k)


class IntentDetector:
    def __init__(self, intents: List[Dict[str, Any]]):
        self.intents = [IntentDefinition(**intent) for intent in intents]

    def detect(self, query: str) -> Optional[IntentDefinition]:
        query_lower = query.lower()
        for intent in self.intents:
            for keyword in intent.keywords:
                if keyword.lower() in query_lower:
                    return intent
        for intent in self.intents:
            if intent.fallback:
                return intent
        return None


class QABotConfig:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_knowledge_corpus(self) -> List[Dict[str, Any]]:
        corpus_path = self.config["knowledge"]["corpus_path"]
        if not Path(corpus_path).is_absolute():
            kb_path = self.config_path.parent / corpus_path
        else:
            kb_path = Path(corpus_path)
        kb_path = kb_path.resolve()
        
        with open(kb_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @property
    def industry(self) -> str:
        return self.config["industry"]

    @property
    def persona(self) -> Dict[str, str]:
        return self.config["bot_persona"]

    @property
    def search_type(self) -> str:
        return self.config["knowledge"].get("search_type", "hybrid")


class IndustryBotManager:
    """Manages multiple industry-specific bots"""
    def __init__(self, configs_dir: str = "configs"):
        self.configs_dir = Path(configs_dir)
        self.bots: Dict[str, Dict] = {}
        self._load_all_industries()

    def _load_all_industries(self):
        """Load all industry configs on startup"""
        industries = ["banking", "healthcare", "saas", "government", "telecom"]
        for industry in industries:
            config_path = self.configs_dir / f"{industry}.yaml"
            if config_path.exists():
                try:
                    config = QABotConfig(str(config_path))
                    kb = KnowledgeBase(config.get_knowledge_corpus())
                    intent_detector = IntentDetector(config.config["intents"])
                    
                    self.bots[industry] = {
                        "config": config,
                        "knowledge_base": kb,
                        "intent_detector": intent_detector,
                        "actions": config.config["actions"]
                    }
                    logger.info(f"✅ Loaded {industry} industry bot")
                except Exception as e:
                    logger.error(f"❌ Failed to load {industry}: {e}")

    def get_bot(self, industry: str) -> Optional[Dict]:
        return self.bots.get(industry)

    def get_industries(self) -> List[str]:
        return list(self.bots.keys())


# Initialize FastMCP server
mcp = FastMCP("qa-bot")
bot_manager = IndustryBotManager()

# Health check endpoints for each industry
@mcp.custom_route("/health", methods=["GET"])
async def health_check_root(request):
    """Root health check"""
    return PlainTextResponse("OK - MCP Q&A Bot Running")

@mcp.custom_route("/health/{industry}", methods=["GET"])
async def health_check_industry(request):
    """Industry-specific health check"""
    industry = request.path_params.get("industry")
    bot = bot_manager.get_bot(industry)
    
    if not bot:
        return JSONResponse(
            {"status": "error", "message": f"Industry '{industry}' not found"},
            status_code=404
        )
    
    return JSONResponse({
        "status": "ok",
        "industry": industry,
        "persona": bot["config"].persona.get("tone", "default"),
        "documents": len(bot["knowledge_base"].documents),
        "intents": len(bot["intent_detector"].intents),
        "actions": len(bot["actions"])
    })

@mcp.custom_route("/industries", methods=["GET"])
async def list_industries(request):
    """List all available industries"""
    return JSONResponse({
        "industries": bot_manager.get_industries()
    })


# HTTP helper routes (compat with OpenAI client)
@mcp.custom_route("/search", methods=["POST"])
async def http_search(request):
    payload = await request.json()
    industry = payload.get("industry")
    query = payload.get("query", "")
    top_k = int(payload.get("top_k", 5))
    # Inline the search logic to avoid calling the FunctionTool wrapper
    bot = bot_manager.get_bot(industry)
    if not bot:
        return JSONResponse({"error": f"Industry '{industry}' not found"}, status_code=404)
    results = bot["knowledge_base"].hybrid_search(query, top_k)
    result = {
        "industry": industry,
        "query": query,
        "search_type": bot["config"].search_type,
        "results": results
    }
    return JSONResponse(result, status_code=200)


@mcp.custom_route("/detect_intent", methods=["POST"])
async def http_detect_intent(request):
    payload = await request.json()
    industry = payload.get("industry")
    query = payload.get("query", "")
    bot = bot_manager.get_bot(industry)
    if not bot:
        return JSONResponse({"error": f"Industry '{industry}' not found"}, status_code=404)
    intent = bot["intent_detector"].detect(query)
    result = {
        "industry": industry,
        "query": query,
        "detected_intent": asdict(intent) if intent else None,
        "requires_escalation": intent.escalate_to_human if intent else False
    }
    return JSONResponse(result, status_code=200)


@mcp.custom_route("/escalate", methods=["POST"])
async def http_escalate(request):
    payload = await request.json()
    reason = payload.get("reason", "")
    ticket_id = f"TKT-{abs(hash(reason)) % 100000:05d}"
    return JSONResponse({"status": "created", "ticket_id": ticket_id, "reason": reason})


# MCP Tool: Search Knowledge Base
@mcp.tool()
async def search_knowledge(industry: str, query: str, top_k: int = 5) -> dict:
    """
    Search the knowledge base for a specific industry.
    
    Args:
        industry: Industry name (banking, healthcare, saas, government, telecom)
        query: Search query string
        top_k: Number of results to return (default: 5)
        
    Returns:
        Search results with matching documents
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return {"error": f"Industry '{industry}' not found"}
    
    results = bot["knowledge_base"].hybrid_search(query, top_k)
    
    return {
        "industry": industry,
        "query": query,
        "search_type": bot["config"].search_type,
        "results": results
    }


# MCP Tool: Detect Intent
@mcp.tool()
async def detect_intent(industry: str, query: str) -> dict:
    """
    Detect user intent from query for a specific industry.
    
    Args:
        industry: Industry name (banking, healthcare, saas, government, telecom)
        query: User query string
        
    Returns:
        Detected intent and escalation requirements
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return {"error": f"Industry '{industry}' not found"}
    
    intent = bot["intent_detector"].detect(query)
    
    return {
        "industry": industry,
        "query": query,
        "detected_intent": asdict(intent) if intent else None,
        "requires_escalation": intent.escalate_to_human if intent else False
    }


# MCP Tool: Create Ticket
@mcp.tool()
async def create_ticket(
    industry: str,
    subject: str,
    description: str,
    priority: str = "medium",
    category: str = "general"
) -> dict:
    """
    Create a support ticket for a specific industry.
    
    Args:
        industry: Industry name
        subject: Ticket subject
        description: Ticket description
        priority: Priority level (low, medium, high)
        category: Ticket category
        
    Returns:
        Created ticket information
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return {"error": f"Industry '{industry}' not found"}
    
    return {
        "status": "created",
        "ticket_id": f"TKT-{hash(subject) % 100000:05d}",
        "subject": subject,
        "description": description,
        "priority": priority,
        "category": category,
        "industry": industry
    }


# MCP Tool: Update Record
@mcp.tool()
async def update_record(industry: str, record_id: str, fields: dict) -> dict:
    """
    Update a record in the system.
    
    Args:
        industry: Industry name
        record_id: Record identifier
        fields: Fields to update
        
    Returns:
        Update confirmation
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return {"error": f"Industry '{industry}' not found"}
    
    return {
        "status": "updated",
        "industry": industry,
        "record_id": record_id,
        "updated_fields": fields,
        "timestamp": "2026-01-17T00:00:00Z"
    }


# MCP Tool: Send Notification
@mcp.tool()
async def send_notification(
    industry: str,
    channel: str,
    recipient: str,
    message: str
) -> dict:
    """
    Send notification via configured channel.
    
    Args:
        industry: Industry name
        channel: Notification channel (email, sms, slack)
        recipient: Recipient identifier
        message: Message content
        
    Returns:
        Notification status
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return {"error": f"Industry '{industry}' not found"}
    
    return {
        "status": "sent",
        "industry": industry,
        "channel": channel,
        "recipient": recipient,
        "message": message
    }


# MCP Resource: Knowledge Base
@mcp.resource("knowledge://{industry}/all")
async def get_knowledge_base(industry: str) -> str:
    """
    Get the full knowledge base for an industry.
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return json.dumps({"error": f"Industry '{industry}' not found"})
    
    return json.dumps({
        "industry": industry,
        "search_type": bot["config"].search_type,
        "document_count": len(bot["knowledge_base"].documents),
        "documents": bot["knowledge_base"].documents
    }, indent=2)


# MCP Resource: Intents
@mcp.resource("intents://{industry}/all")
async def get_intents(industry: str) -> str:
    """
    Get all intents for an industry.
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return json.dumps({"error": f"Industry '{industry}' not found"})
    
    return json.dumps({
        "industry": industry,
        "intents": [asdict(intent) for intent in bot["intent_detector"].intents]
    }, indent=2)


# MCP Resource: Actions
@mcp.resource("actions://{industry}/all")
async def get_actions(industry: str) -> str:
    """
    Get all actions for an industry.
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return json.dumps({"error": f"Industry '{industry}' not found"})
    
    return json.dumps({
        "industry": industry,
        "actions": bot["actions"]
    }, indent=2)


# MCP Resource: Persona
@mcp.resource("persona://{industry}/config")
async def get_persona(industry: str) -> str:
    """
    Get bot persona configuration for an industry.
    """
    bot = bot_manager.get_bot(industry)
    if not bot:
        return json.dumps({"error": f"Industry '{industry}' not found"})
    
    return json.dumps({
        "industry": industry,
        "persona": bot["config"].persona
    }, indent=2)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  MCP Knowledge-Powered Q&A and Action Bot Server (FastMCP)")
    print("  Venture Studio Hackathon - Challenge 1 & 2")
    print("="*70)
    
    # Check for OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"\n✓ OpenAI API Key configured (last 4 chars: ...{openai_key[-4:]})")
    else:
        print(f"\n⚠ OpenAI API Key not found. Set OPENAI_API_KEY in .env file")
    
    print(f"\n🚀 Starting server on http://0.0.0.0:8000")
    print(f"📚 Loaded industries: {', '.join(bot_manager.get_industries())}")
    print(f"\n🔍 Health Endpoints:")
    print(f"   • GET /health - Root health check")
    print(f"   • GET /health/{{industry}} - Industry-specific health")
    print(f"   • GET /industries - List all industries")
    print(f"\n🛠️  MCP Tools Available:")
    print(f"   • search_knowledge(industry, query, top_k)")
    print(f"   • detect_intent(industry, query)")
    print(f"   • create_ticket(industry, subject, description, priority, category)")
    print(f"   • update_record(industry, record_id, fields)")
    print(f"   • send_notification(industry, channel, recipient, message)")
    print(f"\n📌 MCP Resources Available:")
    print(f"   • knowledge://{{industry}}/all")
    print(f"   • intents://{{industry}}/all")
    print(f"   • actions://{{industry}}/all")
    print(f"   • persona://{{industry}}/config")
    print("="*70 + "\n")
    
    mcp.run(transport="http", host="0.0.0.0", port=8000)
