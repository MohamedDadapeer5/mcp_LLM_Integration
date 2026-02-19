# Architecture Overview - Knowledge-Powered Q&A and Action Bot

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          CLAUDE/AI CLIENT                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    MCP Communication
                  (Resources + Tools)
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  MCP SERVER (server.py)                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    RESOURCE HANDLERS                       │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │  Knowledge   │  │   Intents    │  │   Actions    │   │ │
│  │  │  Base (KB)   │  │  Taxonomy    │  │  Connectors  │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  │                    ┌──────────────┐                       │ │
│  │                    │ Bot Persona  │                       │ │
│  │                    │  (Tone/Style)│                       │ │
│  │                    └──────────────┘                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      TOOL HANDLERS                         │ │
│  │  ┌────────────────┐  ┌────────────────┐                   │ │
│  │  │ search_        │  │ detect_        │                   │ │
│  │  │ knowledge()    │  │ intent()       │                   │ │
│  │  └────────────────┘  └────────────────┘                   │ │
│  │  ┌────────────────┐  ┌────────────────┐                   │ │
│  │  │ create_        │  │ update_        │                   │ │
│  │  │ ticket()       │  │ record()       │                   │ │
│  │  └────────────────┘  └────────────────┘                   │ │
│  │  ┌────────────────┐                                       │ │
│  │  │ send_          │                                       │ │
│  │  │ notification() │                                       │ │
│  │  └────────────────┘                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  CORE COMPONENTS                           │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │ KnowledgeBase: Text/Semantic/Hybrid Search          │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │ IntentDetector: Keyword-based Intent Matching       │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │ ActionExecutor: Mock/Webhook/REST API Actions       │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │ QABotConfig: Load YAML/JSON Configuration           │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                 ┌─────────┴────────┐
                 │                  │
        ┌────────▼──────────┐  ┌────▼──────────┐
        │  External Systems │  │  Configuration│
        │  (Webhooks/APIs)  │  │  Files (YAML) │
        └───────────────────┘  └───────────────┘
```

## Data Flow - User Interaction

```
1. USER INPUT
   └─→ "Check my account balance"

2. INTENT DETECTION
   Query: "check account balance"
   Detector: Matches keywords ["balance", "check", "account"]
   Result: intent = "account_balance"
   └─→ Escalate: false (no human needed)

3. KNOWLEDGE SEARCH
   KB: Search documents about balance
   Method: Hybrid (text + semantic)
   Documents:
   - "How to Check Account Balance"
   - "Account Features and Services"
   └─→ Top 5 most relevant documents

4. ANSWER GENERATION (Claude)
   Claude: Uses search results + persona to generate response
   Tone: Formal (banking persona)
   Template: "You can check your balance through..."
   └─→ Personalized response

5. ACTION EXECUTION (if needed)
   Intent: account_balance (no actions needed)
   If transferred: Calls transfer_funds action
   └─→ Ticket created or transfer processed

6. RESPONSE TO USER
   └─→ "Your balance is $X. You can check 24/7 through..."
```

## Configuration Structure

```
Config File (YAML/JSON)
│
├─ industry: "banking"
│  └─ Determines intent/action sets
│
├─ bot_persona:
│  ├─ tone: "formal" | "friendly" | etc
│  ├─ greeting: Custom greeting message
│  ├─ closing: Custom closing message
│  └─ escalation_message: Human handoff message
│
├─ knowledge:
│  ├─ corpus_path: Path to KB documents
│  └─ search_type: "text" | "semantic" | "hybrid"
│
├─ intents: [Array of Intent Definitions]
│  └─ name: "account_transfer"
│     ├─ keywords: ["transfer", "send", "money"]
│     ├─ description: "User wants to move funds"
│     ├─ fallback: false
│     └─ escalate_to_human: false
│
└─ actions: [Array of Action Connectors]
   └─ name: "transfer_funds"
      ├─ type: "webhook" | "rest_api" | "mock"
      ├─ endpoint: "https://api.banking.internal/transfers"
      └─ method: "POST"
```

## Search Strategy Comparison

```
┌──────────────┬─────────────┬──────────────┬────────────────┐
│  Search Type │   Speed     │   Accuracy   │   Use Case     │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ Text         │ Very Fast   │ Good         │ FAQ matching   │
│              │ (inverted   │ (keywords)   │ Simple queries │
│              │  index)     │              │                │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ Semantic     │ Slower      │ Excellent    │ Complex        │
│              │ (embedding  │ (meaning)    │ questions      │
│              │  comparison)│              │ Understanding  │
├──────────────┼─────────────┼──────────────┼────────────────┤
│ Hybrid       │ Moderate    │ Best         │ Production     │
│              │ (both       │ (combined)   │ (recommended)  │
│              │  methods)   │              │                │
└──────────────┴─────────────┴──────────────┴────────────────┘

Implementation:
- Text: Inverted index, O(1) lookup
- Semantic: Embeddings + cosine similarity (extensible)
- Hybrid: Combine both ranking methods
```

## Intent Detection Flow

```
User Query: "I was charged twice and want a refund"
                    │
                    ▼
         ┌──────────────────────┐
         │  Tokenize & Extract  │
         │  Keywords            │
         └──────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   "charged"  "twice"  "refund"
        │           │           │
        └───────────┼───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  Intent Matching     │
         │  (Check Keywords)    │
         └──────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
   billing_issue            fallback
   [charge, refund]         [default]
        │                       │
        └───────────┬───────────┘
                    ▼
        ┌──────────────────────┐
        │  Selected Intent     │
        │  billing_issue       │
        │  escalate: true      │
        └──────────────────────┘
                    │
                    ▼
        Create support ticket
        Assign to human specialist
