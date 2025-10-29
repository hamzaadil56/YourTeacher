# YourTeacher - Next.js + FastAPI Implementation Plan

## 📋 Overview

Convert the current Python/Streamlit application to a production-grade architecture using:

-   **Frontend**: Next.js 14+ with TypeScript, Tailwind CSS, and shadcn/ui
-   **Backend**: FastAPI with WebSocket streaming support

## 🎯 Core Requirements

### Must Preserve

1. **Three-Agent System**: Screener → Teaching → Quiz agents
2. **Real-time Streaming**: Token-by-token response generation
3. **Context Management**: Student profile and learning state
4. **Tool Usage**: All existing tools and functionality
5. **Agent Handoffs**: Seamless transitions between agents

## 🏗️ Architecture Design

### Backend (FastAPI)

#### Directory Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI app initialization
│   ├── config.py                  # Configuration and settings
│   ├── models/
│   │   ├── context.py             # StudentLearningContext
│   │   ├── requests.py            # API request models
│   │   └── responses.py           # API response models
│   ├── agents/
│   │   ├── screener_agent.py      # Screener agent setup
│   │   ├── teaching_agent.py      # Teaching agent setup
│   │   ├── quiz_agent.py          # Quiz agent setup
│   │   └── tools.py               # All agent tools
│   ├── services/
│   │   ├── agent_service.py       # Agent orchestration
│   │   └── session_service.py     # Session management
│   ├── api/
│   │   ├── routes.py              # REST API endpoints
│   │   └── websocket.py           # WebSocket streaming
│   └── utils/
│       └── streaming.py           # Streaming utilities
├── requirements.txt
└── .env
```

#### Key Components

1. **API Endpoints**

    - `POST /api/session/start` - Initialize new learning session
    - `GET /api/session/{session_id}` - Get session state
    - `POST /api/session/{session_id}/reset` - Reset session
    - `WS /api/ws/{session_id}` - WebSocket for streaming

2. **WebSocket Protocol**

    ```json
    // Client → Server
    {
      "type": "message",
      "content": "User message",
      "session_id": "uuid"
    }

    // Server → Client
    {
      "type": "token" | "agent_update" | "tool_call" | "handoff" | "complete",
      "data": {...},
      "timestamp": "ISO8601"
    }
    ```

3. **Session Management**

    - In-memory storage with Redis option
    - Session expiration and cleanup
    - Context preservation across connections

4. **Streaming Implementation**
    - Async generator for token streaming
    - Event-based updates for agent activities
    - Efficient WebSocket message batching

### Frontend (Next.js)

#### Directory Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx             # Root layout
│   │   ├── page.tsx               # Home/chat page
│   │   └── globals.css            # Global styles
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── progress.tsx
│   │   │   └── ...
│   │   ├── chat/
│   │   │   ├── ChatContainer.tsx  # Main chat wrapper
│   │   │   ├── MessageList.tsx    # Message display
│   │   │   ├── MessageItem.tsx    # Individual message
│   │   │   ├── InputArea.tsx      # User input
│   │   │   └── StreamingIndicator.tsx
│   │   ├── sidebar/
│   │   │   ├── Sidebar.tsx        # Main sidebar
│   │   │   ├── ProgressTracker.tsx
│   │   │   ├── AgentStatus.tsx
│   │   │   └── StudentProfile.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   ├── hooks/
│   │   ├── useWebSocket.ts        # WebSocket management
│   │   ├── useChat.ts             # Chat state management
│   │   └── useSession.ts          # Session management
│   ├── lib/
│   │   ├── api.ts                 # API client
│   │   ├── websocket.ts           # WebSocket client
│   │   └── utils.ts               # Utilities
│   ├── types/
│   │   ├── agent.ts
│   │   ├── message.ts
│   │   └── session.ts
│   └── contexts/
│       └── SessionContext.tsx     # Global session state
├── public/
├── package.json
├── tailwind.config.ts
├── components.json                # shadcn/ui config
└── next.config.js
```

#### Key Features

1. **Minimalistic UI Design**

    - Clean, modern interface
    - Focus on conversation flow
    - Subtle agent indicators
    - Smooth animations

2. **Real-time Streaming**

    - WebSocket connection management
    - Incremental message updates
    - Automatic reconnection
    - Loading states

3. **State Management**

    - React Context for global state
    - Local state for UI interactions
    - Optimistic updates

4. **Responsive Design**
    - Mobile-first approach
    - Adaptive layouts
    - Touch-friendly interactions

## 🔄 Implementation Steps

