# MCP Q&A Bot - Knowledge-Powered AI Assistant

A smart question-answering and action bot that works with Claude and other AI clients. It learns from industry-specific knowledge bases and can answer questions, understand what users want, and trigger actions automatically.

## 📌 What This Bot Does

1. **Answers Questions** - Searches through knowledge base to find answers
2. **Understands Intent** - Figures out what users actually want (e.g., "I lost my card" = account_issue)
3. **Takes Actions** - Creates tickets, updates records, sends notifications
4. **Works for Multiple Industries** - Banking, Healthcare, SaaS, Government, Telecom
5. **Runs Anywhere** - Docker-ready for any computer with Docker installed

## 🏗️ Folder Structure

```
new/
├── src/
│   └── fastmcp_server.py          # The bot server (runs on port 8000)
├── configs/                        # Industry settings
│   ├── banking.yaml
│   ├── healthcare.yaml
│   ├── saas.yaml
│   ├── government.yaml
│   └── telecom.yaml
├── knowledge/                      # Knowledge bases
│   ├── banking-kb.yaml
│   ├── healthcare-kb.yaml
│   ├── saas-kb.yaml
│   ├── government-kb.yaml
│   └── telecom-kb.yaml
├── requirements.txt                # Python libraries needed
├── Dockerfile                      # Docker instructions
├── docker-compose.yml              # Docker auto-startup
└── README.md                       # This file
```

## ⚡ Quick Start (Choose One)

### Option 1: Run Without Docker (Easiest for Testing)

**Requirements:** Python 3.11+

```bash
# 1. Go to project folder
cd new

# 2. Install libraries
pip install -r requirements.txt

# 3. Start the bot
pip install -r requirements.txt
python src/fastmcp_server.py

# 4. Open browser and test
# http://localhost:8000/health
# http://localhost:8000/industries
```

### Option 2: Run With Docker (Best for Production)

**Requirements:** Docker installed

```bash
# 1. Go to project folder
cd new

# 2. Build the Docker image
docker build -t mcp-qa-bot .

# 3. Start the bot
docker compose up --build -d
or 
docker compose up --build 

# 4. Test (same as above)
# http://localhost:8000/health


## 🔧 How to Stop the Bot

# If running without Docker:**
- Press `Ctrl+C` in terminal

# If running with Docker:**
```bash
docker compose down
```

## 🤖 Running the Gemini Client (LLM Integration)

The bot includes a Gemini-powered CLI client that connects to the MCP server for industry-specific Q&A.

### Prerequisites

- Python 3.11+
- `GEMINI_API_KEY` from [Google AI Studio](https://aistudio.google.com/)
- Running MCP server (from Option 1 or Option 2 above)

### Setup

**1. Add your Gemini API key to `.env`:**
```bash
# Create or edit .env in project root
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-1.5-flash  # optional; defaults to gemini-1.5-flash
MCP_SERVER_URL=http://localhost:8000  # optional; defaults to localhost:8000
```

**2. Install LLM client dependencies:**
```bash
pip install -r clients/requirements-llm.txt
```

**3. Run the Gemini client:**
```bash
python clients/gemini_client.py
```

### Client Usage

Once running, the client will:
1. List available industries (banking, healthcare, saas, government, telecom)
2. Prompt you to select an industry by number or name
3. Start an interactive Q&A session

**Example interaction:**
```
============================================================
Q&A Bot with Gemini & MCP
============================================================
✓ Using Gemini model: gemini-1.5-flash
✓ Connected to MCP server

Available industries: banking, healthcare, saas, government, telecom

Select your industry:
  1. banking
  2. healthcare
  3. saas
  4. government
  5. telecom

Enter industry number or name: 1
✓ Selected industry: banking

============================================================
Starting Q&A session for banking
Type 'switch' to change industry, 'exit' to quit
============================================================

You: What should I do if I lost my debit card?

Bot: If you've lost your debit card, here are the immediate steps...

You: switch
```

**Commands:**
- Type your question and press Enter to get a response
- Type `switch` to change to a different industry
- Type `exit` to quit the client

### Environment Variables

- `GEMINI_API_KEY`: Required. API key from Google AI Studio.
- `GEMINI_MODEL`: Optional. Model name (defaults to `gemini-1.5-flash`). The client auto-resolves available models.
- `MCP_SERVER_URL`: Optional. MCP server URL (defaults to `http://localhost:8000`).

### Troubleshooting

