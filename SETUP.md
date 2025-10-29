# 🚀 YourTeacher - Setup Guide

Complete setup guide for the Next.js + FastAPI production-grade application.

## 📋 Prerequisites

-   **Python 3.12+** (for backend)
-   **Node.js 18+** (for frontend)
-   **Gemini API Key** or OpenAI API Key

## 🔧 Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Start Backend Server

```bash
# From backend directory
python -m app.main

# Or with uvicorn directly:
uvicorn app.main:app --reload --port 8000
```

The backend will start at:

-   **API**: http://localhost:8000
-   **Docs**: http://localhost:8000/docs
-   **WebSocket**: ws://localhost:8000/api/ws/{session_id}

## 🎨 Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Environment Configuration

The `.env.local` file is already configured for local development:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### 4. Start Frontend Development Server

```bash
npm run dev
```

The frontend will start at http://localhost:3000

## 🎯 Quick Start (Both Services)

### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - Backend:**

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m app.main
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

### Option 2: Using Scripts (Coming Soon)

Create a startup script for your convenience:

**start.sh (macOS/Linux):**

```bash
#!/bin/bash

# Start backend
cd backend
source venv/bin/activate
python -m app.main &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
```

**start.bat (Windows):**

```batch
@echo off

start cmd /k "cd backend && venv\Scripts\activate && python -m app.main"
start cmd /k "cd frontend && npm run dev"

echo Both services started in separate windows
```

## 🧪 Testing the Setup

1. **Check Backend Health:**

```bash
curl http://localhost:8000/api/health
```

Expected response:

```json
{
	"status": "healthy",
	"service": "YourTeacher API",
	"active_sessions": 0
}
```

2. **Open Frontend:**
   Visit http://localhost:3000 in your browser

3. **Test the Flow:**
    - The app should automatically create a session
    - Start chatting with the Student Screener Agent
    - Follow the assessment, teaching, and quiz flow

## 🔍 Troubleshooting

### Backend Issues

**Port already in use:**

```bash
# Change port in backend/.env
BACKEND_PORT=8001

# Or kill the process using port 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**API Key errors:**

-   Verify your `.env` file has `GEMINI_API_KEY` set
-   Check that the key is valid
-   Ensure no extra spaces or quotes

**Import errors:**

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Port 3000 already in use:**

```bash
# Next.js will automatically suggest 3001
# Or specify a different port:
npm run dev -- -p 3001
```

**Connection to backend fails:**

-   Ensure backend is running on port 8000
-   Check CORS settings in backend config
-   Verify `.env.local` has correct URLs

**Build errors:**

```bash
# Clear Next.js cache
rm -rf .next
rm -rf node_modules
npm install
```

### WebSocket Issues

**Connection refused:**

-   Ensure backend WebSocket endpoint is accessible
-   Check firewall settings
-   Verify session ID is valid

**Disconnections:**

-   Check network stability
-   Backend logs for errors
-   Frontend console for WebSocket errors

## 📦 Production Build

### Backend

```bash
cd backend
pip install -r requirements.txt
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

```bash
cd frontend
npm run build
npm start
```

## 🐳 Docker (Optional)

### Backend Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "app.main"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: "3.8"

services:
    backend:
        build: ./backend
        ports:
            - "8000:8000"
        environment:
            - GEMINI_API_KEY=${GEMINI_API_KEY}

    frontend:
        build: ./frontend
        ports:
            - "3000:3000"
        environment:
            - NEXT_PUBLIC_API_URL=http://localhost:8000
            - NEXT_PUBLIC_WS_URL=ws://localhost:8000
        depends_on:
            - backend
```

## 🔒 Security Checklist

-   [ ] API keys stored in `.env` files (not committed)
-   [ ] `.env` files added to `.gitignore`
-   [ ] CORS origins properly configured
-   [ ] WebSocket authentication (if needed)
-   [ ] Rate limiting configured (production)
-   [ ] HTTPS enabled (production)

## 📚 Additional Resources

-   [Backend API Documentation](http://localhost:8000/docs)
-   [Frontend README](frontend/README.md)
-   [Backend README](backend/README.md)
-   [Implementation Plan](IMPLEMENTATION_PLAN.md)

## 💡 Tips

1. **Development Workflow:**

    - Keep both terminals open
    - Watch for errors in both services
    - Use backend API docs for testing endpoints

2. **Debugging:**

    - Backend logs show agent interactions
    - Frontend console shows WebSocket events
    - Use browser DevTools Network tab

3. **Performance:**
    - Backend: Use async operations
    - Frontend: Optimize re-renders
    - Monitor WebSocket message sizes

## ✅ Success Checklist

-   [ ] Backend starts without errors
-   [ ] Frontend loads successfully
-   [ ] Session automatically created
-   [ ] Chat interface displays
-   [ ] Messages send and receive
-   [ ] Streaming works in real-time
-   [ ] Agent handoffs function
-   [ ] Progress tracking updates
-   [ ] Student profile displays correctly
-   [ ] Quiz scoring works

## 🎉 You're Ready!

Open http://localhost:3000 and start your personalized learning journey!

For questions or issues, refer to the documentation or check the logs.
