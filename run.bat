@echo off

echo Starting the application...

REM Get the current directory of the batch file itself
set "BAT_DIR=%~dp0"

REM Define paths to Backend and Frontend based on the script's location
set "BACKEND_DIR=%BAT_DIR%Backend"
set "FRONTEND_DIR=%BAT_DIR%Frontend"

REM Check if backend directory exists
if not exist "%BACKEND_DIR%" (
    echo ERROR: Backend directory not found at "%BACKEND_DIR%"
    exit /b 1
)

REM Check if frontend directory exists
if not exist "%FRONTEND_DIR%" (
    echo ERROR: Frontend directory not found at "%FRONTEND_DIR%"
    exit /b 1
)

REM Run the Python script in the backend folder in parallel
start /d "%BACKEND_DIR%" python Main.py

REM Wait for 3 seconds to ensure the Python script starts
timeout /t 3 /nobreak > nul

REM Run Node.js (Vite) script in the frontend folder
start /d "%FRONTEND_DIR%" npm run dev

echo Local: http://localhost:5173/

REM Kill the calling terminal
exit
