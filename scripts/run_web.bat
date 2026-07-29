@echo off
REM =============================================================================
REM SimpleChatbot - Web GUI Runner (Windows)
REM =============================================================================

cd /d "%~dp0\.."

echo ========================================
echo   SimpleChatbot - Web GUI
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

if "%FLASK_HOST%"=="" set FLASK_HOST=127.0.0.1
if "%FLASK_PORT%"=="" set FLASK_PORT=5000
set URL=http://%FLASK_HOST%:%FLASK_PORT%

echo.
echo [*] Starting web server at %URL%
echo     Press Ctrl+C to stop the server.
echo.

start "" cmd /c "timeout /t 2 /nobreak >nul && start %URL%"
python -m simplechatbot.web.app
