#!/bin/bash

echo "🚀 Starting YourTeacher Production Setup..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Please install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "📦 Syncing backend dependencies..."
cd backend
uv sync
cd ..

# Start Backend
echo "🐍 Starting FastAPI Backend..."
cd backend
uv run python -m app.main &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "⚛️  Starting Next.js Frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ System Running!"
echo "   Backend: http://localhost:8000/docs"
echo "   Frontend: http://localhost:3000"
echo ""
echo "Press CTRL+C to stop both services."

trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT
wait

