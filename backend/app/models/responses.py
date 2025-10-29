"""
Response models for API endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Literal
from datetime import datetime
from .context import StudentLearningContext


class AgentInfo(BaseModel):
    """Information about an agent"""

    name: str
    icon: str
    description: str
    phase: str
    color: str


class SessionResponse(BaseModel):
    """Response for session creation/retrieval"""

    session_id: str
    current_agent: AgentInfo
    context: StudentLearningContext
    created_at: datetime
    message_count: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "abc123def456",
                "current_agent": {
                    "name": "Student Screener Agent",
                    "icon": "🔍",
                    "description": "Assessing your learning profile",
                    "phase": "Assessment Phase",
                    "color": "purple"
                },
                "context": {
                    "screening_complete": False
                },
                "created_at": "2024-01-01T00:00:00",
                "message_count": 0
            }
        }


class MessageResponse(BaseModel):
    """Response for a single message exchange"""

    session_id: str
    agent_name: str
    response: str
    context: StudentLearningContext

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "abc123def456",
                "agent_name": "Student Screener Agent",
                "response": "Hello! Let's begin your assessment...",
                "context": {
                    "screening_complete": False
                }
            }
        }


class StreamEvent(BaseModel):
    """Event sent through WebSocket stream"""

    type: Literal[
        "token",           # Text token delta
        "agent_update",    # Agent changed
        "tool_call",       # Tool being called
        "tool_result",     # Tool execution result
        "handoff",         # Agent handoff
        "message_complete",  # Message finished
        "error",          # Error occurred
        "context_update"  # Context state changed
    ]
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "type": "token",
                "data": {
                    "delta": "Hello",
                    "agent_name": "Student Screener Agent"
                },
                "timestamp": "2024-01-01T00:00:00"
            }
        }
