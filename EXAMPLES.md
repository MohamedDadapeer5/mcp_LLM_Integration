"""
Example usage patterns for the QA Bot MCP Server
"""

# Example 1: Banking Bot - Customer Inquiry
# ==========================================

BANKING_SCENARIO = """
Customer: "My credit card was declined at a store, but I have money in my account"

MCP Flow:
1. Claude receives customer message
2. Calls detect_intent("My credit card was declined...")
   → Returns: intent="card_issue", escalate_to_human=false
3. Calls search_knowledge("card declined declined atm")
   → Returns: Documents about card issues, blocking, PIN issues
4. Claude synthesizes answer from knowledge
5. If customer says "I think it's fraud", Claude:
   → Calls detect_intent() again
   → Gets: escalate_to_human=true for fraud_dispute
   → Calls create_ticket(subject="Card Fraud Report", description="...")
   → Customer directed to specialist
"""

# Example 2: Healthcare Bot - Prescription Refill
# ================================================

HEALTHCARE_SCENARIO = """
Patient: "I need to refill my diabetes medication, it's almost gone"

MCP Flow:
1. Claude receives message
2. Calls detect_intent("refill medication")
   → Returns: intent="prescription_refill"
3. Calls search_knowledge("prescription refill pharmacy")
   → Returns: Steps for refill, pharmacy hours, insurance info
4. Claude explains options based on knowledge:
   - Online through portal (recommended - ready in 24hrs)
   - Call pharmacy
   - Ask at next appointment
5. Claude offers to create action:
   → Calls send_notification(
       channel="email",
       recipient="patient@example.com",
       message="Click here to refill prescription..."
     )
"""

# Example 3: SaaS Bot - Bug Report
# ================================

SAAS_SCENARIO = """
User: "The export feature is broken, it just shows a blank screen"

MCP Flow:
1. Claude receives bug report
2. Calls detect_intent("export broken blank screen")
   → Returns: intent="bug_report", escalate_to_human=true
3. Calls search_knowledge("export feature troubleshooting")
   → Returns: Common export issues, browser requirements, solutions
4. Claude checks knowledge:
   - Suggests clearing cache
   - Checking browser compatibility
   - Trying incognito mode
5. If not resolved, Claude:
   → Calls create_ticket(
       subject="Export Feature - Blank Screen",
       description="User reports blank screen when exporting...",
       priority="high",
       category="bug"
     )
   → User gets ticket number and ETA for fix
"""

# Example 4: Government Bot - Permit Application
# ===============================================

GOVERNMENT_SCENARIO = """
Citizen: "I want to add a deck to my house, what do I need?"

MCP Flow:
1. Claude receives query
2. Calls detect_intent("add deck home permit")
   → Returns: intent="permit_application"
3. Calls search_knowledge("building permit application deck")
   → Returns: Requirements, forms, fees, timeline
4. Claude provides comprehensive answer:
   - Need: property survey, architectural plans, ownership proof
   - Fee: $500-$2000 depending on size
   - Timeline: 10-15 business days
   - Accessibility: online portal, by mail, or in person
5. Claude offers:
   → Calls send_notification(
       channel="email",
       message="Attached: Building Permit Checklist and Application Form"
     )
   → User receives documents to prepare
"""

# Example 5: Telecom Bot - Troubleshooting
# =========================================

TELECOM_SCENARIO = """
Customer: "I have no signal and my phone won't make calls"

MCP Flow:
1. Claude receives troubleshooting request
2. Calls detect_intent("no signal no calls network")
   → Returns: intent="connectivity_issue", escalate_to_human=true
3. Calls search_knowledge("no signal troubleshooting network")
   → Returns: Step-by-step troubleshooting guide
4. Claude walks through steps:
   1. Power off for 30 seconds
   2. Check airplane mode
   3. Manually select network
   4. Remove/reinsert SIM
   5. Update software
5. After each step, Claude can:
   → Suggest next action
   → If unresolved: Calls create_ticket() for tech support
   → Can offer: restart service, device replacement
"""

# Example 6: Using All Search Types
# ==================================

SEARCH_TYPE_EXAMPLES = """
Same query: "How do I check my balance?"

Text Search (Banking):
- Fast, works with keywords
- Results: Documents containing "balance", "check", "account"
- Best for: Simple FAQ lookups

Semantic Search (Healthcare):
- Slow, finds meaning
- Results: Documents about checking medical progress
- Best for: Complex medical queries

Hybrid Search (SaaS):
- Balanced approach
- Results: Mix of keyword matches and semantic similarity
- Best for: Technical docs + guides
"""

# Example 7: Intent-Based Access Control
# =======================================

ACCESS_CONTROL_EXAMPLE = """
Different intents = Different actions available:

Intent: account_balance
├─ Tools available: search_knowledge, detect_intent
└─ No action tools (read-only)

Intent: account_transfer
├─ Tools available: search_knowledge, detect_intent, create_ticket
└─ Actions: transfer_funds (webhook to payment system)

Intent: fraud_dispute
├─ Tools available: All
└─ Actions: create_ticket (escalates to human), update_record
└─ Escalate: true (requires human approval)

Intent: medical_guidance
├─ Tools available: search_knowledge only
└─ Cannot create records without doctor review
└─ Escalate: true
"""

# Example 8: Config-Driven Persona
# ================================

PERSONA_EXAMPLES = """
Banking (Formal):
  Tone: formal
  Greeting: "Hello, I'm your banking assistant."
  Response: "Account balance inquiry processed successfully."

Healthcare (Empathetic):
  Tone: friendly
  Greeting: "Welcome! I'm here to help with your health questions."
  Response: "I understand your concern. Let me help you find..."

SaaS (Concise):
  Tone: friendly
  Greeting: "Hi! What can I help you with today?"
  Response: "Found it! Here's how to..."

All set through config, not code rewrites!
"""

# Example 9: Multi-Intent in Same Conversation
# ==============================================

MULTI_INTENT_SCENARIO = """
Customer: "I was charged twice for my phone bill, I need to dispute this. 
Also, can I upgrade my plan?"

MCP Flow:
1. First message detected:
   → Intent: billing_issue (first sentence)
   → Intent: plan_change (second sentence)

2. Claude handles both:
   - For billing: Create ticket, search knowledge on disputes
   - For plan change: Search knowledge on plans, help upgrade

3. Results in one integrated response:
   "I found duplicate charges from Jan 15. I've created ticket TKT-12345
    for investigation (10 business days). Meanwhile, let me show you
    your plan upgrade options..."
"""

# Example 10: Knowledge Base Evolution
# ====================================

KB_EVOLUTION_EXAMPLE = """
Version 1: Static YAML files
├─ Simple and fast
├─ Good for hackathon MVP
└─ Limited to ~1000 documents

Version 2: Vector database (Pinecone/Weaviate)
├─ Scales to millions of documents
├─ True semantic search
└─ Real-time indexing

Version 3: Hybrid retrieval
├─ BM25 text search + vector semantic search
├─ Combine scores for best results
└─ Production-grade accuracy

Version 4: Knowledge graphs
├─ Relationships between concepts
├─ Question decomposition
└─ Multi-hop reasoning
"""

if __name__ == "__main__":
    print("See documentation for usage examples")
