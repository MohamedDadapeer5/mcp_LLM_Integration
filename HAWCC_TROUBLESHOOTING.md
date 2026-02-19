# HAWCC Platform Troubleshooting Guide

## Issue: FileNotFoundError for Knowledge Base Files

### Problem
```
FileNotFoundError: [Errno 2] No such file or directory: 'configs/../knowledge/healthcare-kb.yaml'
```

### Solution
The server now properly resolves relative paths across platforms. Make sure you:

1. **Run from the project root directory:**
   ```bash
   cd mcp-qa-bot
   python src/server.py configs/healthcare.yaml
   ```

2. **Verify all files exist:**
   ```bash
   python verify_setup.py
   ```

3. **Check directory structure:**
   ```
   mcp-qa-bot/
   ├── src/
   │   └── server.py
   ├── configs/
   │   ├── banking.yaml
   │   ├── healthcare.yaml
   │   └── ...
   └── knowledge/
       ├── banking-kb.yaml
       ├── healthcare-kb.yaml
       └── ...
   ```

### Fixed in Latest Version
- ✅ Path resolution now uses `Path.resolve()` for cross-platform compatibility
- ✅ Handles both absolute and relative paths correctly
- ✅ Better error messages showing troubleshooting steps
- ✅ Works with `../` path navigation in config files

## Testing Each Industry Config

### Banking
```bash
python src/server.py configs/banking.yaml
```

### Healthcare
```bash
python src/server.py configs/healthcare.yaml
```

### SaaS
```bash
python src/server.py configs/saas.yaml
```

### Government
```bash
python src/server.py configs/government.yaml
```

### Telecom
```bash
python src/server.py configs/telecom.yaml
```

## Expected Startup Output

When the server starts correctly, you should see:

```
======================================================================
  MCP Knowledge-Powered Q&A and Action Bot Server
  Venture Studio Hackathon - Challenge 1
======================================================================

📂 Loading configuration: /path/to/configs/healthcare.yaml
✅ Configuration loaded successfully
🏢 Industry: healthcare
🤖 Persona: empathetic
📚 Knowledge Base: 6 documents
🎯 Intents: 6 defined
⚡ Actions: 4 configured
🔍 Search Type: hybrid

======================================================================
🚀 MCP Server Starting...
======================================================================

ℹ️  Server Status: RUNNING
ℹ️  Transport: stdio (MCP protocol via standard input/output)
ℹ️  Waiting for MCP client connections...

📌 Resources Available:
   • knowledge://all - Searchable knowledge base
   • intents://all - Intent taxonomy
   • actions://all - Action connectors
   • persona://config - Bot personality

🛠️  Tools Available:
   • search_knowledge(query, top_k)
   • detect_intent(query)
   • create_ticket(subject, description, priority, category)
   • update_record(record_id, fields)
   • send_notification(channel, recipient, message)
```

## Still Having Issues?

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Verify file permissions:**
   Make sure you have read access to all config and knowledge files

4. **Run verification script:**
   ```bash
   python verify_setup.py
   ```

5. **Check for typos:**
   Ensure config file paths match exactly (case-sensitive on some platforms)

## Contact
If issues persist, include the full error output and the result of:
```bash
python verify_setup.py
ls -la configs/
ls -la knowledge/
```
