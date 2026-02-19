#!/usr/bin/env python3

import asyncio
import json
import os
import httpx
from typing import Any
from openai import OpenAI, APIError, RateLimitError

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

class QABotMCPClient:
    """OpenAI-powered Q&A Bot client that uses MCP tools for industry-specific knowledge"""
    
    def __init__(self, mcp_url: str = None):
        # Use environment variable or provided URL or default to localhost
        self.mcp_url = mcp_url or os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-3.5-turbo"
        self.current_industry = None
        self.tools_info = []
        self.conversation_history = []
        
    async def initialize(self):
        """Initialize the MCP client and get available tools"""
        try:
            # Test MCP connection
            async with httpx.AsyncClient() as http_client:
                response = await http_client.get(f"{self.mcp_url}/health")
                if response.status_code == 200:
                    print("✓ Connected to MCP server")
                else:
                    print("✗ Failed to connect to MCP server")
                    return False
            return True
        except Exception as e:
            print(f"✗ MCP connection error: {e}")
            return False
    
    async def get_industries(self) -> list[str]:
        """Fetch available industries from MCP server"""
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.get(f"{self.mcp_url}/industries")
                if response.status_code == 200:
                    data = response.json()
                    return data.get("industries", [])
        except Exception as e:
            print(f"Error fetching industries: {e}")
        return []
    
    async def select_industry(self, industry: str) -> bool:
        """Select an industry for Q&A"""
        industries = await self.get_industries()
        if industry.lower() not in [i.lower() for i in industries]:
            print(f"✗ Industry '{industry}' not found")
            print(f"Available industries: {', '.join(industries)}")
            return False
        
        self.current_industry = industry.lower()
        self.conversation_history = []
        print(f"✓ Selected industry: {self.current_industry}")
        return True
    
    async def _search_knowledge(self, query: str) -> dict[str, Any]:
        """Search knowledge base for relevant information"""
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    f"{self.mcp_url}/search",
                    json={"industry": self.current_industry, "query": query}
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Knowledge search error: {e}")
        return {"results": []}
    
    async def _detect_intent(self, query: str) -> dict[str, Any]:
        """Detect user intent"""
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    f"{self.mcp_url}/detect_intent",
                    json={"industry": self.current_industry, "query": query}
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Intent detection error: {e}")
        return {"intent": "general", "confidence": 0.0}
    
    async def _escalate_to_human(self, reason: str) -> str:
        """Escalate to human agent"""
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    f"{self.mcp_url}/escalate",
                    json={"reason": reason}
                )
                if response.status_code == 200:
                    return response.json().get("ticket_id", "UNKNOWN")
        except Exception as e:
            print(f"Escalation error: {e}")
        return "ESCALATION_FAILED"
    
    async def chat(self, user_message: str) -> str:
        """Chat with OpenAI using MCP tools for context"""
        if not self.current_industry:
            print("✗ Please select an industry first")
            return ""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Search knowledge base
        knowledge = await self._search_knowledge(user_message)
        detect_intent = await self._detect_intent(user_message)
        
        # Build system prompt with context
        knowledge_context = ""
        if knowledge.get("results"):
            knowledge_context = "\n\nRelevant knowledge base information:\n"
            for result in knowledge["results"][:3]:
                knowledge_context += f"- {result}\n"
        
        system_prompt = f"""You are a helpful Q&A bot for the {self.current_industry.title()} industry.
You have access to industry-specific knowledge and best practices.
{knowledge_context}

Provide clear, accurate answers based on the knowledge provided.
If you don't have enough information to answer, offer to escalate to a human agent."""
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history
        ]
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except RateLimitError:
            print("⚠ Rate limit reached. Please try again later.")
            escalation_id = await self._escalate_to_human("Rate limit exceeded - user should retry")
            return f"I'm currently at capacity. Your case has been escalated (Ticket: {escalation_id})"
        except APIError as e:
            print(f"⚠ OpenAI API error: {e}")
            escalation_id = await self._escalate_to_human(f"API error: {str(e)}")
            return f"I encountered an error. Your case has been escalated (Ticket: {escalation_id})"

async def main():
    """Main function to run the Q&A bot"""
    print("=" * 60)
    print("Q&A Bot with OpenAI & MCP")
    print("=" * 60)
    
    # Initialize client
    client = QABotMCPClient()
    
    # Connect to MCP
    if not await client.initialize():
        print("\n✗ Failed to initialize. Make sure MCP server is running:")
        print("  python src/fastmcp_server.py")
        return
    
    # Get and display industries
    industries = await client.get_industries()
    if not industries:
        print("✗ No industries available")
        return
    
    print(f"\nAvailable industries: {', '.join(industries)}")
    
    # Select industry
    print("\nSelect your industry:")
    for i, industry in enumerate(industries, 1):
        print(f"  {i}. {industry}")
    
    choice = input("\nEnter industry number or name: ").strip()
    if choice.isdigit():
        industry = industries[int(choice) - 1] if 0 < int(choice) <= len(industries) else None
    else:
        industry = choice
    
    if not industry or not await client.select_industry(industry):
        return
    
    # Chat loop
    print(f"\n{'=' * 60}")
    print(f"Starting Q&A session for {industry}")
    print("Type 'switch' to change industry, 'exit' to quit")
    print('=' * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == "exit":
            print("✓ Goodbye!")
            break
        
        if user_input.lower() == "switch":
            print("\nSelect a new industry:")
            for i, ind in enumerate(industries, 1):
                print(f"  {i}. {ind}")
            
            choice = input("Enter industry number or name: ").strip()
            if choice.isdigit():
                industry = industries[int(choice) - 1] if 0 < int(choice) <= len(industries) else None
            else:
                industry = choice
            
            if industry and await client.select_industry(industry):
                continue
            else:
                print("✗ Invalid industry selection")
            continue
        
        # Get response from bot
        response = await client.chat(user_input)
        print(f"\nBot: {response}")

if __name__ == "__main__":
    asyncio.run(main())
