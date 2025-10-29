"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    AsyncOpenAI
)

from app.config import settings
from app.api import routes, websocket

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")

    # Configure OpenAI Agents SDK
    set_tracing_disabled(True)
    set_default_openai_api("chat_completions")

    # Set up Gemini API client
    external_client = AsyncOpenAI(
        api_key=settings.gemini_api_key,
        base_url=settings.openai_base_url,
    )
    set_default_openai_client(external_client)

    print("✅ OpenAI Agents SDK configured with Gemini API")
    print(
        f"📡 WebSocket endpoint: ws://localhost:{settings.backend_port}/api/ws/{{session_id}}")
    print(f"🔗 API docs: http://localhost:{settings.backend_port}/docs")

    yield

    # Shutdown
    print(f"🛑 Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-grade AI-powered personalized learning system with real-time streaming",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "YourTeacher API - Personalized Learning System",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.backend_port,
        reload=True,
        log_level="info"
    )
