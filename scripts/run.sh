#!/bin/bash
# SimpleChatbot - CLI Runner (macOS/Linux)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "========================================"
echo "  SimpleChatbot - CLI Interface"
echo "========================================"
echo ""

if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv .venv
fi

echo "[*] Activating virtual environment..."
source .venv/bin/activate

echo "[*] Installing dependencies..."
pip install -e . --quiet

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "[*] Creating .env from .env.example..."
    cp .env.example .env
fi

echo ""
echo "[*] Starting CLI chatbot..."
echo "    Type 'quit' or 'exit' to end the conversation."
echo ""

python -m simplechatbot.cli
