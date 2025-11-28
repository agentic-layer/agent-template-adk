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

For detailed configuration of sub-agents and MCP tools, refer to the [Agentic Layer SDK](https://github.com/agentic-layer/sdk-python/blob/main/adk/README.md#configuration)

## Usage

You can use the prebuild docker images like this:

```shell
docker run \
  -e AGENT_NAME="my_helper" \
  -e AGENT_DESCRIPTION="A helpful assistant agent" \
  -e AGENT_INSTRUCTION="You are a helpful assistant" \
  -p 8000:8000 \
  ghcr.io/agentic-layer/agent-template-adk:latest
```

## Development and Testing

Create a `.env` file based on the provided `.env.example` to store your secrets (e.g., API keys)
and configuration.

There are multiple agents available in the [tests/agents](tests/agents) folder for testing purposes.
They can be run all together in Docker Compose or individually via Python for debugging.
Combining both methods is not recommended for the agents, as the URLs have to be adjusted accordingly.

If you want to test the Python SDK (https://github.com/agentic-layer/sdk-python/tree/main/adk),
you can include a local copy in the build, see [pyproject.toml](pyproject.toml).
This will not work with Docker, as the docker build process cannot access local files outside the build context.


### Run with Python

Run the agents in the following order due to dependencies.
Look into [tests/run-agent.sh](tests/run-agent.sh) for details on launching an agent in your IDE for debugging.

```shell
# Run Analyzer agent (no further dependencies)
./tests/run-agent.sh analyzer
```
```shell
# Start an MCP tool server for testing
docker compose up mcp-fetch
```
```shell
# Run data gatherer agent (depends on the MCP tool server)
./tests/run-agent.sh data-gatherer
```
```shell
# Run research coordinator agent (depends on both the data gatherer and analyzer agents)
./tests/run-agent.sh research-coordinator
```

### Run with Docker

```shell
docker compose up --build
```

### Send message to the agent
The root agent will be available at `http://localhost:8001` and will expose an Agent Card at 
`http://localhost:8001/.well-known/agent-card.json`.

Ask the agent a question:

```shell
./tests/send-message.sh "Where does the statement 'What is the meaning of life? - 42' originate from?"
```

You can also send messages to other agents:

```shell
A2A_RPC_URL="http://localhost:8003" ./tests/send-message.sh "Please analyze the sentiment of the following text: 'I love programming!'"
```
