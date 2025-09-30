import json
import logging
import os

from agenticlayer.agent_to_a2a import to_a2a
from agenticlayer.otel import setup_otel
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.planners import BuiltInPlanner
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.genai import types


def get_sub_agents():
    """Create sub agents from environment variable configuration."""
    sub_agents_config = os.environ.get("SUB_AGENTS", "{}")
    try:
        agents_map = json.loads(sub_agents_config)
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in SUB_AGENTS environment variable. Using empty configuration.")
        agents_map = {}

    sub_agents = []
    for agent_name, config in agents_map.items():
        if "url" not in config:
            print(f"Warning: Missing 'url' for agent '{agent_name}'. Skipping.")
            continue

        logging.info("Adding sub-agent: %s with URL: %s", agent_name, config["url"])
        sub_agents.append(RemoteA2aAgent(
            name=agent_name,
            agent_card=config["url"],
        ))

    return sub_agents

def get_tools():
    """Get tools from environment variable configuration."""
    tools_config = os.environ.get("AGENT_TOOLS", "{}")
    try:
        tools_map = json.loads(tools_config)
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in AGENT_TOOLS environment variable. Using empty configuration.")
        tools_map = {}

    tools = []
    for name, config in tools_map.items():
        if "url" not in config:
            print(f"Warning: Missing 'url' for tool '{name}'. Skipping.")
            continue

        logging.info("Adding tool: %s with URL: %s", name, config["url"])
        tools.append(McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=config["url"],
            ),
        ))

    return tools

if os.environ.get("AGENT_OTEL_ENABLED", "false").lower() == "true":
    setup_otel()

root_agent = Agent(
    name=os.environ.get("AGENT_NAME", "root_agent"),
    model=LiteLlm(os.environ.get("AGENT_MODEL", "gemini/gemini-2.5-flash")),
    description=os.environ.get("AGENT_DESCRIPTION", ""),
    instruction=os.environ.get("AGENT_INSTRUCTION", ""),
    sub_agents=get_sub_agents(),
    tools=get_tools(),
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=os.environ.get("AGENT_INCLUDE_THOUGHTS", "True").lower() == "true",
            thinking_budget=int(os.environ.get("AGENT_THINKING_BUDGET", 1024)),
        )
    ),
)


app = to_a2a(root_agent)

# Entry point for IDE to start in debug mode
# Make sure that the IDE uses the .env file
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=os.environ.get("UVICORN_HOST", "localhost"), port=int(os.environ.get("UVICORN_PORT", 8000)))
