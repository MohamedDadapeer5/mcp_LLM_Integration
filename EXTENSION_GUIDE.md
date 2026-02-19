"""
Extension Guide: Adding New Industries to the QA Bot

This guide shows how to add a new industry without changing any code.
"""

# ============================================================================
# STEP 1: Create Industry Configuration
# File: configs/retail.yaml (Example: Retail/E-commerce)
# ============================================================================

RETAIL_CONFIG = """
industry: retail
description: E-commerce product support and order assistance bot

bot_persona:
  tone: friendly
  style: helpful
  greeting: "Welcome to our store! How can I help you find the perfect product?"
  closing: "Thanks for shopping with us! Enjoy your purchase!"
  escalation_message: "Let me connect you with a product specialist."

knowledge:
  corpus_path: ../knowledge/retail-kb.yaml
  search_type: hybrid
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"

intents:
  - name: product_search
    description: Customer searches for products
    keywords: ["find", "looking for", "product", "search", "item"]
    fallback: false
    escalate_to_human: false

  - name: order_status
    description: Customer checks order status
    keywords: ["order", "shipped", "tracking", "delivery", "where"]
    fallback: false
    escalate_to_human: false

  - name: returns_refunds
    description: Customer initiates return or refund
    keywords: ["return", "refund", "wrong", "broken", "defective"]
    fallback: false
    escalate_to_human: false

  - name: product_comparison
    description: Customer compares products
    keywords: ["compare", "difference", "better", "vs", "which one"]
    fallback: false
    escalate_to_human: false

  - name: inventory_check
    description: Check if product is in stock
    keywords: ["stock", "available", "inventory", "in stock", "out of stock"]
    fallback: false
    escalate_to_human: false

  - name: payment_issue
    description: Payment or checkout problems
    keywords: ["payment", "card", "checkout", "billing", "declined"]
    fallback: false
    escalate_to_human: true

  - name: fallback
    description: Default intent
    keywords: []
    fallback: true
    escalate_to_human: false

actions:
  - name: create_support_ticket
    type: mock
    description: Create customer support ticket
    mock_response:
      status: success
      ticket_created: true

  - name: check_inventory
    type: rest_api
    endpoint: "https://api.retail.internal/inventory/check"
    method: POST
    description: Check product availability

  - name: create_order
    type: webhook
    endpoint: "https://api.retail.internal/orders"
    method: POST
    description: Create new order

  - name: initiate_return
    type: rest_api
    endpoint: "https://api.retail.internal/returns"
    method: POST
    description: Start return process

  - name: send_tracking_email
    type: rest_api
    endpoint: "https://email.retail.internal/send"
    method: POST
    description: Send tracking information
"""

# ============================================================================
# STEP 2: Create Knowledge Base
# File: knowledge/retail-kb.yaml
# ============================================================================

RETAIL_KB = """
- id: retail_001
  title: How to Search for Products
  content: Browse by category or use search bar. Filter by price, color, size, rating. Save favorites to wishlist. Compare products side-by-side. Reviews from verified buyers help with decisions.
  category: shopping
  tags: [search, browse, filter]

- id: retail_002
  title: Order Status and Tracking
  content: Track orders from your account dashboard. Tracking number sent via email. Most orders ship in 1-2 business days. Standard shipping takes 5-7 days. Express shipping available.
  category: orders
  tags: [tracking, shipping, delivery]

- id: retail_003
  title: Returns and Refund Policy
  content: Returns accepted within 30 days of purchase for full refund or exchange. Items must be unused with original packaging. Free return shipping for defective items. Refunds processed within 5-7 business days.
  category: returns
  tags: [return, refund, exchange]

- id: retail_004
  title: Product Comparison
  content: Compare up to 4 products at once using comparison tool. View specs, features, price, ratings side-by-side. Helpful for making purchasing decisions. Share comparisons with friends.
  category: shopping
  tags: [compare, features, specs]

- id: retail_005
  title: Check Product Availability
  content: Availability shown on product page. Limited stock indicated by low inventory warnings. Pre-order available for upcoming products. Sign up for restock alerts if out of stock.
  category: inventory
  tags: [stock, availability, inventory]

- id: retail_006
  title: Payment Methods and Security
  content: Accept all major credit cards, PayPal, Apple Pay, Google Pay. SSL encryption for all transactions. Secure checkout with address verification. Fraud protection included.
  category: payment
  tags: [payment, security, checkout]
"""

# ============================================================================
# STEP 3: Run the Server
# Command: python src/server.py configs/retail.yaml
# ============================================================================

RUNNING_COMMAND = """
# Run retail bot
python src/server.py configs/retail.yaml

# Server starts with:
# - Retail intents (product_search, order_status, returns, etc.)
# - Retail knowledge base (product searching, shipping, returns)
# - Retail actions (check_inventory, create_order, etc.)
# - Retail persona (friendly, helpful tone)
"""

# ============================================================================
# EXAMPLE CONVERSATION: Retail Industry
# ============================================================================