### Phase 1: Backend Foundation

1. Set up FastAPI project structure
2. Implement StudentLearningContext model
3. Port all agent tools
4. Configure OpenAI Agents SDK integration

### Phase 2: Backend Streaming

1. Implement WebSocket endpoint
2. Create streaming event handlers
3. Build session management
4. Add error handling and recovery

### Phase 3: Frontend Foundation

1. Initialize Next.js project with TypeScript
2. Configure Tailwind CSS
3. Install and configure shadcn/ui
4. Set up project structure

### Phase 4: Frontend Core UI

1. Build chat interface components
2. Implement message display
3. Create input area
4. Add sidebar with progress tracking

### Phase 5: Frontend Streaming

1. Implement WebSocket client
2. Create streaming hooks
3. Handle real-time updates
4. Add reconnection logic

### Phase 6: Integration & Polish

1. Connect frontend to backend
2. Test all agent workflows
3. Optimize performance
4. Add loading states and error handling

### Phase 7: Production Readiness

1. Environment configuration
2. Docker setup (optional)
3. Documentation
4. Deployment guides

## 🎨 UI/UX Design Principles

### Minimalistic Design

-   **Clean Layout**: Ample whitespace, clear hierarchy
-   **Subtle Colors**: Professional color palette, gentle gradients
-   **Typography**: Readable fonts, appropriate sizing
-   **Icons**: Consistent icon set for agents and actions

### User Experience

-   **Progressive Disclosure**: Show information when needed
-   **Feedback**: Clear loading states and confirmations
-   **Accessibility**: Keyboard navigation, ARIA labels
-   **Performance**: Fast load times, smooth animations

### Component Design

-   **Chat Messages**: Distinct styles for user/agent messages
-   **Agent Indicators**: Visual cues for current agent
-   **Progress Display**: Clear learning journey visualization
-   **Tool Usage**: Subtle indicators when tools are used

## 🔧 Technical Decisions

### Backend

-   **FastAPI**: High performance, native async support
-   **WebSockets**: Real-time bidirectional communication
-   **Pydantic**: Type-safe data validation
-   **OpenAI Agents SDK**: Preserve existing agent logic

### Frontend

-   **Next.js 14**: App Router, Server Components
-   **TypeScript**: Type safety and better DX
-   **Tailwind CSS**: Utility-first styling
-   **shadcn/ui**: High-quality, customizable components
-   **WebSocket API**: Native browser WebSocket

### Data Flow

```
User Input → WebSocket → FastAPI → Agent System → Streaming Response → WebSocket → UI Update
```

## 📊 Performance Optimization

### Backend

-   Connection pooling for database/APIs
-   Efficient session storage
-   Streaming response generation
-   Async/await throughout

### Frontend

-   Code splitting
-   Lazy loading components
-   Optimistic UI updates
-   Debounced inputs

## 🧪 Testing Strategy

### Backend

-   Unit tests for tools and utilities
-   Integration tests for API endpoints
-   WebSocket connection tests
-   Agent workflow tests

### Frontend

-   Component unit tests
-   Integration tests
-   E2E tests with Playwright
-   WebSocket mock testing

## 📦 Deployment

### Backend

-   Docker containerization
-   Environment variables management
-   CORS configuration
-   Rate limiting

### Frontend

-   Vercel deployment (recommended)
-   Environment variables
-   API URL configuration
-   WebSocket proxy setup

## 🔐 Security Considerations

-   API key management
-   Session validation
-   Input sanitization
-   CORS policies
-   Rate limiting
-   WebSocket authentication

## 📝 Documentation Deliverables

1. Backend API documentation (FastAPI auto-generated)
2. Frontend component documentation
3. Setup and installation guides
4. Environment configuration guide
5. Deployment instructions
6. Developer contribution guide

## ✅ Success Criteria

-   [ ] All three agents work correctly
-   [ ] Streaming responses display in real-time
-   [ ] Agent handoffs function seamlessly
-   [ ] All tools execute properly
-   [ ] Session state persists correctly
-   [ ] UI is responsive and intuitive
-   [ ] Performance is optimal (<100ms latency)
-   [ ] Error handling is robust
-   [ ] Code is well-documented
-   [ ] Production-ready deployment setup

## 🚀 Next Steps

1. Create backend structure
2. Implement core FastAPI app
3. Port agent system
4. Build WebSocket streaming
5. Initialize Next.js project
6. Build UI components
7. Implement WebSocket client
8. Integration testing
9. Polish and optimize
10. Documentation and deployment
