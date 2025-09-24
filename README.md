# agent-template-adk

A template for building configurable AI agents using Google's Agent Development Kit (ADK). This template allows you to create agents with customizable system prompts, sub-agents, and MCP (Model Context Protocol) tools through environment variables, making it easy to deploy different agent configurations without code changes.

## Features

- **Environment-based Configuration**: Configure agents, tools, and system prompts via environment variables
- **Sub-Agent Support**: Connect to remote A2A (Agent-to-Agent) agents
- **MCP Tool Integration**: Add external tools via MCP protocol
- **Multi-Model Support**: Use various LLM providers through LiteLLM
- **Docker Ready**: Multi-platform Docker support for easy deployment

## Environment Configuration

Create `.env` for secrets and common variables:
```shell
# .env (for secrets and common config)
GOOGLE_API_KEY=your-api-key-here
LOGLEVEL=DEBUG
```

Pass agent-specific configuration via `-e` flags when running Docker. Available environment variables:
- `AGENT_NAME`: Name of the root agent
- `AGENT_DESCRIPTION`: Agent description
- `AGENT_INSTRUCTION`: Agent system instruction
- `AGENT_MODEL`: LLM model to use (default: "gemini/gemini-2.5-flash")
- `SUB_AGENTS`: JSON configuration for sub-agents
- `AGENT_TOOLS`: JSON configuration for MCP tools
- `A2A_AGENT_CARD_URL`: URL for the agent's own Agent Card
- `AGENT_OTEL_ENABLED`: Enable OpenTelemetry (default: "false")

## Quick Start with Docker

1. **Set up your environment:**
```shell
cp .env.example .env
# Edit .env with your secrets (like GOOGLE_API_KEY)
```

2. **(Optional) Build the Docker image:**
```shell
make docker-build
```

3. **Run with Docker (basic example):**
```shell
docker run --rm -it -p 8000:8000 \
  -e AGENT_NAME="my_helper" \
  -e AGENT_DESCRIPTION="A helpful assistant agent" \
  -e AGENT_INSTRUCTION="You are a helpful assistant that can answer questions and help with tasks." \
  -e AGENT_MODEL="gemini/gemini-2.0-flash" \
  -e A2A_AGENT_CARD_URL="http://localhost:8000/.well-known/agent-card.json" \
  --env-file .env \
  ghcr.io/agentic-layer/agent-template-adk
```

4. **Run with sub-agents and tools:**
```shell
docker run --rm -it -p 8000:8000 \
  -e AGENT_NAME="research_agent" \
  -e AGENT_DESCRIPTION="A research-focused agent with tools" \
  -e AGENT_INSTRUCTION="You are a research assistant that can search the web and analyze documents." \
  -e SUB_AGENTS='{"example_agent":{"url":"https://example.com/.well-known/agent-card.json"}}' \
  -e AGENT_TOOLS='{"web_fetch":{"url":"https://remote.mcpservers.org/fetch/mcp"}}' \
  -e A2A_AGENT_CARD_URL="http://localhost:8000/.well-known/agent-card.json" \
  --env-file .env \
  ghcr.io/agentic-layer/agent-template-adk
```

5. **Access your agent:**
The agent will be available at `http://localhost:8000` and will expose an Agent Card at `/.well-known/agent-card.json`.

Ask the agent a question using curl:
```shell
curl http://localhost:8000/ \
    -H "Content-Type: application/json" \
    -d '{
      "jsonrpc": "2.0",
      "id": 1,
      "method": "message/send",
      "params": {
        "message": {
          "role": "user",
          "parts": [
            {
              "kind": "text",
              "text": "Whats the purpose of life?"
            }
          ],
          "messageId": "9229e770-767c-417b-a0b0-f0741243c589",
          "contextId": "abcd1234-5678-90ab-cdef-1234567890ab"
        },
        "metadata": {}
      }
    }' | jq
```