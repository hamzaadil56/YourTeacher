from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.domain.entities.student_context import StudentLearningContext

class SessionData(BaseModel):
    session_id: str
    context: StudentLearningContext
    history: List[Dict[str, Any]] # List of message dicts
    current_agent_name: str

class ISessionRepository(ABC):
    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        pass

    @abstractmethod
    async def save_session(self, session: SessionData) -> None:
        pass
