"""
Request models for API endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional


class SessionCreateRequest(BaseModel):
    """Request to create a new learning session"""

    initial_message: Optional[str] = Field(
        default="Hello! I'm ready to start my personalized learning journey.",
        description="Initial message to start the session"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "initial_message": "Hello! I'm ready to start my personalized learning journey."
            }
        }


class MessageRequest(BaseModel):
    """Request to send a message to the agent"""

    content: str = Field(
        ...,
        description="Message content from the user",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "content": "My name is Alex and I'm 16 years old."
            }
        }
