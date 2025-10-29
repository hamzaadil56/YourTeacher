# 🏗️ YourTeacher Architecture Documentation

## 📐 System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                           User Browser                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            Next.js Frontend (Port 3000)                   │   │
│  │  • React Components                                       │   │
│  │  • TypeScript                                            │   │
│  │  • Tailwind CSS + shadcn/ui                             │   │
│  │  • WebSocket Client                                      │   │
│  └────────────┬──────────────────────────┬──────────────────┘   │
└───────────────┼──────────────────────────┼──────────────────────┘
                │                          │
                │ HTTP/REST                │ WebSocket
                │                          │
┌───────────────▼──────────────────────────▼──────────────────────┐
│              FastAPI Backend (Port 8000)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    API Layer                              │   │
│  │  • REST Endpoints (routes.py)                            │   │
│  │  • WebSocket Handler (websocket.py)                      │   │
│  └───────────────────────┬──────────────────────────────────┘   │
│                          │                                       │
│  ┌───────────────────────▼──────────────────────────────────┐   │
│  │                 Service Layer                             │   │
│  │  • AgentStreamingService                                 │   │
│  │  • SessionService                                        │   │
│  └───────────────────────┬──────────────────────────────────┘   │
│                          │                                       │
│  ┌───────────────────────▼──────────────────────────────────┐   │
│  │                  Agent System                             │   │
│  │  • Student Screener Agent                                │   │
│  │  • Teaching Agent                                        │   │
│  │  • Quiz Agent                                            │   │
│  │  • Tools (cognitive assessment, content gen, etc.)       │   │
│  └───────────────────────┬──────────────────────────────────┘   │
│                          │                                       │
│  ┌───────────────────────▼──────────────────────────────────┐   │
│  │              OpenAI Agents SDK                            │   │
│  │  • Agent Orchestration                                   │   │
│  │  • Streaming Support                                     │   │
│  │  • Handoff Management                                    │   │
│  └───────────────────────┬──────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────-┘
                          │
                          │
┌───────────────────────▼──────────────────────────────────────┐
│                   External APIs                               │
│  • Gemini API (Google)                                       │
│  • OpenAI API (Alternative)                                  │
└──────────────────────────────────────────────────────────────┘
```

## 🔧 Backend Architecture (FastAPI)

### Layer Structure

```
backend/app/
├── main.py                    # Application entry point
├── config.py                  # Configuration management
│
├── models/                    # Data models (Pydantic)
│   ├── context.py            # StudentLearningContext
│   ├── requests.py           # API request schemas
│   └── responses.py          # API response schemas
│
├── api/                      # API endpoints
│   ├── routes.py             # REST API routes
│   └── websocket.py          # WebSocket handler
│
├── services/                 # Business logic
│   ├── session_service.py    # Session management
│   └── agent_service.py      # Agent orchestration
│
└── agents/                   # Agent system
    ├── agents.py             # Agent definitions
    └── tools.py              # Agent tools
```

### Request Flow

1. **HTTP Request** → FastAPI Router → Service Layer → Response
2. **WebSocket** → Connection → Message Loop → Stream Events

### Data Flow

```
User Message
    ↓
WebSocket Endpoint (websocket.py)
    ↓
AgentStreamingService.process_message_stream()
    ↓
Runner.run_streamed() [OpenAI Agents SDK]
    ↓
Agent → Tools → LLM → Streaming Response
    ↓
Stream Events (token, tool_call, handoff, etc.)
    ↓
WebSocket → Frontend
```

## 🎨 Frontend Architecture (Next.js)

### Component Hierarchy

```
App (layout.tsx)
├── SessionProvider (Context)
│   └── Main Page (page.tsx)
│       ├── Header
│       ├── ChatContainer
│       │   ├── Connection Status
│       │   ├── Agent Badge
│       │   ├── MessageList
│       │   │   └── MessageItem(s)
│       │   └── InputArea
│       └── Sidebar
│           ├── ProgressTracker
│           ├── StudentProfile
│           ├── Session Controls
│           └── Tips
```

### State Management

```
Global State (SessionContext)
├── session (SessionResponse)
├── isLoading
├── error
└── Methods (createSession, resetSession, etc.)

Local State (useChat hook)
├── messages (Message[])
├── isProcessing
├── isConnected
└── Methods (sendMessage)

WebSocket State (useWebSocket hook)
├── wsRef (WebSocket connection)
├── isConnected
└── Methods (sendMessage, reconnect)
```

### Data Flow

```
User Input
    ↓
InputArea Component
    ↓
useChat.sendMessage()
    ↓
useWebSocket.sendMessage()
    ↓
WebSocket → Backend
    ↓
Stream Events Received
    ↓
useChat.handleStreamEvent()
    ↓
Update messages state
    ↓
MessageList re-renders
    ↓
Display updated UI
```

## 🔄 Agent System Architecture

### Agent Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Lifecycle                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. User Message                                           │
│          ↓                                                  │
│  2. Current Agent Receives Message                         │
│          ↓                                                  │
│  3. Agent Processes (Uses Tools if needed)                 │
│          ↓                                                  │
│  4. Agent Generates Response (Streaming)                   │
│          ↓                                                  │
│  5. Agent Decides:                                         │
│      • Continue conversation                               │
│      • Handoff to another agent                           │
│          ↓                                                  │
│  6. Update Context (if tools modified state)               │
│          ↓                                                  │
│  7. Return to Step 1                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Agent Handoffs

```
Screener Agent
    ↓ (when screening_complete=True)
