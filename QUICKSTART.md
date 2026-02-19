# Quick Start Guide - QA Bot MCP Server

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Choose Your Industry
```bash
# For Banking
python src/server.py configs/banking.yaml

# For Healthcare  
python src/server.py configs/healthcare.yaml

# For SaaS
python src/server.py configs/saas.yaml

# For Government
python src/server.py configs/government.yaml

# For Telecom
python src/server.py configs/telecom.yaml
```

### Step 3: Test with Client
```bash
python client_example.py
```

## What Happens?

1. **Server starts** with industry configuration
2. **Resources are exposed**:
   - Knowledge base (documents)
   - Intent taxonomy (categories)
   - Actions (tools)
   - Bot persona (tone/style)
3. **Claude can call tools**:
   - Search knowledge
   - Detect intent
   - Create tickets
   - Update records
   - Send notifications

## Core Concept

```
User Query → Intent Detection → Knowledge Search → Action Execution
                                                   ↓
                                            Configured Action
                                          (webhook/API/mock)
```

## Example: Banking

```
User: "I want to transfer $500 to my friend"

1. Intent Detection: ✓ Detected "account_transfer"
2. Knowledge Search: ✓ Found transfer guidelines (1-3 days, limits)
3. Escalation Check: ✗ No human needed
4. Action: User can proceed with transfer through app
```

## Example: Healthcare

```
User: "My leg hurts, what could be wrong?"

1. Intent Detection: ✓ Detected "medical_guidance"
2. Knowledge Search: ✓ Found common causes of leg pain
3. Escalation Check: ✓ Requires doctor (escalate_to_human=true)
4. Action: Create ticket for doctor review
```

## Configuration Swapping

All behavior is in YAML:
- Change `banking.yaml` → `healthcare.yaml`
- Same code, completely different bot!
- Update intents, knowledge, actions, persona in config

## What to Customize

Edit `configs/[industry].yaml`:

```yaml
bot_persona:          # Change greeting/tone
  tone: formal → friendly → concise → instructional

knowledge:            # Swap knowledge base
  corpus_path: ../knowledge/[industry]-kb.yaml

intents:              # Add your intents
  - name: your_intent
    keywords: [key, words]
    escalate_to_human: true/false

actions:              # Configure actions
  - name: action_name
    type: webhook → rest_api → mock
    endpoint: https://...
```

## Adding New Industry

1. Create config: `configs/my-industry.yaml`
2. Create KB: `knowledge/my-industry-kb.yaml`
3. Run: `python src/server.py configs/my-industry.yaml`

## Testing

```bash
# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_server.py::TestIntentDetector::test_detect_intent -v
```

## Next Steps

1. **Semantic Search**: Implement embeddings for better search
2. **Database**: Store tickets and records in database
3. **Webhooks**: Connect to real systems (Jira, Salesforce, etc.)
4. **Authentication**: Add OAuth/API key security
5. **Analytics**: Track usage and effectiveness
6. **Multi-language**: Support non-English queries

## Hackathon Checklist

- [x] MCP server with resources and tools
- [x] Knowledge base integration
- [x] Intent detection
- [x] Action execution (mock)
- [x] Multi-industry support
- [x] Configuration-driven design
- [x] Example configs for 5 industries
- [x] Documentation and examples
- [ ] Deploy to production (next challenge!)
