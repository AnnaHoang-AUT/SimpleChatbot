@echo off
REM =============================================================================
REM SimpleChatbot - CLI Runner (Windows)
REM =============================================================================

cd /d "%~dp0\.."

echo ========================================
echo   SimpleChatbot - CLI Interface
echo ========================================
echo.

if not exist ".venv" (
    echo [*] Creating virtual environment...
    python -m venv .venv
)

echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [*] Installing dependencies...
pip install -e . --quiet

if not exist ".env" (
    if exist ".env.example" (
        echo [*] Creating .env from .env.example...
        copy .env.example .env >nul
    )
)

echo.
echo [*] Starting CLI chatbot...
echo     Type 'quit' or 'exit' to end the conversation.
echo.

python -m simplechatbot.cli
