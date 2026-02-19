# Challenge 3 Quick Reference

## 1️⃣ Setup (5 minutes)

```bash
# 1. Get API key from LLM provider
#    - Claude: https://console.anthropic.com/account/keys
#    - Gemini: https://aistudio.google.com/app/apikey
#    - OpenAI: https://platform.openai.com/api-keys

# 2. Create .env file
echo "GOOGLE_API_KEY=your-key" > .env

# 3. Install dependencies
pip install -r clients/requirements-llm.txt

# 4. Start MCP server (terminal 1)
python src/fastmcp_server.py

# 5. Run LLM client (terminal 2)
python clients/gemini_client.py
python clients/claude_client.py    # or this
python clients/openai_client.py    # or this
```

## 2️⃣ Usage

```
Select industry: banking

💬 Chat with the bot:
You: I lost my card
🤖 Bot: [searches knowledge, creates ticket if needed]

Switch industry anytime:
You: switch
New industry: healthcare

Exit:
You: quit
```

## 3️⃣ Key Files

| File | Purpose |
|------|---------|
| `clients/gemini_client.py` | Google Gemini LLM client |
| `clients/claude_client.py` | Anthropic Claude client |
| `clients/openai_client.py` | OpenAI GPT client |
| `CHALLENGE_3_SETUP.md` | Full documentation |
| `CHALLENGE_3_COMPLETE.md` | Architecture details |

## 4️⃣ Tools Available to LLM

| Tool | Input | Output |
|------|-------|--------|
| `search_knowledge` | query, top_k | matching docs |
| `detect_intent` | query | intent + escalation |
| `create_ticket` | subject, description, priority | ticket_id |
| `update_record` | record_id, fields | status |
| `send_notification` | channel, recipient, message | status |

## 5️⃣ Industries

- **banking** - Account support, transfers, fraud
- **healthcare** - Appointments, prescriptions, billing
- **telecom** - Connectivity, plans, billing
- **government** - Permits, benefits, services
- **saas** - Features, bugs, integration

## 6️⃣ What Gets Returned

```json
{
  "success": true,
  "query": "user question",
  "industry": "banking",
  "response": "bot answer",
  "tools_called": [
    {
      "name": "search_knowledge",
      "args": {"industry": "banking", "query": "...", "top_k": 5},
      "result": {"results": [...]}
    }
  ],
  "needs_escalation": false,  // escalation flag
  "turns": 2,
  "logs": [...]  // detailed execution trace
}
```

## 7️⃣ Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not set" | Add to `.env`: `GOOGLE_API_KEY=...` |
| "Industries empty" | Check MCP server running |
| "Connection refused" | Ensure MCP server on port 8000 |
| "Tool failed" | Check MCP server logs |

## 8️⃣ LLM Comparison

| Feature | Gemini | Claude | OpenAI |
|---------|--------|--------|--------|
| Native MCP | ✅ | ❌ (via tools) | ❌ (via tools) |
| Speed | Fast | Slow | Medium |
| Cost | Cheapest | Mid | Mid |
| Reasoning | Good | Best | Good |

## 9️⃣ Commands

```bash
# Start everything
terminal-1: python src/fastmcp_server.py
terminal-2: python clients/gemini_client.py

# Test MCP server
curl http://localhost:8000/health
curl http://localhost:8000/industries

# Call a tool directly
curl -X POST http://localhost:8000/mcp/tool/search_knowledge \
  -H "Content-Type: application/json" \
  -d '{"industry":"banking","query":"card","top_k":2}'
```

## 🔟 Next Steps

1. ✅ Run client
2. ✅ Test with banking → healthcare switch
3. ✅ Try complex queries (multi-step)
4. 📋 Monitor execution logs
5. 🚀 Deploy to production
