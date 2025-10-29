#!/bin/bash

# YourTeacher Development Startup Script
# This script starts both backend and frontend in development mode

echo "🎓 Starting YourTeacher Development Environment"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.12+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Start backend
echo ""
echo "🔧 Starting Backend (FastAPI)..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/installed.txt" ]; then
    echo "📦 Installing backend dependencies..."
    pip install -r requirements.txt
    touch venv/installed.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found in backend directory"
    echo "Please create a .env file with your GEMINI_API_KEY"
    echo "Copying .env.example to .env..."
    cp .env.example .env || cp ../.env backend/.env 2>/dev/null || true
fi

# Start backend in background
echo "✅ Starting FastAPI server on port 8000..."
python -m app.main &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

cd ..

# Start frontend
echo ""
echo "🎨 Starting Frontend (Next.js)..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Start frontend in background
echo "✅ Starting Next.js dev server on port 3000..."
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

cd ..

# Print access information
echo ""
echo "================================================"
echo "✅ YourTeacher is now running!"
echo "================================================"
echo ""
echo "📡 Backend API:  http://localhost:8000"
echo "📚 API Docs:     http://localhost:8000/docs"
echo "🌐 Frontend:     http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup INT TERM

# Wait for user to press Ctrl+C
wait

