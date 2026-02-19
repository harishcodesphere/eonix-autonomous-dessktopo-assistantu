@echo off
echo [Eonix] Launching System...

start "" scripts\start_backend.bat
timeout /t 5 /nobreak >nul
start "" scripts\start_frontend.bat

echo [Eonix] Both services launched.