```

## Action Execution Pipeline

```
Tool Call: create_ticket(...)
           │
           ▼
┌──────────────────────────────┐
│ Validate Input              │
│ - Check required fields     │
│ - Validate data types       │
└──────────────────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ Lookup Action Connector     │
│ - name: "create_ticket"     │
│ - type: "mock"              │
└──────────────────────────────┘
           │
           ▼
        ┌──┴───────────────────┐
        │                      │
        ▼                      ▼
    ┌─────┐              ┌──────────┐
    │Mock │              │Webhook/API
    └──┬──┘              └──────┬───┘
       │                        │
       ▼                        ▼
  Return Mock          Execute HTTP Request
  Response             Return Response
       │                        │
       └────────┬───────────────┘
                ▼
        ┌──────────────────────────────┐
        │ Return Result to Claude      │
        │ {                            │
        │   status: "created",         │
        │   ticket_id: "TKT-12345"     │
        │ }                            │
        └──────────────────────────────┘
```

## Multi-Industry Switching

```
Directory Structure:
├─ configs/
│  ├─ banking.yaml
│  ├─ healthcare.yaml
│  ├─ saas.yaml
│  ├─ government.yaml
│  └─ telecom.yaml
│
├─ knowledge/
│  ├─ banking-kb.yaml
│  ├─ healthcare-kb.yaml
│  ├─ saas-kb.yaml
│  ├─ government-kb.yaml
│  └─ telecom-kb.yaml
│
└─ src/
   └─ server.py (ONE FILE, handles all)

Usage:
python src/server.py configs/banking.yaml
  → Banking bot with banking intents/actions

python src/server.py configs/healthcare.yaml
  → Healthcare bot with healthcare intents/actions

python src/server.py configs/retail.yaml
  → Retail bot with retail intents/actions (add your own!)

SAME CODE, DIFFERENT BEHAVIOR!
```

## Resource Exposure

```
┌────────────────────────────────────────────┐
│  MCP Resources Exposed to Claude           │
├────────────────────────────────────────────┤
│                                            │
│  knowledge://all                           │
│  ├─ Industry: banking                      │
│  ├─ Document Count: 6                      │
│  └─ Documents:                             │
│     ├─ "How to Check Account Balance"      │
│     ├─ "How to Transfer Money"             │
│     ├─ "Fraud Protection Process"          │
│     ├─ "Loan Options"                      │
│     ├─ "Card Services"                     │
│     └─ "Minimum Balance Requirements"      │
│                                            │
│  intents://all                             │
│  ├─ Industry: banking                      │
│  └─ Intents:                               │
│     ├─ account_balance (no escalate)       │
│     ├─ account_transfer (no escalate)      │
│     ├─ fraud_dispute (ESCALATE)            │
│     ├─ loan_inquiry (no escalate)          │
│     └─ card_issue (no escalate)            │
│                                            │
│  actions://all                             │
│  ├─ Industry: banking                      │
│  └─ Actions:                               │
│     ├─ create_ticket                       │
│     ├─ update_account                      │
│     ├─ send_notification                   │
│     └─ transfer_funds                      │
│                                            │
│  persona://config                          │
│  ├─ Industry: banking                      │
│  ├─ Tone: formal                           │
│  └─ Messages: [greeting, closing, etc]     │
│                                            │
└────────────────────────────────────────────┘
```

## Class Relationships

```
ManagedKnowledgeQABot
├─ Contains: KnowledgeBase
│  ├─ Documents: List[Document]
│  ├─ Index: Inverted index for text search
│  └─ Methods:
│     ├─ text_search(query)
│     ├─ semantic_search(query)
│     └─ hybrid_search(query)
│
├─ Contains: IntentDetector
│  ├─ Intents: List[IntentDefinition]
│  └─ Methods:
│     └─ detect(query) → IntentDefinition
│
├─ Contains: ActionExecutor
│  ├─ Connectors: Dict[name, Connector]
│  └─ Methods:
│     └─ execute(action_name, input_data)
│
├─ Contains: QABotConfig
│  └─ Config: Dict[key, value]
│
└─ Contains: MCP Server
   ├─ Resources: Registered resource handlers
   └─ Tools: Registered tool handlers
```

## Data Models

```python
@dataclass
IntentDefinition:
  name: str                          # Unique intent name
  description: str                   # Human-readable description
  keywords: List[str]                # Keywords to match
  fallback: bool                     # Is this the fallback?
  escalate_to_human: bool            # Requires human review?

@dataclass
ActionConnector:
  name: str                          # Action name
  type: str                          # mock|webhook|rest_api
  endpoint: Optional[str]            # Where to send requests
  method: str                        # HTTP method
  headers: Dict[str, str]            # Custom headers
  mock_response: Optional[Dict]      # Mock response data
```

---

This architecture enables instant industry switching while maintaining code clarity and modularity. The configuration-driven approach means scaling to new industries requires only adding new YAML files, not modifying the server code.
