"""
REST API Routes
"""
from fastapi import APIRouter, HTTPException
from app.models.requests import SessionCreateRequest
from app.models.responses import SessionResponse, AgentInfo
from app.services.session_service import get_session_service
from app.agents import get_agent_info

router = APIRouter(prefix="/api", tags=["sessions"])


@router.post("/session/start", response_model=SessionResponse)
async def create_session(request: SessionCreateRequest):
    """
    Create a new learning session

    Returns:
        SessionResponse: Session information including ID and initial state
    """
    session_service = get_session_service()
    session = session_service.create_session(request.initial_message)

    agent_info = get_agent_info(session.current_agent.name)

    return SessionResponse(
        session_id=session.session_id,
        current_agent=agent_info,
        context=session.context,
        created_at=session.created_at,
        message_count=session.message_count
    )


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """
    Get session information

    Args:
        session_id: The session identifier

    Returns:
        SessionResponse: Current session state
    """
    session_service = get_session_service()
    session = session_service.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    agent_info = get_agent_info(session.current_agent.name)

    return SessionResponse(
        session_id=session.session_id,
        current_agent=agent_info,
        context=session.context,
        created_at=session.created_at,
        message_count=session.message_count
    )


@router.post("/session/{session_id}/reset", response_model=SessionResponse)
async def reset_session(session_id: str):
    """
    Reset a session to initial state

    Args:
        session_id: The session identifier

    Returns:
        SessionResponse: Reset session state
    """
    session_service = get_session_service()
    session = session_service.reset_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    agent_info = get_agent_info(session.current_agent.name)

    return SessionResponse(
        session_id=session.session_id,
        current_agent=agent_info,
        context=session.context,
        created_at=session.created_at,
        message_count=session.message_count
    )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session

    Args:
        session_id: The session identifier

    Returns:
        dict: Confirmation message
    """
    session_service = get_session_service()
    success = session_service.delete_session(session_id)

    if not success:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"message": "Session deleted successfully"}


@router.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns:
        dict: Service health status
    """
    session_service = get_session_service()

    return {
        "status": "healthy",
        "service": "YourTeacher API",
        "active_sessions": session_service.get_session_count()
    }
