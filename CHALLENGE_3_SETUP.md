# Challenge 3: LLM Integration Setup Guide

## Overview

Challenge 3 integrates the MCP server with Large Language Models (LLMs) so Claude, Gemini, or OpenAI can:
- Search the knowledge base
- Detect user intent
- Create tickets and take actions
- Adapt responses based on industry persona
- Escalate complex queries to humans

## Architecture

```
User Query
    ↓
LLM Client (Claude/Gemini/OpenAI)
    ↓
Tool Calling Loop:
  1. LLM analyzes query
  2. Calls MCP tools (search_knowledge, detect_intent, etc.)
  3. MCP server executes tools
  4. LLM receives results
  5. LLM generates final response
    ↓
Final Response + Reasoning
```

## Prerequisites

- MCP server running: `python src/fastmcp_server.py`
- API key for your chosen LLM provider

## Setup

### 1. Install LLM Client Dependencies

```bash
pip install -r clients/requirements-llm.txt
```

### 2. Set Up Environment Variables

Create `.env` file in project root:

```env
# Choose one or more:

# Google Gemini
GOOGLE_API_KEY=your-gemini-api-key

# Anthropic Claude
ANTHROPIC_API_KEY=your-claude-api-key

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# MCP Server URL (default: http://localhost:8000)
MCP_SERVER_URL=http://localhost:8000
```

### 3. Start MCP Server

In terminal 1:
```bash
cd mcp-qa-bot
python src/fastmcp_server.py
```

Confirm it's running:
```bash
curl http://localhost:8000/health
```

### 4. Run LLM Client

In terminal 2:

**For Gemini:**
```bash
python clients/gemini_client.py
```

**For Claude:**
```bash
python clients/claude_client.py
```

**For OpenAI:**
```bash
python clients/openai_client.py
```

## Usage

1. Select industry:
```
Select industry (e.g., banking, healthcare, telecom): banking
✅ Industry switched to: banking
```

2. Ask questions:
```
You: I lost my credit card, what should I do?

(Bot searches knowledge, detects intent, may create ticket)

🤖 Bot: Here are the steps to report your lost card...
```

3. Switch industries mid-conversation:
```
You: switch
New industry: healthcare

(Bot now answers healthcare questions)
```

4. Exit:
```
You: quit
```

## Features

### Tool Calling
The LLM can call 5 tools:
- **search_knowledge** - Find answers in knowledge base
- **detect_intent** - Understand what user wants
- **create_ticket** - Create support ticket
- **update_record** - Modify data
- **send_notification** - Send messages

### Persona-Based Responses
Each industry has a persona (tone, greeting, closing) that the LLM uses to style responses.

### Escalation Logic
If a query:
- Fails tool execution
- Returns "no answer found"
- Matches sensitive keywords

The bot will flag: ⚠️ **This query needs human escalation**

### Industry Switching
Switch between 5 industries without restarting:
- Banking - Account support, transfers, fraud
- Healthcare - Patient queries, appointments, prescriptions
- Telecom - Connectivity issues, plan help
- Government - Citizen services, permits, benefits
- SaaS - Product help, features, billing

### Structured Output
Each response includes:
- Query
- Industry
- Final response
- Tools called (with inputs/outputs)
- Escalation flag
- Execution logs (timestamps, errors)

## Example Conversations

### Banking
```
You: Can I transfer money between my accounts?
🤖 Bot: Yes, you can transfer money between your accounts. 
        Here's how to do it through online banking...
```

### Healthcare
```
You: How do I schedule an appointment?
🤖 Bot: To schedule an appointment, you can:
        1. Call our clinic...
        2. Use our online portal...
```

### Telecom
```
You: My internet is not working
🤖 Bot: Let's troubleshoot. First, please check:
        1. Is the modem powered on?...
```

## Troubleshooting

**"GOOGLE_API_KEY not set"**
- Add `GOOGLE_API_KEY=...` to `.env`
- Restart the client

**"Industries list is empty"**
- Ensure MCP server is running
- Check `/industries` endpoint: `curl http://localhost:8000/industries`

**"Tool call failed"**
- Verify MCP server is running
- Check tool name spelling
- Look at execution logs in response

**"Connection refused"**
- Start MCP server first
- Check MCP_SERVER_URL in `.env`
- Default is `http://localhost:8000`

## Execution Logs

Each response includes detailed logs:
```json
{
  "success": true,
  "query": "I lost my card",
  "industry": "banking",
  "response": "Here are the steps...",
  "tools_called": [
    {
      "name": "search_knowledge",
      "args": {"industry": "banking", "query": "lost card", "top_k": 5},
      "result": {"results": [...]}
    }
  ],
  "needs_escalation": false,
  "turns": 2,
  "logs": [...]
}
```

## API Keys

### Get Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click "Get API Key"
3. Create new key
4. Copy to `.env`

### Get Claude API Key
1. Go to https://console.anthropic.com/account/keys
2. Create new key
3. Copy to `.env`

### Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create new key
3. Copy to `.env`

## Next Steps

1. Test with different industries
2. Try complex multi-step queries
3. Monitor execution logs for patterns
4. Add custom intents to `configs/*.yaml`
5. Extend tool definitions in client files
