@echo off
REM YourTeacher Development Startup Script for Windows

echo ========================================
echo Starting YourTeacher Development Environment
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.12 or higher
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    echo Please install Node.js 18 or higher
    pause
    exit /b 1
)

REM Start Backend
echo.
echo Starting Backend (FastAPI)...
start "YourTeacher Backend" cmd /k "cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python -m app.main"

REM Wait a few seconds for backend to start
timeout /t 5 /nobreak >nul

REM Start Frontend
echo.
echo Starting Frontend (Next.js)...
start "YourTeacher Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ========================================
echo YourTeacher is starting...
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend:     http://localhost:3000
echo.
echo Both services are running in separate windows.
echo Close the command windows to stop the services.
echo.
pause

