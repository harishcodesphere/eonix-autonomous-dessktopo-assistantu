@echo off
echo [Eonix] Starting Backend...
cd backend
if not exist venv (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b
)
call venv\Scripts\activate
start "Eonix Backend" python main.py
cd ..
