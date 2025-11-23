# YourTeacher - Production Grade

This project has been transformed from a Streamlit POC to a production-grade application using **Next.js (Frontend)** and **FastAPI (Backend)**.

## 🏗 Architecture

### Backend (FastAPI)
Follows **Clean Architecture** principles:
- **Domain Layer**: `backend/app/domain` - Entities (`StudentContext`) and Interfaces.
- **Use Cases**: `backend/app/use_cases` - Application logic (`chat_stream`).
- **Infrastructure**: `backend/app/infrastructure` - Concrete implementations (`MemorySessionRepository`, `agents`).
- **API**: `backend/app/api` - Controllers/Endpoints.

### Frontend (Next.js)
Follows **MVVM (Model-View-ViewModel)** pattern:
- **Model**: `frontend/src/types` - Data definitions.
- **View**: `frontend/src/components` & `app` - React UI components.
- **ViewModel**: `frontend/src/hooks/useChat.ts` - State management and API logic.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Gemini API Key (in `.env`)

### Running the App
Simply run the helper script:

```bash
./run_prod.sh
```

This will start:
- **Backend** on `http://localhost:8000`
- **Frontend** on `http://localhost:3000`

## 🔧 Manual Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📝 Features
- **Real-time Streaming**: SSE (Server-Sent Events) for token-by-token AI responses.
- **Multi-Agent System**: Screener -> Teacher -> Quiz handoffs.
- **Session Persistence**: State maintained across reloads (Session ID in localStorage).
- **Clean UI**: Modern interface with Tailwind CSS and Framer Motion.

