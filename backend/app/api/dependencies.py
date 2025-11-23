from app.infrastructure.db.memory_session_repo import MemorySessionRepository

# Global instance for now
_repo_instance = MemorySessionRepository()

def get_session_repo():
    return _repo_instance

