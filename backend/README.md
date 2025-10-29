# YourTeacher Backend - FastAPI

Production-grade backend API for the YourTeacher personalized learning system.

## 🚀 Features

-   **FastAPI Framework**: High-performance async API
-   **Real-time Streaming**: WebSocket support for token-by-token responses
-   **Multi-Agent System**: Three specialized AI agents with seamless handoffs
-   **Session Management**: Stateful learning sessions
-   **OpenAI Agents SDK**: Advanced agent orchestration
-   **Gemini API Integration**: Powered by Google's Gemini 2.0 Flash

## 📋 Requirements

-   Python 3.12+
-   Gemini API Key (or OpenAI API Key)

## 🔧 Installation

1. **Navigate to backend directory:**

```bash
cd backend
```

2. **Create virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment:**

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## ▶️ Running the Server

**Development mode:**

```bash
python -m app.main
```

**Or with uvicorn directly:**

```bash
uvicorn app.main:app --reload --port 8000
```

The server will start at:

-   API: http://localhost:8000
-   Docs: http://localhost:8000/docs
-   WebSocket: ws://localhost:8000/api/ws/{session_id}

## 📡 API Endpoints

### REST API

-   `POST /api/session/start` - Create new learning session
-   `GET /api/session/{session_id}` - Get session state
-   `POST /api/session/{session_id}/reset` - Reset session
-   `DELETE /api/session/{session_id}` - Delete session
-   `GET /api/health` - Health check

### WebSocket

-   `WS /api/ws/{session_id}` - Real-time streaming endpoint

## 🔌 WebSocket Protocol

**Client → Server:**

```json
{
	"type": "message",
	"content": "User message here"
}
```

**Server → Client:**

```json
{
  "type": "token" | "agent_update" | "tool_call" | "handoff" | "complete",
  "data": {...},
  "timestamp": "ISO8601"
}
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models/              # Data models
│   │   ├── context.py       # Learning context
│   │   ├── requests.py      # API requests
│   │   └── responses.py     # API responses
│   ├── agents/              # Agent system
│   │   ├── agents.py        # Agent definitions
│   │   └── tools.py         # Agent tools
│   ├── services/            # Business logic
│   │   ├── session_service.py
│   │   └── agent_service.py
│   └── api/                 # API routes
│       ├── routes.py        # REST endpoints
│       └── websocket.py     # WebSocket endpoint
├── requirements.txt
└── README.md
```

## 🧪 Testing

**Test the API:**

```bash
curl http://localhost:8000/api/health
```

**Create a session:**

```bash
curl -X POST http://localhost:8000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"initial_message": "Hello!"}'
```

## 🔒 Environment Variables

-   `GEMINI_API_KEY` - Your Gemini API key (required)
-   `BACKEND_PORT` - Port to run server on (default: 8000)
-   `CORS_ORIGINS` - Allowed CORS origins (comma-separated)

## 📚 Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## 🐛 Troubleshooting

**Import errors:**

-   Ensure you're in the backend directory
-   Check that all dependencies are installed

**API key errors:**

-   Verify your .env file has GEMINI_API_KEY set
-   Check that the key is valid

**WebSocket connection issues:**

-   Ensure session exists before connecting
-   Check CORS settings for your frontend origin

## 🤝 Development

The backend uses:

-   **FastAPI** for API framework
-   **Pydantic** for data validation
-   **OpenAI Agents SDK** for agent orchestration
-   **WebSockets** for real-time streaming
-   **AsyncIO** for asynchronous operations

## 📄 License

MIT License - see main project LICENSE file
