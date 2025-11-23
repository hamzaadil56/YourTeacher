# YourTeacher Frontend Setup Guide

Complete setup instructions for the YourTeacher frontend application.

## Prerequisites

Ensure you have the following installed:

- **Node.js 20+** (check with `node --version`)
- **npm 10+** or **yarn** or **pnpm**
- **Git** for version control

## Step-by-Step Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

This will install all required packages including:
- Next.js 16
- React 19
- Tailwind CSS 4
- TypeScript
- shadcn/ui components
- Lucide icons

### 2. Environment Configuration

Create a `.env.local` file in the frontend directory:

```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
```

**Important**: Make sure the backend is running on port 8000 or update this URL accordingly.

### 3. Start Development Server

```bash
npm run dev
```

The application will start on [http://localhost:3000](http://localhost:3000).

### 4. Verify Backend Connection

The frontend expects the backend API to be running. Start the backend:

```bash
# In a separate terminal
cd ../backend
uvicorn app.main:app --reload --port 8000
```

Verify the backend is running by visiting:
- http://localhost:8000/docs (API documentation)

## Production Build

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `.next` folder.

### Start Production Server

```bash
npm start
```

The production server will run on port 3000 by default.

### Change Port (Optional)

```bash
# Development
PORT=3001 npm run dev

# Production
PORT=3001 npm start
```

## Troubleshooting

### Port Already in Use

If port 3000 is already in use:

```bash
# Find process using port 3000
lsof -i :3000

# Kill the process (replace PID with actual process ID)
kill -9 PID

# Or use a different port
PORT=3001 npm run dev
```

### API Connection Issues

If you see "Failed to fetch" errors:

1. Verify backend is running: `curl http://localhost:8000/api`
2. Check CORS settings in backend
3. Verify `.env.local` has correct API URL
4. Check browser console for detailed errors

### Build Errors

If you encounter TypeScript errors during build:

```bash
# Clear Next.js cache
rm -rf .next

# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Try building again
npm run build
```

### Styling Issues

If Tailwind styles aren't loading:

1. Verify `globals.css` is imported in `layout.tsx`
2. Check `postcss.config.mjs` exists
3. Clear `.next` cache and restart dev server

## Development Workflow

### 1. Feature Development

```bash
# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes
# Test thoroughly

# Commit changes
git add .
git commit -m "Add: your feature description"
```

### 2. Testing

Manual testing checklist:
- [ ] Test on Chrome/Firefox/Safari
- [ ] Test mobile responsive design
- [ ] Test keyboard navigation
- [ ] Test with screen reader (optional)
- [ ] Test API error scenarios
- [ ] Test streaming functionality

### 3. Code Quality

```bash
# Lint your code
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

## Adding New Components

### Using shadcn/ui CLI

```bash
# Add a new shadcn component
npx shadcn@latest add [component-name]

# Example: Add dialog component
npx shadcn@latest add dialog
```

### Creating Custom Components

Follow the MVVM structure:

1. **Model**: Create in `src/models/`
2. **ViewModel**: Create hook in `src/viewmodels/`
3. **View**: Create component in `src/components/`

Example:

```typescript
// 1. Model (src/models/NewFeature.ts)
export interface NewFeature {
  id: string;
  name: string;
}

// 2. ViewModel (src/viewmodels/useNewFeatureViewModel.ts)
export function useNewFeatureViewModel() {
  const [data, setData] = useState<NewFeature[]>([]);
  // ... business logic
  return { data, /* ... */ };
}

// 3. View (src/components/features/NewFeatureComponent.tsx)
export function NewFeatureComponent() {
  const vm = useNewFeatureViewModel();
  return <div>{/* UI */}</div>;
}
```

## Environment Variables

### Available Variables

```bash
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Optional (add as needed)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_DEBUG_MODE=false
```

**Note**: Variables starting with `NEXT_PUBLIC_` are exposed to the browser.

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import project in Vercel dashboard
3. Configure environment variables
4. Deploy automatically on push

### Docker

```bash
# Build Docker image
docker build -t yourteacher-frontend .

# Run container
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://your-backend-url yourteacher-frontend
```

### Custom Server

```bash
# Build
npm run build

# Copy files to server
scp -r .next package.json your-server:/var/www/yourteacher

# On server, install dependencies and start
npm install --production
npm start
```

## Performance Optimization

### Recommendations

1. **Enable Image Optimization**
   - Use Next.js `<Image>` component
   - Configure `next.config.ts` with image domains

2. **Code Splitting**
   - Use dynamic imports for large components
   - Example: `const HeavyComponent = dynamic(() => import('./Heavy'))`

3. **Caching**
   - Implement proper cache headers
   - Use React Query for data fetching (optional)

4. **Bundle Analysis**
   ```bash
   npm install @next/bundle-analyzer
   # Update next.config.ts to use analyzer
   npm run build
   ```

## Monitoring

### Development Monitoring

- React Developer Tools (browser extension)
- Network tab for API calls
- Console for errors and warnings

### Production Monitoring

- Vercel Analytics (if using Vercel)
- Google Analytics (configure in `layout.tsx`)
- Error tracking (Sentry, etc.)

## Getting Help

### Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com)

### Common Issues

1. **"Module not found"** → Run `npm install`
2. **"Port in use"** → Change port or kill process
3. **"API not responding"** → Check backend is running
4. **Styling not applied** → Clear cache, restart dev server

## Next Steps

After setup is complete:

1. ✅ Verify frontend loads at http://localhost:3000
2. ✅ Verify backend connection works
3. ✅ Test the welcome screen
4. ✅ Test starting a session
5. ✅ Test chat streaming
6. ✅ Test all three phases (Screening, Teaching, Quiz)
7. ✅ Test session reset

Happy coding! 🚀

