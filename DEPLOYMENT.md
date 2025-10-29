# 🚀 Deployment Guide

Production deployment guide for YourTeacher application.

## 🌐 Deployment Options

### 1. Vercel (Frontend) + Railway/Render (Backend)

#### Frontend on Vercel

1. **Install Vercel CLI:**

```bash
npm i -g vercel
```

2. **Deploy Frontend:**

```bash
cd frontend
vercel
```

3. **Configure Environment Variables:**
   In Vercel dashboard:

-   `NEXT_PUBLIC_API_URL`: Your backend API URL
-   `NEXT_PUBLIC_WS_URL`: Your backend WebSocket URL

4. **Set up Custom Domain** (optional)

#### Backend on Railway

1. **Sign up at [Railway.app](https://railway.app)**

2. **Create New Project** → Deploy from GitHub

3. **Configure Environment Variables:**

-   `GEMINI_API_KEY`: Your API key
-   `CORS_ORIGINS`: Your frontend URL(s)
-   `PORT`: Railway will set automatically

4. **Deploy** - Railway auto-detects Python and runs your app

#### Backend on Render

1. **Sign up at [Render.com](https://render.com)**

2. **Create New Web Service** → Connect GitHub

3. **Configure:**

-   Build Command: `pip install -r requirements.txt`
-   Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables:**

-   `GEMINI_API_KEY`
-   `CORS_ORIGINS`

### 2. AWS Deployment

#### Backend on AWS ECS/Fargate

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Deploy using:

-   ECS with Fargate
-   Application Load Balancer for WebSocket support
-   CloudWatch for logging

#### Frontend on AWS Amplify

1. Connect GitHub repository
2. Configure build settings
3. Set environment variables
4. Deploy

### 3. Google Cloud Platform

#### Backend on Cloud Run

```bash
# Build and deploy
gcloud run deploy yourteacher-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY
```

#### Frontend on Cloud Run or Firebase Hosting

**Cloud Run:**

```bash
gcloud run deploy yourteacher-frontend \
  --source ./frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Firebase Hosting:**

```bash
cd frontend
npm run build
firebase deploy
```

### 4. DigitalOcean App Platform

1. **Create New App**
2. **Connect GitHub**
3. **Configure Components:**
    - Backend: Python service
    - Frontend: Node.js service
4. **Set Environment Variables**
5. **Deploy**

### 5. Heroku

#### Backend

```bash
cd backend

# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create yourteacher-api
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

#### Frontend

```bash
cd frontend

# Heroku auto-detects Next.js
heroku create yourteacher-app
heroku config:set NEXT_PUBLIC_API_URL=https://yourteacher-api.herokuapp.com
git push heroku main
```

## 🐳 Docker Deployment

### Docker Compose Production

```yaml
version: "3.8"

services:
    backend:
        build: ./backend
        restart: always
        ports:
            - "8000:8000"
        environment:
            - GEMINI_API_KEY=${GEMINI_API_KEY}
            - CORS_ORIGINS=${FRONTEND_URL}
        healthcheck:
            test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
            interval: 30s
            timeout: 10s
            retries: 3

    frontend:
        build:
            context: ./frontend
            args:
                - NEXT_PUBLIC_API_URL=${BACKEND_URL}
                - NEXT_PUBLIC_WS_URL=${WS_URL}
        restart: always
        ports:
            - "3000:3000"
        depends_on:
            - backend

    nginx:
        image: nginx:alpine
        ports:
            - "80:80"
            - "443:443"
        volumes:
            - ./nginx.conf:/etc/nginx/nginx.conf
            - ./ssl:/etc/nginx/ssl
        depends_on:
            - frontend
            - backend
```

### Nginx Configuration

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name yourteacher.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourteacher.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket
    location /api/ws {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

## 🔒 Production Checklist

### Security

-   [ ] API keys in environment variables, not code
-   [ ] HTTPS enabled
-   [ ] CORS properly configured
-   [ ] Rate limiting enabled
-   [ ] WebSocket authentication (if needed)
-   [ ] Input validation and sanitization
-   [ ] Error messages don't leak sensitive info
-   [ ] Security headers configured

### Performance

-   [ ] Backend: Gunicorn/Uvicorn workers configured
-   [ ] Frontend: Production build optimized
-   [ ] CDN for static assets
-   [ ] Database connection pooling (if added)
-   [ ] Caching strategy implemented
-   [ ] WebSocket message batching
-   [ ] Gzip compression enabled

### Monitoring

-   [ ] Application logs configured
-   [ ] Error tracking (Sentry, etc.)
-   [ ] Performance monitoring (New Relic, DataDog)
-   [ ] Uptime monitoring
-   [ ] WebSocket connection monitoring
-   [ ] Session metrics tracking

### Scalability

-   [ ] Horizontal scaling configured
-   [ ] Load balancer setup
-   [ ] Session storage (Redis for multiple instances)
-   [ ] Auto-scaling rules
-   [ ] Database optimization (if added)

### Backup & Recovery

-   [ ] Automated backups
-   [ ] Disaster recovery plan
-   [ ] Database backups (if applicable)
-   [ ] Configuration backups
-   [ ] Rollback procedure documented

## 📊 Environment Variables

### Backend Production

```bash
GEMINI_API_KEY=your_production_key
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com
BACKEND_PORT=8000
```

### Frontend Production

```bash
NEXT_PUBLIC_API_URL=https://api.yourapp.com
NEXT_PUBLIC_WS_URL=wss://api.yourapp.com
```

## 🔍 Health Checks

### Backend Health Endpoint

```bash
curl https://api.yourapp.com/api/health
```

### Frontend Health

```bash
curl https://yourapp.com
```

## 📈 Scaling Strategies

### Backend Scaling

1. **Vertical**: Increase server resources
2. **Horizontal**: Add more server instances
3. **Database**: Use Redis for session storage
4. **Caching**: Cache frequent responses

### Frontend Scaling

1. **CDN**: Use Vercel/CloudFront
2. **Static Generation**: Pre-render where possible
3. **Code Splitting**: Optimize bundle sizes
4. **Image Optimization**: Use Next.js Image component

## 🐛 Debugging Production Issues

### Backend Logs

```bash
# View logs
docker-compose logs backend -f

# Or on cloud platform
railway logs
render logs
```

### Frontend Logs

```bash
# View build logs on platform
vercel logs

# Browser console for client-side issues
```

### WebSocket Issues

-   Check proxy configuration
-   Verify WebSocket upgrade headers
-   Monitor connection timeout settings
-   Check firewall rules

## 🚦 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
    push:
        branches: [main]

jobs:
    deploy-backend:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v2
            - name: Deploy to Railway
              uses: bervProject/railway-deploy@main
              with:
                  railway_token: ${{ secrets.RAILWAY_TOKEN }}
                  service: backend

    deploy-frontend:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v2
            - name: Deploy to Vercel
              uses: amondnet/vercel-action@v20
              with:
                  vercel-token: ${{ secrets.VERCEL_TOKEN }}
                  vercel-org-id: ${{ secrets.ORG_ID }}
                  vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 📞 Support & Monitoring

### Error Tracking

```bash
# Install Sentry
pip install sentry-sdk
npm install @sentry/nextjs
```

### Uptime Monitoring

-   UptimeRobot
-   Pingdom
-   StatusCake

### Performance Monitoring

-   New Relic
-   DataDog
-   CloudWatch (AWS)

## ✅ Post-Deployment Verification

1. [ ] All services are running
2. [ ] HTTPS is working
3. [ ] WebSocket connections successful
4. [ ] Agent interactions working
5. [ ] Session creation/management
6. [ ] All API endpoints responding
7. [ ] Frontend loads correctly
8. [ ] Mobile responsiveness verified
9. [ ] Performance is acceptable
10. [ ] Monitoring is active

## 🎉 You're Live!

Your application is now running in production. Monitor logs and metrics to ensure smooth operation.

For issues, check:

1. Server logs
2. Application metrics
3. Error tracking dashboard
4. User feedback