EXAMPLE_CONVERSATION = """
Customer: "I'm looking for red shoes size 10"

Flow:
1. Intent Detection
   Query: "looking for red shoes size 10"
   → Detected: product_search
   → Escalate: false

2. Knowledge Search
   Query: "red shoes size 10"
   → Found: Product search guide, how to filter, recommendations

3. Bot Response
   "I can help! Let me search for red shoes in your size.
    You can filter by:
    • Color: Red ✓
    • Size: 10 ✓
    • Price range
    • Brand
    • Customer ratings
    
    We have 47 red shoes in size 10. Would you like to see:
    1. Best rated
    2. Most affordable
    3. Trending now
    4. New arrivals"

---

Customer: "My order hasn't arrived yet"

Flow:
1. Intent Detection
   → Detected: order_status
   → Escalate: false

2. Knowledge Search
   → Found: Order tracking info, shipping timelines

3. Bot Response
   "I can help track your order! To find it quickly, I need:
   • Order number (from confirmation email)
   • Or email address used for purchase
   
   Once you provide it, I'll show:
   • Current status
   • Tracking number
   • Estimated delivery date
   • Option to contact carrier"

---

Customer: "I want to return my shoes, they don't fit"

Flow:
1. Intent Detection
   → Detected: returns_refunds
   → Escalate: false

2. Knowledge Search
   → Found: Return policy (30 days, unused, original packaging)

3. Bot Response
   "No problem! Our return process is easy:
   
   ✓ Your purchase date: Within return window
   ✓ Condition check: Unused with packaging ✓
   
   Next steps:
   1. Click 'Return Item' in your account
   2. Choose shipping method (free return label included)
   3. Ship back to us
   4. Refund processed in 5-7 business days
   
   Ready to start? I can create a return label now."
   
   [Calls: initiate_return action]
"""

# ============================================================================
# STEP 4: Industry Configuration Checklist
# ============================================================================

CHECKLIST = """
Checklist for Adding New Industry:

□ Create configs/[industry].yaml with:
  □ industry name
  □ bot_persona (tone, greeting, closing, escalation_message)
  □ knowledge settings (corpus_path, search_type)
  □ 5-7 intents with keywords and escalation rules
  □ 3-5 actions (webhook, REST API, or mock)

□ Create knowledge/[industry]-kb.yaml with:
  □ 5-10 documents
  □ Each with: id, title, content, category, tags
  □ Cover main use cases for industry

□ Test with:
  python src/server.py configs/[industry].yaml

□ Verify resources exposed:
  □ GET knowledge://all (documents visible)
  □ GET intents://all (intents list)
  □ GET actions://all (actions available)
  □ GET persona://config (persona settings)

□ Test tools:
  □ CALL search_knowledge (finds documents)
  □ CALL detect_intent (recognizes intents)
  □ CALL create_ticket (works)
  □ CALL send_notification (works)

□ Document in:
  □ README.md (add industry to table)
  □ EXAMPLES.md (add scenario)
"""

# ============================================================================
# STEP 5: Schema Validation
# ============================================================================

CONFIG_SCHEMA = """
industry: string (required)
  - Must be unique per config file
  - Examples: banking, healthcare, saas, government, telecom, retail

bot_persona: object (required)
  - tone: "formal" | "friendly" | "concise" | "instructional"
  - style: string (optional)
  - greeting: string (required)
  - closing: string (required)
  - escalation_message: string (required)

knowledge: object (required)
  - corpus_path: string (path to KB file)
  - search_type: "text" | "semantic" | "hybrid" (default: "hybrid")
  - embedding_model: string (optional, for semantic search)

intents: array of objects (required, min 2)
  - name: string (unique identifier)
  - description: string
  - keywords: array of strings (min 1)
  - fallback: boolean (exactly 1 intent must have true)
  - escalate_to_human: boolean

actions: array of objects (required, min 1)
  - name: string (unique identifier)
  - type: "mock" | "webhook" | "rest_api"
  - endpoint: string (required if type != "mock")
  - method: "GET" | "POST" | "PUT" | "PATCH" (default: POST)
  - description: string (optional)
  - mock_response: object (required if type == "mock")
"""

# ============================================================================
# STEP 6: Common Pitfalls and Solutions
# ============================================================================

PITFALLS = """
Pitfall 1: Knowledge base too large
Solution: Start with 5-10 documents per industry, expand later

Pitfall 2: Intents overlap (same keywords)
Solution: Make keywords more specific, order matters, first match wins

Pitfall 3: No fallback intent
Solution: Always include one fallback intent with empty keywords

Pitfall 4: Wrong escalation_to_human
Solution: Escalate: true for sensitive, complex, or safety issues

Pitfall 5: Broken corpus_path
Solution: Path is relative to config file, use ../knowledge/filename

Pitfall 6: Actions don't match intents
Solution: Some intents need actions, some just need information

Pitfall 7: Persona doesn't match industry
Solution: Banking=formal, Healthcare=empathetic, SaaS=casual
"""

# ============================================================================
# STEP 7: Production Considerations
# ============================================================================

PRODUCTION_NOTES = """
When deploying to production:

1. Vector Database
   - Replace YAML file KB with Pinecone/Weaviate/Milvus
   - Enable true semantic search at scale

2. Action Handlers
   - Replace webhooks with real API integrations
   - Add authentication (OAuth, API keys)
   - Implement retry logic and error handling

3. Monitoring
   - Log all intent detections
   - Track action success/failure rates
   - Monitor search quality metrics

4. Scaling
   - Multi-instance support with load balancing
   - Caching for frequent queries
   - Async action processing

5. Security
   - Input validation for all tool calls
   - Rate limiting per user/IP
   - Audit logging for sensitive actions

6. Compliance
   - GDPR compliance for user data
   - Industry-specific regulations (HIPAA, PCI-DSS, etc.)
   - Data retention policies
"""

if __name__ == "__main__":
    print("See documentation for extension guide")
