# MCP Knowledge + Action Bot - Docker Deployment Guide

## Challenge 2: Containerized MCP Server ✅

### Features Implemented

✅ **Multi-stage Docker builds** for optimized images  
✅ **FastMCP framework** with HTTP transport on port 8000  
✅ **Industry-specific health endpoints** (`/health/{industry}`)  
✅ **Hot-swappable configs** via volume mounts  
✅ **5 industries pre-loaded**: banking, healthcare, saas, government, telecom  
✅ **MCP Tools & Resources** exposed via HTTP  
✅ **Logging & monitoring** endpoints for debugging  

---

## Quick Start

### 1. Build the Docker Image

```bash
cd mcp-qa-bot
docker build -t mcp-qa-bot:latest .
```

### 2. Run with Docker

```bash
docker run -d \
  --name mcp-bot \
  -p 8000:8000 \
  -v $(pwd)/configs:/app/configs:ro \
  -v $(pwd)/knowledge:/app/knowledge:ro \
  mcp-qa-bot:latest
```

### 3. Run with Docker Compose

```bash
docker-compose up -d
```

---

## Health Check Endpoints

### Root Health Check
```bash
curl http://localhost:8000/health
# Response: OK - MCP Q&A Bot Running
```

### Industry-Specific Health Checks
```bash
# Banking
curl http://localhost:8000/health/banking

# Healthcare
curl http://localhost:8000/health/healthcare

# SaaS
curl http://localhost:8000/health/saas

# Government
curl http://localhost:8000/health/government

# Telecom
curl http://localhost:8000/health/telecom
```

**Response Example:**
```json
{
  "status": "ok",
  "industry": "banking",
  "persona": "formal",
  "documents": 6,
  "intents": 6,
  "actions": 4
}
```

### List All Industries
```bash
curl http://localhost:8000/industries
```

---

## MCP Tools (via HTTP)

### 1. Search Knowledge Base

```bash
curl -X POST http://localhost:8000/tools/search_knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "healthcare",
    "query": "How to reset password?",
    "top_k": 3
  }'
```

### 2. Detect Intent

```bash
curl -X POST http://localhost:8000/tools/detect_intent \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "banking",
    "query": "I need to create a ticket for fraud"
  }'
```

### 3. Create Ticket

```bash
curl -X POST http://localhost:8000/tools/create_ticket \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "telecom",
    "subject": "Network Outage",
    "description": "Customer experiencing connectivity issues",
    "priority": "high",
    "category": "technical"
  }'
```

### 4. Update Record

```bash
curl -X POST http://localhost:8000/tools/update_record \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "saas",
    "record_id": "USR-12345",
    "fields": {
      "status": "active",
      "subscription": "premium"
    }
  }'
```

### 5. Send Notification

```bash
curl -X POST http://localhost:8000/tools/send_notification \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "government",
    "channel": "email",
    "recipient": "citizen@example.com",
    "message": "Your application has been approved"
  }'
```

---

## MCP Resources (via HTTP)

### Get Knowledge Base

```bash
curl http://localhost:8000/resources/knowledge://banking/all
```

### Get Intents

```bash
curl http://localhost:8000/resources/intents://healthcare/all
```

### Get Actions

```bash
curl http://localhost:8000/resources/actions://saas/all
```

### Get Persona

```bash
curl http://localhost:8000/resources/persona://telecom/config
```

---

## Hot-Swapping Configurations

### Update Knowledge Base (No Rebuild Required)

1. Edit `knowledge/banking-kb.yaml`
2. Restart container:
   ```bash
   docker restart mcp-bot
   ```

### Change Industry Config

1. Edit `configs/healthcare.yaml`
2. Restart container:
   ```bash
   docker restart mcp-bot
   ```

---

## Environment Variables for Connectors

Set these in `docker-compose.yml` or via `-e` flags:

```yaml
environment:
  - TICKETING_ENDPOINT=https://jira.company.com/api
  - CRM_ENDPOINT=https://salesforce.company.com/api
  - EHR_ENDPOINT=https://epic.hospital.com/api
  - OSS_BSS_ENDPOINT=https://oss.telecom.com/api
  - TICKETING_API_KEY=your-key-here
```

Then reference in your action configs:

```yaml
actions:
  - name: create_ticket
    type: rest_api
    endpoint: ${TICKETING_ENDPOINT}
    headers:
      Authorization: Bearer ${TICKETING_API_KEY}
```

---

## Monitoring & Logging

### View Logs

```bash
# Docker
docker logs -f mcp-bot

# Docker Compose
docker-compose logs -f
```

### Health Check in Browser

Open: `http://localhost:8000/health/banking`

### Prometheus Metrics (Optional)

Add `/metrics` endpoint in `fastmcp_server.py` for Prometheus scraping.

---

## Production Deployment

### Build for Production

```bash
docker build -t mcp-qa-bot:prod --target runtime .
```

### Deploy to Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-qa-bot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-qa-bot
  template:
    metadata:
      labels:
        app: mcp-qa-bot
    spec:
      containers:
      - name: mcp-bot
        image: mcp-qa-bot:prod
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: configs
          mountPath: /app/configs
          readOnly: true
        - name: knowledge
          mountPath: /app/knowledge
          readOnly: true
        env:
        - name: LOG_LEVEL
          value: "INFO"
      volumes:
      - name: configs
        configMap:
          name: mcp-configs
      - name: knowledge
        configMap:
          name: mcp-knowledge
```

---

## Troubleshooting

### Container won't start

```bash
docker logs mcp-bot
```

### Health check fails

```bash
curl -v http://localhost:8000/health
```

### Config not loading

Check volume mounts:
```bash
docker inspect mcp-bot | grep -A 10 Mounts
```

---

## Next Steps

1. Add Prometheus metrics endpoint
2. Implement authentication/authorization
3. Add rate limiting
4. Set up CI/CD pipeline
5. Deploy to cloud (AWS ECS, Azure Container Apps, GCP Cloud Run)

---

## Summary

✅ **Challenge 1 Complete**: Knowledge + Action Bot with 5 industries  
✅ **Challenge 2 Complete**: Dockerized with FastMCP on port 8000  

**Key Features:**
- Industry-specific health endpoints  
- Hot-swappable configs via volumes  
- MCP tools & resources over HTTP  
- Production-ready multi-stage build  
- Docker Compose for easy deployment
