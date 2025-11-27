# YourTeacher Frontend Architecture

## 🏗️ Architecture Overview

The frontend follows the **MVVM (Model-View-ViewModel)** architectural pattern for clean separation of concerns, testability, and maintainability.

```
┌─────────────────────────────────────────────────────────────┐
│                         View Layer                           │
│  (React Components - Presentational, UI-focused)             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Header     │  │  ChatInput   │  │ WelcomeScreen│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ChatContainer│  │ PhaseIndicator│  │ProfileCard   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ Uses
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     ViewModel Layer                          │
│  (Business Logic, State Management, Hooks)                   │
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐         │
│  │  useChatViewModel    │  │ useStudentViewModel  │         │
│  │  - sendMessage()     │  │ - updateContext()    │         │
│  │  - resetSession()    │  │ - getCompletion()    │         │
│  │  - streaming state   │  │ - profile state      │         │
│  └──────────────────────┘  └──────────────────────┘         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ Manipulates
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Model Layer                            │
│  (Data Structures, Types, Interfaces)                        │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Student   │  │   Chat     │  │  Session   │            │
│  │  Context   │  │  Message   │  │            │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ Communicates via
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                           │
│  (API Integration, External Communication)                   │
│                                                              │
│  ┌──────────────────────────────────────────────┐           │
│  │            API Service (api.ts)              │           │
│  │  - streamChat() → AsyncGenerator             │           │
│  │  - getSession() → Promise<Context>           │           │
│  │  - resetSession() → Promise<void>            │           │
│  └──────────────────────────────────────────────┘           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ HTTP/SSE
                            ▼
                    ┌───────────────┐
                    │    Backend    │
                    │  FastAPI API  │
                    └───────────────┘
```

## 📁 Directory Structure

```
src/
├── app/                          # Next.js App Router
│   ├── layout.tsx                # Root layout, fonts, metadata
│   ├── page.tsx                  # Main application page (orchestrator)
│   └── globals.css               # Global styles, design tokens, animations
│
├── models/                       # MODEL LAYER
│   ├── StudentContext.ts         # Student profile data structure
│   ├── ChatMessage.ts            # Chat message types and phases
│   └── Session.ts                # Session state structure
│
├── viewmodels/                   # VIEWMODEL LAYER
│   ├── useChatViewModel.ts       # Chat logic, streaming, message state
│   └── useStudentViewModel.ts    # Student profile logic, validation
│
├── services/                     # SERVICE LAYER
│   └── api.ts                    # Backend API integration with streaming
│
├── components/                   # VIEW LAYER
│   ├── ui/                       # Base UI components (shadcn/ui)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── textarea.tsx
│   │   ├── progress.tsx
│   │   ├── badge.tsx
│   │   ├── label.tsx
│   │   └── spinner.tsx
│   │
│   ├── chat/                     # Chat-specific components
│   │   ├── ChatContainer.tsx     # Message list container
│   │   ├── ChatMessage.tsx       # Individual message display
│   │   └── ChatInput.tsx         # Message input with auto-resize
│   │
│   ├── phases/                   # Learning phase components
│   │   ├── WelcomeScreen.tsx     # Initial landing page
│   │   ├── PhaseIndicator.tsx    # Progress indicator
│   │   └── StudentProfileCard.tsx # Profile display
│   │
│   └── layout/                   # Layout components
│       └── Header.tsx            # App header with navigation
│
└── lib/
    └── utils.ts                  # Utility functions (cn, etc.)
```

## 🔄 Data Flow

### 1. User Interaction Flow

```
User Action (Click/Type)
    ↓
View Component (Button/Input)
    ↓
Event Handler (onClick/onChange)
    ↓
ViewModel Hook (useChatViewModel)
    ↓
Service Call (streamChat)
    ↓
Backend API
    ↓
Stream Response (SSE)
    ↓
ViewModel State Update
    ↓
View Re-render
    ↓
UI Update (Streaming Text)
```

### 2. State Management Flow

