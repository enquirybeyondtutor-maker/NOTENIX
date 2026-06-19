@echo off
echo Starting Notenix Backend...
cd /d "%~dp0backend"

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Installing dependencies...
.venv\Scripts\pip.exe install -r requirements.txt -q

echo.
echo Backend running at http://localhost:8000
echo API Docs at http://localhost:8000/docs
echo.
.venv\Scripts\uvicorn.exe main:app --reload --host 0.0.0.0 --port 8000
pause
