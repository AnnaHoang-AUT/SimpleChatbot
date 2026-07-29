#!/bin/bash
# SimpleChatbot - Web GUI Runner (macOS/Linux)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "========================================"
echo "  SimpleChatbot - Web GUI"
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

HOST="${FLASK_HOST:-127.0.0.1}"
PORT="${FLASK_PORT:-5000}"
URL="http://${HOST}:${PORT}"

echo ""
echo "[*] Starting web server at ${URL}"
echo "    Press Ctrl+C to stop the server."
echo ""

(sleep 2 && {
    if command -v xdg-open &> /dev/null; then
        xdg-open "$URL"
    elif command -v open &> /dev/null; then
        open "$URL"
    fi
}) &

python -m simplechatbot.web.app
