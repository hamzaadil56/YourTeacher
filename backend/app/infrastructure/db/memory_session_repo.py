from typing import Dict, Optional
from app.domain.interfaces.session_repository import ISessionRepository, SessionData
from app.domain.entities.student_context import StudentLearningContext

class MemorySessionRepository(ISessionRepository):
    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}

    async def get_session(self, session_id: str) -> Optional[SessionData]:
        return self._sessions.get(session_id)

    async def save_session(self, session: SessionData) -> None:
        self._sessions[session.session_id] = session

