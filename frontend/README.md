# YourTeacher Frontend

Modern, accessible, and beautiful frontend for the YourTeacher AI-powered personalized learning system.

## 🎨 Design System

### Architecture

Built with **MVVM (Model-View-ViewModel)** architecture for clean separation of concerns:

- **Models** (`src/models/`): Data structures and types
  - `StudentContext.ts`: Student learning profile and context
  - `ChatMessage.ts`: Chat message types and phases
  - `Session.ts`: Learning session management

- **ViewModels** (`src/viewmodels/`): Business logic and state management
  - `useChatViewModel.ts`: Chat interactions and streaming
  - `useStudentViewModel.ts`: Student profile management

- **Views** (`src/components/`): UI components
  - `ui/`: shadcn/ui base components
  - `chat/`: Chat interface components
  - `phases/`: Phase-specific components
  - `layout/`: Layout components

- **Services** (`src/services/`): API integration
  - `api.ts`: Backend communication with streaming support

### Technology Stack

- **Next.js 16** with App Router
- **React 19** with Server Components
- **TypeScript** for type safety
- **Tailwind CSS 4** for styling
- **shadcn/ui** for accessible components
- **Lucide React** for icons

### Design Principles

#### Colors
Our educational color palette uses RGB CSS variables for consistency:

- **Primary (Teal)**: Trust & Knowledge - `rgb(20, 130, 130)`
- **Secondary (Orange)**: Energy & Engagement - `rgb(235, 110, 65)`
- **Accent (Purple)**: Highlight & Focus - `rgb(130, 95, 180)`
- **Background**: Soft cream for warmth - `rgb(253, 253, 250)`

#### Typography
- **Display Font**: Poppins (headings, bold statements)
- **Body Font**: Inter (readable, professional)

#### Animations
- Fade-in on load
- Slide-up for content
- Slide-in-left for side panels
- Pulse-glow for streaming indicators
- Duration: 150ms (fast), 300ms (normal), 500ms (slow)

#### Accessibility
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus visible states
- High contrast ratios (WCAG compliant)
- Screen reader friendly

## 🚀 Getting Started

### Prerequisites

- Node.js 20+ and npm/yarn/pnpm
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local

# Run development server
npm run dev
```

The app will be available at [http://localhost:3000](http://localhost:3000).

### Backend Setup

Make sure the YourTeacher backend is running:

```bash
cd ../backend
uvicorn app.main:app --reload --port 8000
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx            # Root layout with fonts
│   │   ├── page.tsx              # Main application page
│   │   └── globals.css           # Global styles and design tokens
│   ├── components/
│   │   ├── ui/                   # shadcn/ui base components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── textarea.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── label.tsx
│   │   │   └── spinner.tsx
│   │   ├── chat/                 # Chat interface
│   │   │   ├── ChatContainer.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   └── ChatInput.tsx
│   │   ├── phases/               # Learning phases
│   │   │   ├── WelcomeScreen.tsx
│   │   │   ├── PhaseIndicator.tsx
│   │   │   └── StudentProfileCard.tsx
│   │   └── layout/               # Layout components
│   │       └── Header.tsx
│   ├── models/                   # Data models
│   │   ├── StudentContext.ts
│   │   ├── ChatMessage.ts
│   │   └── Session.ts
│   ├── viewmodels/               # Business logic
│   │   ├── useChatViewModel.ts
│   │   └── useStudentViewModel.ts
│   ├── services/                 # API services
│   │   └── api.ts
│   └── lib/
│       └── utils.ts              # Utility functions
├── public/                       # Static assets
├── components.json               # shadcn/ui config
├── tsconfig.json                 # TypeScript config
└── package.json                  # Dependencies
```

## 🎯 Features

### Three-Phase Learning Journey

1. **Screening Phase** (Blue)
   - Cognitive ability assessment
   - Learning style identification
   - Pace determination
   - Profile creation

2. **Teaching Phase** (Teal)
   - Personalized lessons
   - Real-time streaming
   - Adaptive content
   - Interactive learning

3. **Quiz Phase** (Orange)
   - Custom assessments
   - Instant evaluation
   - Detailed feedback
   - Progress tracking

### Real-Time Streaming

- Token-by-token response display
- Live progress indicators
- Smooth animations
- Transparent AI operations

### Student Profile

- Visual profile card
- Cognitive ability badge
- Learning style indicator
- Pace visualization
- Interest tracking

### Responsive Design

- Mobile-first approach
- Tablet-optimized layouts
- Desktop-enhanced experience
- Smooth breakpoint transitions

## 🔧 Development

### Scripts

```bash
# Development server with hot reload
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Adding New Components

