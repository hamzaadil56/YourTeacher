"""
Educational Agents Package

This package contains three main agents for personalized education:
1. StudentScreenerAgent - Assesses students on grade, field, and cognitive ability
2. PersonalizedTeachingAgent - Provides personalized teaching based on student profile
3. CoordinatorAgent - Manages workflow between agents and tracks progress
"""

from .screening_agent import StudentScreenerAgent
from .teaching_assistant_agent import PersonalizedTeachingAgent
from .coordinator_agent import CoordinatorAgent
from .global_agent_config import EducationalAgentSystem, educational_system

__all__ = [
    'StudentScreenerAgent',
    'PersonalizedTeachingAgent',
    'CoordinatorAgent',
    'EducationalAgentSystem',
    'educational_system'
]
