"""
Global configuration for all educational agents.
"""

from .screening_agent import StudentScreenerAgent
from .teaching_assistant_agent import PersonalizedTeachingAgent
from .coordinator_agent import CoordinatorAgent


class EducationalAgentSystem:
    """
    Main system that manages all educational agents.
    """

    def __init__(self):
        self.screening_agent = StudentScreenerAgent()
        self.teaching_agent = PersonalizedTeachingAgent()
        self.coordinator_agent = CoordinatorAgent()

    def get_screening_agent(self):
        """Get the student screening agent."""
        return self.screening_agent

    def get_teaching_agent(self):
        """Get the personalized teaching agent."""
        return self.teaching_agent

    def get_coordinator_agent(self):
        """Get the coordinator agent."""
        return self.coordinator_agent

    def get_all_agents(self):
        """Get all agents as a dictionary."""
        return {
            'screening': self.screening_agent,
            'teaching': self.teaching_agent,
            'coordinator': self.coordinator_agent
        }


# Global instance
educational_system = EducationalAgentSystem()