Use shadcn/ui CLI to add more components:

```bash
npx shadcn@latest add [component-name]
```

### Styling Guidelines

1. Use Tailwind CSS utility classes
2. Use `rgb(var(--color-name))` for theme colors
3. Use `font-[var(--font-display)]` for display font
4. Add animations with `animate-*` classes
5. Ensure responsive with `md:`, `lg:` breakpoints

### Accessibility Checklist

- ✅ Semantic HTML elements
- ✅ ARIA labels and roles
- ✅ Keyboard navigation
- ✅ Focus indicators
- ✅ Color contrast ratios
- ✅ Screen reader support
- ✅ Alternative text for images

## 🎨 Customization

### Colors

Edit `src/app/globals.css` to change the color palette:

```css
:root {
  --primary: 20 130 130;        /* Your custom RGB */
  --secondary: 235 110 65;
  --accent: 130 95 180;
  /* ... */
}
```

### Fonts

Edit `src/app/layout.tsx` to change fonts:

```typescript
import { YourFont } from "next/font/google";

const yourFont = YourFont({
  variable: "--font-custom",
  subsets: ["latin"],
});
```

### Animations

Add custom animations in `globals.css`:

```css
@keyframes your-animation {
  from { /* start state */ }
  to { /* end state */ }
}

.animate-your-animation {
  animation: your-animation 300ms ease-out;
}
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Welcome screen loads correctly
- [ ] Start button initiates screening
- [ ] Chat streaming works smoothly
- [ ] Messages display properly
- [ ] Phase transitions work
- [ ] Profile card updates correctly
- [ ] Reset button clears session
- [ ] Mobile layout is responsive
- [ ] Dark mode (if implemented)
- [ ] Keyboard navigation works

### Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📚 API Integration

The frontend communicates with the backend via:

### Endpoints

- `POST /api/chat/stream` - Stream chat responses
- `GET /api/session/{id}` - Get session info
- `DELETE /api/session/{id}` - Reset session

### Streaming Format

Server-Sent Events (SSE) with JSON payloads:

```
data: {"type": "text", "content": "Hello"}
data: {"type": "phase_change", "phase": "teaching"}
data: [DONE]
```

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Environment Variables

Set in your deployment platform:

```
NEXT_PUBLIC_API_URL=https://your-api-domain.com/api
```

### Build Optimization

- Automatic code splitting
- Image optimization with Next.js Image
- Font optimization with next/font
- CSS optimization with Tailwind

## 📖 Best Practices

### Performance

- Use `"use client"` only when needed
- Minimize client-side JavaScript
- Optimize images and assets
- Use React Suspense for loading states
- Implement proper error boundaries

### Code Quality

- Follow TypeScript strict mode
- Use ESLint and Prettier
- Write meaningful component names
- Keep components small and focused
- Document complex logic

### State Management

- Use ViewModels for business logic
- Keep UI components presentational
- Manage side effects in hooks
- Use React Context sparingly

## 🤝 Contributing

1. Follow the MVVM architecture
2. Maintain design system consistency
3. Ensure accessibility standards
4. Add TypeScript types
5. Test on multiple devices
6. Update documentation

## 📄 License

MIT License - See LICENSE file for details

---

Built with ❤️ using Next.js, React, and Tailwind CSS
