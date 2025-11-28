# agent-template-adk

A template for building configurable AI agents using Google's Agent Development Kit (ADK). 
This template allows you to create agents with customizable system prompts, sub-agents, 
and MCP (Model Context Protocol) tools through environment variables, 
making it easy to deploy different agent configurations without code changes.

It is based on https://github.com/agentic-layer/sdk-python.

## Features

- **Environment-based Configuration**: Configure agents, tools, and system prompts via environment variables
- **Sub-Agent Support**: Connect to remote A2A (Agent-to-Agent) agents
- **MCP Tool Integration**: Add external tools via MCP protocol
- **Multi-Model Support**: Use various LLM providers through LiteLLM
- **Docker Ready**: Multi-platform Docker support for easy deployment

## Environment Configuration

Available environment variables:

| Variable                 | Description                              | Default                   | Example                                                                                                        |
|--------------------------|------------------------------------------|---------------------------|----------------------------------------------------------------------------------------------------------------|
| `AGENT_NAME`             | Name of the root agent                   | -                         | `my_helper`                                                                                                    |
| `AGENT_DESCRIPTION`      | Agent description                        | -                         | `A helpful assistant agent`                                                                                    |
| `AGENT_INSTRUCTION`      | Agent system instruction                 | -                         | `You are a helpful assistant`                                                                                  |
| `AGENT_MODEL`            | LLM model to use                         | `gemini/gemini-2.5-flash` | `gemini/gemini-2.0-flash`                                                                                      |
| `SUB_AGENTS`             | JSON configuration for sub-agents        | `{}`                      | `{"weather_agent":{"url":"http://localhost:8002/.well-known/agent-card.json","interaction_type":"tool_call"}}` |
| `AGENT_TOOLS`            | JSON configuration for MCP tools         | `{}`                      | `{"web_fetch":{"url":"https://remote.mcpservers.org/fetch/mcp"}}`                                              |
| `AGENT_A2A_RPC_URL`      | RPC URL inserted into the A2A agent card | `None`                    | `https://my-agent.example.com/a2a`                                                                             |
| `AGENT_OTEL_ENABLED`     | Enable OpenTelemetry                     | `false`                   | `true`                                                                                                         |
| `AGENT_INCLUDE_THOUGHTS` | Include agent thoughts in responses      | `true`                    | `false`                                                                                                        |
| `AGENT_THINKING_BUDGET`  | Max tokens for LLM responses             | `1024`                    | `2048`                                                                                                         |

## Usage

Create a `.env` file based on the provided `.env.example` to store your secrets (e.g., API keys)
and configuration.

### Run with Python

```shell
make run
```

### Run with Docker

```shell
make docker-run
```

### Send message to the agent
The agent will be available at `http://localhost:8001` and will expose an Agent Card at 
`http://localhost:8001/.well-known/agent-card.json`.

Ask the agent a question:

```shell
./scripts/send_message.sh "What is the purpose of life?"
```