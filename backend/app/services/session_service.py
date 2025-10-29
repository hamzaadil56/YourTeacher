"""
Session Management Service
Handles session creation, storage, and lifecycle
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from app.models.context import StudentLearningContext
from app.agents import screener_agent
from agents import Agent, TResponseInputItem


class SessionData:
    """Data structure for a learning session"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.context = StudentLearningContext()
        self.current_agent: Agent[StudentLearningContext] = screener_agent
        self.input_items: List[TResponseInputItem] = []
        self.message_count = 0

    def update_access_time(self):
        """Update the last accessed time"""
        self.last_accessed = datetime.now()


class SessionService:
    """Service for managing learning sessions"""

    def __init__(self, timeout_minutes: int = 60):
        self.sessions: Dict[str, SessionData] = {}
        self.timeout_minutes = timeout_minutes

    def create_session(self, initial_message: Optional[str] = None) -> SessionData:
        """
        Create a new learning session

        Args:
            initial_message: Optional initial message to start the conversation

        Returns:
            SessionData: The newly created session
        """
        session_id = uuid.uuid4().hex[:16]
        session = SessionData(session_id)

        # Add initial message if provided
        if initial_message:
            session.input_items.append({
                "content": initial_message,
                "role": "user"
            })

        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SessionData]:
        """
        Get a session by ID

        Args:
            session_id: The session identifier

        Returns:
            Optional[SessionData]: The session data if found, None otherwise
        """
        session = self.sessions.get(session_id)
        if session:
            session.update_access_time()
        return session

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session

        Args:
            session_id: The session identifier

        Returns:
            bool: True if session was deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def reset_session(self, session_id: str) -> Optional[SessionData]:
        """
        Reset a session to initial state

        Args:
            session_id: The session identifier

        Returns:
            Optional[SessionData]: The reset session if found, None otherwise
        """
        if session_id in self.sessions:
            session = SessionData(session_id)
            self.sessions[session_id] = session
            return session
        return None

    def cleanup_expired_sessions(self):
        """Remove sessions that have exceeded the timeout period"""
        current_time = datetime.now()
        expired_sessions = [
            session_id
            for session_id, session in self.sessions.items()
            if current_time - session.last_accessed > timedelta(minutes=self.timeout_minutes)
        ]

        for session_id in expired_sessions:
            del self.sessions[session_id]

        return len(expired_sessions)

    def get_session_count(self) -> int:
        """Get the total number of active sessions"""
        return len(self.sessions)


# Global session service instance
_session_service: Optional[SessionService] = None


def get_session_service() -> SessionService:
    """Get the global session service instance"""
    global _session_service
    if _session_service is None:
        _session_service = SessionService()
    return _session_service
