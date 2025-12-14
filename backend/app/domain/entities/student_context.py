from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class StudentLearningContext(BaseModel):
    student_name: Optional[str] = None
    age: Optional[int] = None
    grade_level: Optional[str] = None
    cognitive_ability: Optional[str] = None  # "High", "Medium", "Low"
    # "Visual", "Auditory", "Kinesthetic", "Mixed"
    learning_style: Optional[str] = None
    learning_pace: Optional[str] = None  # "Fast", "Medium", "Slow"
    subjects_of_interest: List[str] = []
    current_subject: Optional[str] = None
    current_topic: Optional[str] = None
    learning_objectives: List[str] = []
    quiz_score: Optional[int] = None
    quiz_total: Optional[int] = None
    student_profile: Dict[str, Any] = {}
    screening_complete: bool = False
    concept_taught: bool = False
    # Private attribute for internal logic
    _quiz_results: List[Dict[str, Any]] = []