Teaching Agent
    ↓ (when concept_taught=True)
Quiz Agent
    ↓ (can go back to Teaching or Screener)
Teaching Agent / Screener Agent
```

### Tool Execution

```
Agent decides to use tool
    ↓
Tool Call Event sent to frontend
    ↓
Tool executes (e.g., cognitive_assessment_tool)
    ↓
Tool Result Event sent to frontend
    ↓
Context updated with tool results
    ↓
Agent continues with updated context
```

## 📊 Data Models

### StudentLearningContext

```python
class StudentLearningContext:
    # Profile
    student_name: str | None
    age: int | None
    grade_level: str | None
    cognitive_ability: str | None      # High/Medium/Low
    learning_style: str | None         # Visual/Auditory/Kinesthetic
    learning_pace: str | None          # Fast/Medium/Slow
    subjects_of_interest: List[str]

    # Current State
    current_subject: str | None
    current_topic: str | None
    learning_objectives: List[str]

    # Assessment Results
    quiz_score: int | None
    quiz_total: int | None

    # Workflow Flags
    screening_complete: bool
    concept_taught: bool
```

### Message Types

```typescript
type MessageType =
	| "user" // User message
	| "agent" // Agent response
	| "tool_call" // Tool being called
	| "tool_result" // Tool execution result
	| "handoff" // Agent handoff
	| "system"; // System message
```

### Stream Events

```typescript
type StreamEventType =
	| "token" // Text token delta
	| "agent_update" // Agent changed
	| "tool_call" // Tool called
	| "tool_result" // Tool result
	| "handoff" // Agent handoff
	| "message_complete" // Message finished
	| "error" // Error occurred
	| "context_update"; // Context state changed
```

## 🔐 Security Architecture

### API Security

1. **API Keys**: Stored server-side only in environment variables
2. **CORS**: Configurable allowed origins
3. **Input Validation**: Pydantic models validate all inputs
4. **Error Handling**: Sanitized error messages to clients

### Session Security

1. **Session IDs**: UUID-based, hard to guess
2. **Timeout**: Sessions expire after inactivity
3. **Isolation**: Each session has isolated context

## ⚡ Performance Optimizations

### Backend

-   **Async/Await**: All I/O operations are async
-   **Streaming**: Token-by-token response generation
-   **Connection Pooling**: Ready for database connections
-   **Efficient Session Storage**: In-memory with optional Redis

### Frontend

-   **Code Splitting**: Automatic by Next.js
-   **Lazy Loading**: Components loaded on demand
-   **Optimistic Updates**: Immediate UI feedback
-   **WebSocket Reconnection**: Automatic retry logic
-   **Efficient Re-rendering**: React optimizations

## 📡 Communication Protocols

### REST API

```
POST /api/session/start
  → Creates new session
  ← SessionResponse

GET /api/session/{id}
  → Retrieves session state
  ← SessionResponse

POST /api/session/{id}/reset
  → Resets session
  ← SessionResponse

DELETE /api/session/{id}
  → Deletes session
  ← Success message
```

### WebSocket Protocol

**Client → Server:**

```json
{
	"type": "message",
	"content": "User message content"
}
```

**Server → Client:**

```json
{
  "type": "token" | "agent_update" | "tool_call" | etc.,
  "data": {
    // Event-specific data
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🔧 Extensibility

### Adding New Agents

1. Define agent in `backend/app/agents/agents.py`
2. Add agent-specific tools in `backend/app/agents/tools.py`
3. Configure handoffs
4. Update AgentInfo in `backend/app/agents/agents.py`

### Adding New Endpoints

1. Add route in `backend/app/api/routes.py`
2. Add request/response models if needed
3. Implement service logic
4. Update frontend API client

### Adding New Features

1. **Backend**: Add service method
2. **Frontend**: Create React component
3. **Hook**: Create custom hook if needed
4. **Type**: Add TypeScript types
5. **Test**: Add tests for new feature

## 📈 Scalability Considerations

### Horizontal Scaling

-   **Backend**: Stateless API servers (with Redis for sessions)
-   **Frontend**: CDN distribution (Vercel/CloudFront)
-   **Database**: PostgreSQL/MySQL (when added)
-   **Cache**: Redis for session and response caching

### Load Balancing

-   **Backend**: Multiple FastAPI instances behind load balancer
-   **WebSocket**: Sticky sessions or Redis pub/sub
-   **Static Assets**: CDN edge locations

## 🔍 Monitoring & Observability

### Logging

-   **Backend**: Structured JSON logs
-   **Frontend**: Console logs (dev), Analytics (prod)
-   **WebSocket**: Connection events logged

### Metrics

-   API response times
-   WebSocket connection count
-   Session creation rate
-   Agent interaction frequency
-   Error rates

### Health Checks

-   `/api/health` endpoint
-   Frontend healthcheck (/)
-   WebSocket connectivity test

## 🎯 Design Principles

1. **Separation of Concerns**: Clear boundaries between layers
2. **Single Responsibility**: Each component has one job
3. **Type Safety**: TypeScript + Pydantic for all data
4. **Fail Gracefully**: Comprehensive error handling
5. **Performance First**: Optimized for speed
6. **User Experience**: Smooth, responsive UI
7. **Maintainability**: Clean, documented code
8. **Scalability**: Ready for growth

---

This architecture provides a solid foundation for a production-grade AI learning application with room for future enhancements and scaling.
