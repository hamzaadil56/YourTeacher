# YourTeacher Frontend - Next.js

Production-grade frontend for the YourTeacher personalized learning system.

## 🚀 Features

-   **Next.js 14+**: Modern React framework with App Router
-   **TypeScript**: Type-safe development
-   **Tailwind CSS**: Utility-first styling
-   **shadcn/ui**: High-quality, accessible UI components
-   **Real-time Streaming**: WebSocket integration for live responses
-   **Responsive Design**: Mobile-first, adaptive layouts
-   **Dark Mode Support**: Seamless theme switching

## 📋 Requirements

-   Node.js 18+
-   npm or yarn
-   Backend API running (see backend README)

## 🔧 Installation

1. **Navigate to frontend directory:**

```bash
cd frontend
```

2. **Install dependencies:**

```bash
npm install
```

3. **Configure environment:**

```bash
# .env.local is already configured for local development
# Update if your backend is running on different ports
```

## ▶️ Running the Application

**Development mode:**

```bash
npm run dev
```

**Build for production:**

```bash
npm run build
npm start
```

The application will start at http://localhost:3000

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── chat/               # Chat interface components
│   │   │   ├── ChatContainer.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageItem.tsx
│   │   │   └── InputArea.tsx
│   │   ├── sidebar/            # Sidebar components
│   │   │   ├── Sidebar.tsx
│   │   │   ├── ProgressTracker.tsx
│   │   │   └── StudentProfile.tsx
│   │   └── layout/             # Layout components
│   │       └── Header.tsx
│   ├── hooks/                  # Custom React hooks
│   │   ├── useWebSocket.ts     # WebSocket management
│   │   └── useChat.ts          # Chat state management
│   ├── contexts/               # React contexts
│   │   └── SessionContext.tsx  # Global session state
│   ├── lib/                    # Utilities
│   │   ├── api.ts              # API client
│   │   └── utils.ts            # Helper functions
│   └── types/                  # TypeScript definitions
│       └── index.ts
├── public/                     # Static assets
├── package.json
├── tailwind.config.ts
├── components.json             # shadcn/ui config
└── next.config.js
```

## 🎨 UI Components

The application uses shadcn/ui components for a consistent, accessible design:

-   **Button**: Primary actions and interactions
-   **Card**: Content containers
-   **Input**: Text input fields
-   **Badge**: Status indicators
-   **Progress**: Loading and progress bars
-   **Avatar**: User and agent avatars
-   **ScrollArea**: Scrollable content areas

## 🔌 API Integration

The frontend communicates with the backend via:

1. **REST API** for session management
    - Create/get/reset/delete sessions
2. **WebSocket** for real-time streaming
    - Token-by-token response display
    - Agent status updates
    - Tool usage notifications

## 🎯 Key Features

### Real-time Streaming

-   Token-by-token message display
-   Live typing indicators
-   Automatic reconnection
-   Connection status monitoring

### Session Management

-   Persistent sessions via localStorage
-   Automatic session restoration
-   Session reset capability
-   Context state management

### Progress Tracking

-   Visual learning journey display
-   Phase completion indicators
-   Student profile summary
-   Quiz score tracking

### Responsive Design

-   Mobile-first approach
-   Adaptive layouts
-   Touch-friendly interactions
-   Optimized for all screen sizes

## 🛠️ Development

### Adding New Components

```bash
# Add shadcn/ui components
npx shadcn@latest add [component-name]
```

### Code Style

The project uses:

-   ESLint for code quality
-   TypeScript for type safety
-   Prettier (recommended) for formatting

### Environment Variables

-   `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
-   `NEXT_PUBLIC_WS_URL`: WebSocket URL (default: ws://localhost:8000)

## 🐛 Troubleshooting

**Connection issues:**

-   Ensure backend is running
-   Check CORS settings in backend
-   Verify WebSocket URL is correct

**Build errors:**

-   Clear .next directory: `rm -rf .next`
-   Reinstall dependencies: `rm -rf node_modules && npm install`

**Styling issues:**

-   Check Tailwind config
-   Verify CSS imports
-   Clear browser cache

## 📦 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker

```bash
# Build
docker build -t yourteacher-frontend .

# Run
docker run -p 3000:3000 yourteacher-frontend
```

## 🔒 Security

-   API keys are not exposed to client
-   CORS properly configured
-   Input sanitization
-   XSS protection via React

## 📄 License

MIT License - see main project LICENSE file
