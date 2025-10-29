from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import chat

app = FastAPI(
    title="YourTeacher API",
    description="API for the YourTeacher personalized learning system.",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",  # Allow Next.js frontend
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the YourTeacher API!"}
