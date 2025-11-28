#!/usr/bin/env bash

# Run an agent with a specified environment file.
# It will also use the default .env file for picking up common configuration like API keys.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

agent_name="${1}"

cd "${SCRIPT_DIR}/.."
uv run --env-file "${SCRIPT_DIR}/agents/${agent_name}.env" uvicorn main:app
