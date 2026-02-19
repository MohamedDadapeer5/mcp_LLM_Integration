# Multi-stage build for MCP Knowledge + Action Bot

# 1) Builder: install dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# 2) Runtime: minimal image
FROM python:3.11-slim
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    CONFIG_PATH=/app/configs/banking.yaml
WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code and defaults
COPY src ./src
COPY configs ./configs
COPY knowledge ./knowledge

# Expose MCP HTTP/monitoring port
EXPOSE 8000

# Default command runs FastMCP server with industry-specific endpoints
CMD ["python", "src/fastmcp_server.py"]

# Notes for runtime configuration:
# - All 5 industries (banking, healthcare, saas, government, telecom) loaded on startup
# - Health check endpoints: /health, /health/{industry}, /industries
# - Mount volumes for hot-swappable assets:
#     -v $(pwd)/configs:/app/configs \
#     -v $(pwd)/knowledge:/app/knowledge
# - Connector endpoints/keys can be provided via env vars in action configs
# - Restart container to reload configs after changes
