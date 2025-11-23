from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.api.dependencies import get_session_repo
from app.domain.interfaces.session_repository import ISessionRepository
from app.use_cases.chat import chat_stream

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@router.post("/chat/stream")
async def stream_chat(
    request: ChatRequest,
    repo: ISessionRepository = Depends(get_session_repo)
):
    return StreamingResponse(
        chat_stream(request.session_id, request.message, repo),
        media_type="text/event-stream"
    )

@router.get("/session/{session_id}")
async def get_session_info(
    session_id: str,
    repo: ISessionRepository = Depends(get_session_repo)
):
    session = await repo.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.context

@router.delete("/session/{session_id}")
async def reset_session(
    session_id: str,
    repo: ISessionRepository = Depends(get_session_repo)
):
    # For memory repo, we can just delete key or set to None
    # In real DB, we delete row
    if hasattr(repo, '_sessions') and session_id in repo._sessions:
        del repo._sessions[session_id]
    return {"status": "reset"}