```
┌─────────────────────────────────────────────┐
│          React State (useState)              │
│  - messages: ChatMessage[]                   │
│  - session: Session                          │
│  - isStreaming: boolean                      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│      ViewModel Hooks (Custom Hooks)          │
│  - useChatViewModel()                        │
│  - useStudentViewModel()                     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         Component Props (Props)              │
│  - Passed down to child components           │
│  - Callbacks passed up for actions           │
└─────────────────────────────────────────────┘
```

## 🎯 MVVM Pattern Implementation

### Model Layer

**Purpose**: Define data structures and types

**Files**:
- `StudentContext.ts`: Student learning profile
- `ChatMessage.ts`: Message structure with phases
- `Session.ts`: Session state management

**Principles**:
- Pure TypeScript interfaces/types
- No business logic
- Immutable data structures
- Factory functions for creation

**Example**:
```typescript
export interface StudentContext {
  student_name: string | null;
  cognitive_ability: CognitiveAbility | null;
  // ... other fields
}

export const createEmptyContext = (): StudentContext => ({
  // ... default values
});
```

### ViewModel Layer

**Purpose**: Handle business logic and state management

**Files**:
- `useChatViewModel.ts`: Chat interactions, streaming
- `useStudentViewModel.ts`: Profile management

**Principles**:
- Custom React hooks
- Manage component state
- Handle API calls
- Business logic encapsulation
- No direct DOM manipulation

**Example**:
```typescript
export function useChatViewModel() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  
  const sendMessage = useCallback(async (content: string) => {
    // Business logic here
    for await (const event of streamChat(sessionId, content)) {
      // Handle streaming
    }
  }, [dependencies]);
  
  return { messages, sendMessage, ... };
}
```

### View Layer

**Purpose**: Present UI and handle user interactions

**Files**: All components in `components/`

**Principles**:
- Presentational components
- Minimal logic (only UI-related)
- Use ViewModels for data
- Accessible (ARIA, keyboard)
- Responsive design

**Example**:
```typescript
export function ChatMessage({ message }: Props) {
  const vm = useChatViewModel();
  
  return (
    <div>
      {/* UI markup only */}
    </div>
  );
}
```

## 🌊 Streaming Architecture

### Real-Time Streaming Implementation

```
Backend (FastAPI)
    ↓
Server-Sent Events (SSE)
    ↓
Fetch API (Response.body.getReader())
    ↓
TextDecoder (decode chunks)
    ↓
Line-by-line parsing
    ↓
JSON parsing per line
    ↓
AsyncGenerator (yield events)
    ↓
for await...of loop
    ↓
State updates (setMessages)
    ↓
React re-render
    ↓
Animated UI update
```

### Streaming Event Types

```typescript
type StreamEvent = 
  | { type: "text", data: string }
  | { type: "tool_use", data: ToolUse }
  | { type: "phase_change", data: Phase }
  | { type: "error", data: string }
  | { type: "done", data: null }
```

## 🎨 Design System Architecture

### Token-Based Design

```
CSS Variables (globals.css)
    ↓
Tailwind Theme (inline theme)
    ↓
Component Variants (CVA)
    ↓
Component Props (variant, size)
    ↓
Applied Classes (cn utility)
```

### Color System

```
Light Mode              Dark Mode
    ↓                       ↓
RGB Values              RGB Values
    ↓                       ↓
CSS Variables           CSS Variables
(--primary)             (--primary)
    ↓                       ↓
Tailwind Classes        Tailwind Classes
rgb(var(--primary))     rgb(var(--primary))
    ↓                       ↓
Components              Components
```

### Animation System

```
@keyframes (globals.css)
    ↓
.animate-* classes
    ↓
Applied to components
    ↓
Triggered on mount/change
    ↓
Smooth transitions
```

## 🔐 Type Safety

### TypeScript Flow

```
Interface Definition (models/)
    ↓
Type Imports (in ViewModels)
    ↓
Typed State (useState<Type>)
    ↓
Typed Props (ComponentProps)
    ↓
Type Checking (at compile time)
    ↓
Runtime Safety
```

## 📱 Responsive Design

### Breakpoint Strategy

```
Mobile First (base styles)
    ↓
sm: (640px+) - Small tablets
    ↓
md: (768px+) - Tablets
    ↓
lg: (1024px+) - Laptops
    ↓
xl: (1280px+) - Desktops
```

### Responsive Patterns

