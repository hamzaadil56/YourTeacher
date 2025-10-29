"""
Student Learning Context Model
Maintains state across the learning session
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class StudentLearningContext(BaseModel):
    """Context for student learning session"""

    # Student Profile
    student_name: Optional[str] = None
    age: Optional[int] = None
    grade_level: Optional[str] = None
    cognitive_ability: Optional[str] = None  # "High", "Medium", "Low"
    # "Visual", "Auditory", "Kinesthetic", "Mixed"
    learning_style: Optional[str] = None
    learning_pace: Optional[str] = None  # "Fast", "Medium", "Slow"
    subjects_of_interest: List[str] = Field(default_factory=list)

    # Current Learning State
    current_subject: Optional[str] = None
    current_topic: Optional[str] = None
    learning_objectives: List[str] = Field(default_factory=list)

    # Quiz State
    quiz_score: Optional[int] = None
    quiz_total: Optional[int] = None

    # Comprehensive Profile
    student_profile: Dict[str, Any] = Field(default_factory=dict)

    # Workflow State
    screening_complete: bool = False
    concept_taught: bool = False

    # Internal Quiz Results (not exposed in API by default)
    quiz_results: List[Dict[str, Any]] = Field(
        default_factory=list, exclude=True)

    class Config:
        json_schema_extra = {
            "example": {
                "student_name": "Alex",
                "age": 16,
                "grade_level": "10th",
                "cognitive_ability": "High",
                "learning_style": "Visual",
                "learning_pace": "Fast",
                "subjects_of_interest": ["Mathematics", "Physics"],
                "screening_complete": True
            }
        }
