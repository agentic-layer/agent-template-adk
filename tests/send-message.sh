#!/bin/bash

# Send message to an agent via A2A protocol

set -euo pipefail

# Configuration
A2A_RPC_URL="${A2A_RPC_URL:-http://localhost:8001}"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Install with 'brew install jq' for formatted output."
    exit 1
fi

# Function to test Agent Gateway (A2A protocol)
send_message() {
    local message="$1"

    # Generate a random message ID and context ID
    MESSAGE_ID=$(uuidgen 2>/dev/null || echo "$(date +%s)-$RANDOM")
    CONTEXT_ID=$(uuidgen 2>/dev/null || echo "$(date +%s)-$RANDOM")

    curl -vfs "${A2A_RPC_URL}" \
        -H "Content-Type: application/json" \
        -d "$(jq -n --arg message "$message" --arg msg_id "$MESSAGE_ID" --arg ctx_id "$CONTEXT_ID" '{
            "jsonrpc": "2.0",
            "id": 1,
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [
                        {
                            "kind": "text",
                            "text": $message
                        }
                    ],
                    "messageId": $msg_id,
                    "contextId": $ctx_id
                },
                "metadata": {}
            }
        }')" | jq
}

send_message "$1"
