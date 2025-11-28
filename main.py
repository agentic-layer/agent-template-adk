import logging
import os
import warnings

from agenticlayer.agent_to_a2a import to_a2a
from agenticlayer.config import parse_sub_agents, parse_tools
from agenticlayer.otel import setup_otel
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.planners import BuiltInPlanner
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Set up ADK logging
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s"
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format=LOGGING_FORMAT)

if os.environ.get("AGENT_OTEL_ENABLED", "false").lower() == "true":
    setup_otel()

# Suppress some warnings by default - unfortunately, the experimental warnings for A2A can not be suppressed
# using the ADK environment variable alone, so we filter them here.
warnings.filterwarnings("ignore", category=UserWarning, message="\\[EXPERIMENTAL\\] .*")
os.environ.setdefault("ADK_SUPPRESS_GEMINI_LITELLM_WARNINGS", "true")
os.environ.setdefault("ADK_SUPPRESS_EXPERIMENTAL_FEATURE_WARNINGS", "true")

sub_agent, agent_tools = parse_sub_agents(os.environ.get("SUB_AGENTS", "{}"))
mcp_tools = parse_tools(os.environ.get("AGENT_TOOLS", "{}"))
tools = agent_tools + mcp_tools
root_agent = LlmAgent(
    name=os.environ.get("AGENT_NAME", "root_agent"),
    model=LiteLlm(os.environ.get("AGENT_MODEL", "gemini/gemini-2.5-flash")),
    description=os.environ.get("AGENT_DESCRIPTION", ""),
    instruction=os.environ.get("AGENT_INSTRUCTION", ""),
    sub_agents=sub_agent,
    tools=tools,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=os.environ.get("AGENT_INCLUDE_THOUGHTS", "True").lower() == "true",
            thinking_budget=int(os.environ.get("AGENT_THINKING_BUDGET", 1024)),
        )
    ),
)

# The agent url is needed for the agent card to tell other agents how to reach this agent.
# We can only guess the host and port here, as it may be set differently by Uvicorn at runtime.
# If running in k8s or similar, the host and port may also be different.
port = os.environ.get("UVICORN_PORT", 8000)
rpc_url = os.environ.get("AGENT_A2A_RPC_URL", f"http://localhost:{port}")

app = to_a2a(root_agent, rpc_url)
