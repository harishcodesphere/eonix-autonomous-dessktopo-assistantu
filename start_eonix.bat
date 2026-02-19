@echo off
title EONIX — Local JARVIS
color 0B
echo.
echo  ███████╗ ██████╗ ███╗  ██╗██╗██╗  ██╗
echo  ██╔════╝██╔═══██╗████╗ ██║██║╚██╗██╔╝
echo  █████╗  ██║   ██║██╔██╗██║██║ ╚███╔╝
echo  ██╔══╝  ██║   ██║██║╚████║██║ ██╔██╗
echo  ███████╗╚██████╔╝██║ ╚███║██║██╔╝╚██╗
echo  ╚══════╝ ╚═════╝ ╚═╝  ╚══╝╚═╝╚═╝  ╚═╝
echo  Your Local JARVIS — Autonomous Desktop Agent
echo ================================================
echo.

REM Check if Ollama is running
echo [1/3] Checking Ollama...
curl -s http://localhost:11434/api/tags > nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Ollama is running
) else (
    echo [!!] Ollama not running - attempting to start...
    start /B ollama serve
    timeout /t 3 /nobreak > nul
    curl -s http://localhost:11434/api/tags > nul 2>&1
    if %errorlevel% == 0 (
        echo [OK] Ollama started
    ) else (
        echo [WARN] Ollama could not start - will use Gemini only
    )
)

REM Activate virtual environment if it exists
echo [2/3] Starting EONIX backend...
cd /d "%~dp0backend"

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Start backend in background
start /B python -m uvicorn main:app --host 127.0.0.1 --port 8000 --log-level warning

REM Wait for backend to start
echo [3/3] Waiting for backend...
timeout /t 3 /nobreak > nul

REM Check if backend started
curl -s http://127.0.0.1:8000/api/health > nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Backend is running
) else (
    echo [WARN] Backend may still be starting...
)

REM Open browser
echo.
echo ================================================
echo  EONIX is running at: http://127.0.0.1:8000
echo  Close this window to stop EONIX
echo ================================================
echo.
start http://127.0.0.1:8000

pause
