@echo off
title UniEvent - University Event Management Platform
echo ========================================================
echo Starting UniEvent Platform (FastAPI + React TypeScript)...
echo ========================================================

cd /d "%~dp0backend"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo [1/2] Database check: SQLite events.db ready.
echo [2/2] Launching server on http://localhost:8000...
echo.
echo Opening browser at http://localhost:8000
start http://localhost:8000
echo.
echo Press CTRL+C to stop the server anytime.
echo.

".venv\Scripts\python.exe" -m uvicorn main:app --reload --port 8000
pause
