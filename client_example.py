"""
Example client code showing how to interact with the QA Bot MCP Server
"""

import asyncio
import json
from typing import Dict, List


class QABotClient:
    """Example client for interacting with QA Bot MCP Server"""

    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url

    async def get_resources(self) -> List[Dict]:
        """Get available resources"""
        print("📚 Available Resources:")
        return [
            {"uri": "knowledge://all", "name": "Knowledge Base"},
            {"uri": "intents://all", "name": "Intent Taxonomy"},
            {"uri": "actions://all", "name": "Action Connectors"},
            {"uri": "persona://config", "name": "Bot Persona"},
        ]

    async def search_knowledge(self, query: str, top_k: int = 5) -> Dict:
        """Search knowledge base"""
        print(f"\n🔍 Searching knowledge base: '{query}'")
        # In real implementation, call MCP server
        return {
            "query": query,
            "results": [
                {
                    "id": "doc_001",
                    "title": "How to...",
                    "content": "...",
                    "relevance": 0.95
                }
            ]
        }

    async def detect_intent(self, query: str) -> Dict:
        """Detect user intent"""
        print(f"\n🎯 Detecting intent: '{query}'")
        # In real implementation, call MCP server
        return {
            "query": query,
            "detected_intent": "account_help",
            "confidence": 0.92,
            "escalate_to_human": False
        }

    async def create_ticket(self, subject: str, description: str) -> Dict:
        """Create support ticket"""
        print(f"\n🎫 Creating ticket: {subject}")
        return {
            "status": "created",
            "ticket_id": "TKT-12345",
            "subject": subject
        }

    async def send_notification(self, channel: str, recipient: str, message: str) -> Dict:
        """Send notification"""
        print(f"\n📨 Sending {channel} to {recipient}")
        return {
            "status": "sent",
            "channel": channel,
            "recipient": recipient
        }


async def example_banking_conversation():
    """Example: Banking customer support conversation"""
    print("=" * 60)
    print("EXAMPLE 1: Banking Customer - Balance Check")
    print("=" * 60)

    client = QABotClient()

    # Step 1: Customer asks question
    customer_query = "What's my current account balance?"
    print(f"\n👤 Customer: {customer_query}")

    # Step 2: Detect intent
    intent = await client.detect_intent(customer_query)
    print(f"✓ Intent: {intent['detected_intent']}")

    # Step 3: Search knowledge
    knowledge = await client.search_knowledge("account balance check")
    print(f"✓ Found {len(knowledge['results'])} relevant documents")

    # Step 4: Bot response (simulated)
    print("\n🤖 Bot: You can check your balance through:")
    print("  1. Online banking portal")
    print("  2. Mobile app")
    print("  3. ATM or bank teller")
    print("  4. Phone customer service: 1-800-BANK-123")


async def example_healthcare_appointment():
    """Example: Healthcare patient booking appointment"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Healthcare Patient - Book Appointment")
    print("=" * 60)

    client = QABotClient()

    customer_query = "I need to schedule a doctor's appointment"
    print(f"\n👤 Patient: {customer_query}")

    # Detect intent
    intent = await client.detect_intent(customer_query)
    print(f"✓ Intent: {intent['detected_intent']}")

    # Search knowledge
    knowledge = await client.search_knowledge("appointment booking schedule")
    print(f"✓ Found appointment instructions")

    # Bot response
    print("\n🤖 Bot: I can help you book an appointment!")
    print("  Available methods:")
    print("  1. Online: patient-portal.health.com")
    print("  2. Phone: 1-800-HEALTH-1")
    print("  3. Mobile app: Available on iOS and Android")


async def example_saas_bug_report():
    """Example: SaaS user reporting a bug"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: SaaS User - Bug Report")
    print("=" * 60)

    client = QABotClient()

    customer_query = "The export function crashes when I click it"
    print(f"\n👤 User: {customer_query}")

    # Detect intent
    intent = await client.detect_intent(customer_query)
    print(f"✓ Intent: {intent['detected_intent']}")
    print(f"✓ Escalate to human: {intent['escalate_to_human']}")

    # Search knowledge
    knowledge = await client.search_knowledge("export feature troubleshooting")
    print(f"✓ Found troubleshooting steps")

    # Bot response
    print("\n🤖 Bot: I'm sorry you're experiencing issues.")
    print("  Quick fixes to try:")
    print("  1. Clear browser cache")
    print("  2. Try incognito/private mode")
    print("  3. Update your browser")

    # If not resolved, create ticket
    print("\n  Let me create a bug report for our team...")
    ticket = await client.create_ticket(
        subject="Export Function Crash",
        description="User reports export button causes crash"
    )
    print(f"✓ Ticket created: {ticket['ticket_id']}")


async def example_government_permit():
    """Example: Government citizen applying for permit"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Government - Building Permit")
    print("=" * 60)

    client = QABotClient()

    customer_query = "I want to add a deck to my house. What do I need?"
    print(f"\n👤 Citizen: {customer_query}")

    # Detect intent
    intent = await client.detect_intent(customer_query)
    print(f"✓ Intent: {intent['detected_intent']}")

    # Search knowledge
    knowledge = await client.search_knowledge("building permit application requirements")
    print(f"✓ Found permit requirements")

    # Bot response
    print("\n🤖 Bot: To add a deck, you'll need:")
    print("  Required documents:")
    print("  • Property survey")
    print("  • Architectural plans")
    print("  • Proof of ownership")
    print("\n  Processing:")
    print("  • Fee: $500-$2000")
    print("  • Timeline: 10-15 business days")
    print("  • Submit online or in person")

    # Send documents
    await client.send_notification(
        channel="email",
        recipient="citizen@example.com",
        message="Attached: Permit Application Checklist"
    )


async def example_telecom_troubleshooting():
    """Example: Telecom customer troubleshooting"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Telecom - Network Troubleshooting")
    print("=" * 60)

    client = QABotClient()

    customer_query = "I have no signal and can't make calls"
    print(f"\n👤 Customer: {customer_query}")

    # Detect intent
    intent = await client.detect_intent(customer_query)
    print(f"✓ Intent: {intent['detected_intent']}")
    print(f"✓ Escalate to human: {intent['escalate_to_human']}")

    # Search knowledge
    knowledge = await client.search_knowledge("network troubleshooting no signal")
    print(f"✓ Found troubleshooting guide")

    # Bot response
    print("\n🤖 Bot: Let's troubleshoot step by step:")
    print("  Step 1: Power off for 30 seconds")
    print("  Step 2: Check if airplane mode is ON (turn OFF)")
    print("  Step 3: Go to Settings > Network > Select Network Manually")
    print("  Step 4: Remove and reinsert SIM card")
    print("  Step 5: Check for software updates")

    print("\n  If still not working:")
    ticket = await client.create_ticket(
        subject="No Signal - Network Issue",
        description="Customer reports no signal after troubleshooting"
    )
    print(f"✓ Tech support ticket created: {ticket['ticket_id']}")


async def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  QA BOT MCP SERVER - CLIENT USAGE EXAMPLES              ║")
    print("╚" + "=" * 58 + "╝")

    await example_banking_conversation()
    await example_healthcare_appointment()
    await example_saas_bug_report()
    await example_government_permit()
    await example_telecom_troubleshooting()

    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)
    print("\nNext: Start the actual MCP server with a config file")
    print("  python src/server.py configs/banking.yaml")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