1. **Flex/Grid Layouts**: Adapt to screen size
2. **Hidden Elements**: `hidden md:block`
3. **Responsive Typography**: `text-base lg:text-lg`
4. **Responsive Spacing**: `p-4 md:p-6 lg:p-8`

## ♿ Accessibility Architecture

### A11y Layers

```
Semantic HTML (base)
    ↓
ARIA Attributes (enhanced)
    ↓
Keyboard Navigation (interactions)
    ↓
Focus Management (visual feedback)
    ↓
Screen Reader Support (announcements)
```

### Accessibility Features

- **Semantic HTML**: Proper element usage
- **ARIA Labels**: Descriptive labels for screen readers
- **Keyboard Navigation**: Full keyboard support
- **Focus Indicators**: Visible focus states
- **Color Contrast**: WCAG AA/AAA compliance
- **Alt Text**: Images have descriptions

## 🚀 Performance Architecture

### Optimization Strategies

1. **Code Splitting**: Dynamic imports for heavy components
2. **Tree Shaking**: Unused code elimination
3. **Image Optimization**: Next.js Image component
4. **Font Optimization**: next/font with swap
5. **Lazy Loading**: Components loaded on demand
6. **Memoization**: React.memo for expensive renders

### Bundle Strategy

```
App Code (application logic)
    ↓
Chunks (automatic splitting)
    ↓
    ├── main-[hash].js (core app)
    ├── framework-[hash].js (React, Next.js)
    ├── vendors-[hash].js (dependencies)
    └── [page]-[hash].js (per-page code)
```

## 🧪 Testing Strategy

### Testing Layers

1. **Unit Tests**: Individual functions (models, utils)
2. **Hook Tests**: ViewModel hooks (React Testing Library)
3. **Component Tests**: UI components (Jest + RTL)
4. **Integration Tests**: Full user flows (Playwright)
5. **E2E Tests**: Complete application (Cypress/Playwright)

## 📦 Build Architecture

### Build Pipeline

```
TypeScript Source
    ↓
Next.js Compilation
    ↓
    ├── Type Checking (tsc)
    ├── Transpilation (SWC)
    ├── Bundling (Webpack/Turbopack)
    └── Optimization (Minification, Tree-shaking)
    ↓
.next/ Output
    ↓
Static + Server
```

## 🔄 Deployment Architecture

### Deployment Options

1. **Vercel** (Recommended)
   - Automatic builds on push
   - Edge functions
   - CDN distribution

2. **Docker**
   - Multi-stage build
   - Production optimized
   - Container orchestration ready

3. **Custom Server**
   - Node.js server
   - PM2 process manager
   - Nginx reverse proxy

## 📊 Monitoring & Analytics

### Monitoring Points

```
Browser (Client)
    ↓
Console Logs (development)
    ↓
Error Boundaries (React)
    ↓
Analytics Events (user actions)
    ↓
Performance Metrics (Web Vitals)
    ↓
Server Logs (SSR/API)
```

## 🔮 Future Enhancements

### Planned Architecture Improvements

1. **State Management**: Redux Toolkit or Zustand
2. **Data Fetching**: React Query/SWR
3. **Testing**: Comprehensive test suite
4. **CI/CD**: Automated testing and deployment
5. **Monitoring**: Error tracking (Sentry)
6. **Analytics**: User behavior tracking
7. **PWA**: Offline support
8. **i18n**: Multi-language support

## 📝 Best Practices

### Code Organization

✅ **DO**:
- Keep components small and focused
- Use TypeScript for type safety
- Follow MVVM pattern strictly
- Write meaningful names
- Comment complex logic

❌ **DON'T**:
- Mix business logic with UI
- Create large monolithic components
- Skip type definitions
- Ignore accessibility
- Hardcode values

### Performance

✅ **DO**:
- Use React.memo for expensive components
- Implement proper loading states
- Optimize images
- Lazy load heavy components
- Profile performance regularly

❌ **DON'T**:
- Create unnecessary re-renders
- Load all data upfront
- Skip optimization
- Ignore bundle size
- Nest too deeply

---

**Architecture Version**: 1.0.0
**Last Updated**: 2025
**Maintained By**: YourTeacher Team