**"GEMINI_API_KEY is missing"**
- Ensure `.env` file exists in project root with `GEMINI_API_KEY=<your-key>`
- Or export it: `export GEMINI_API_KEY=<your-key>`

**"Failed to connect to MCP server"**
- Start the server first (Option 1 or 2)
- Verify server is running: `curl http://localhost:8000/health`
- Check `MCP_SERVER_URL` env var if using a non-default server address

**"No Gemini models supporting generateContent found"**
- Your API key may have limited model access
- Try setting `GEMINI_MODEL=gemini-1.5-pro` or another available model
- Contact Google Cloud support if issues persist

## 🧪 Testing the Bot

After starting the bot, try these commands in terminal:

**Check if bot is running:**
```bash
curl http://localhost:8000/health
```
Expected: `OK - MCP Q&A Bot Running`

**List all industries:**
```bash
curl http://localhost:8000/industries
```
Expected: List of banking, healthcare, saas, government, telecom

**Check an industry:**
```bash
curl http://localhost:8000/health/banking
```
Expected: Status with document counts

**Search for information:**
```bash
curl -X POST http://localhost:8000/mcp/tool/search_knowledge \
  -H "Content-Type: application/json" \
  -d '{"industry":"banking","query":"credit card dispute","top_k":2}'
```
Expected: Matching documents from knowledge base

**Detect what user wants:**
```bash
curl -X POST http://localhost:8000/mcp/tool/detect_intent \
  -H "Content-Type: application/json" \
  -d '{"industry":"banking","query":"I lost my card"}'
```
Expected: Detected intent and escalation info

## 🛠️ Available Functions

The bot can do these things:

1. **search_knowledge** - Find answers in knowledge base
2. **detect_intent** - Figure out what user needs
3. **create_ticket** - Make support tickets
4. **update_record** - Modify data
5. **send_notification** - Send messages via email/SMS/Slack

## ⚙️ Runtime Configuration (Connectors)

You can configure external connectors at runtime via environment variables (Compose or `docker run`):

- `TICKETING_ENDPOINT`: URL for ticketing system API
- `CRM_ENDPOINT`: URL for CRM integration
- `EHR_ENDPOINT`: URL for healthcare EHR system
- `OSS_BSS_ENDPOINT`: URL for telecom OSS/BSS
- `LOG_LEVEL`: Logging level (e.g., `INFO`, `DEBUG`)

These can be referenced inside action configurations using placeholders like `${TICKETING_ENDPOINT}`.



## 📂 How to Add Your Own Knowledge

1. Edit `knowledge/banking-kb.yaml` (or other industry)
2. Add documents in this format:
```yaml
documents:
  - title: "How to Report Fraud"
    content: "If you suspect fraud, call..."
  - title: "Check Balance"
    content: "To check your balance..."
```
3. Restart the bot

## ❓ Troubleshooting

**Industries list is empty?**
- Make sure you're in the `mcp-qa-bot` folder
- Check `configs/` folder exists with YAML files

**Get "Not Found" on /mcp/tool endpoints?**
- You need to use POST, not GET
- Include JSON body with parameters

**Port 8000 already in use?**
- Stop other services or edit `docker-compose.yml` port mapping

**Docker won't start?**
- Run `docker compose logs` to see errors
- Check Docker is installed: `docker --version`
- Bot persona as configurable resource

✅ **Tools**
- search_knowledge for querying documents
- detect_intent for understanding user needs
- create_ticket, update_record, send_notification for actions
- All tools accept configurable parameters

✅ **Configuration-Driven Design**
- Knowledge corpus swappable via config
- Intent taxonomy in YAML/JSON
- Action connectors configurable
- Bot persona customizable

✅ **Multi-Industry Support**
- Banking ✓
- Healthcare ✓
- SaaS ✓
- Government ✓
- Telecom ✓

## 🚧 Next Steps / Enhancements

1. **Semantic Search**: Integrate sentence-transformers for embeddings
2. **Persistence**: Add database support for tickets and records
3. **Analytics**: Track intent detection and action execution
4. **Advanced NLU**: Add intent confidence scores and multi-intent detection
5. **Workflow Orchestration**: Chain multiple actions together
6. **Approval Workflows**: Add human-in-the-loop for sensitive actions
7. **Multi-language Support**: Extend for international use
8. **Vector Database**: Integrate Pinecone/Weaviate for semantic search at scale

## 📝 License

MIT License - Built for Venture Studio Hackathon

## 🤝 Contributing

Contributions welcome! Please submit PRs with:
- Test coverage
- Documentation updates
- New industry configs as examples
