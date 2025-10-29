from pydantic import BaseModel
from typing import Dict, Any, List


class StudentLearningContext(BaseModel):
    student_name: str | None = None
    age: int | None = None
    grade_level: str | None = None
    cognitive_ability: str | None = None  # "High", "Medium", "Low"
    learning_style: str | None = None  # "Visual", "Auditory", "Kinesthetic", "Mixed"
    learning_pace: str | None = None  # "Fast", "Medium", "Slow"
    subjects_of_interest: List[str] = []
    current_subject: str | None = None
    current_topic: str | None = None
    learning_objectives: List[str] = []
    quiz_score: int | None = None
    quiz_total: int | None = None
    student_profile: Dict[str, Any] = {}
    screening_complete: bool = False
    concept_taught: bool = False

    # This is a temporary field used by the quiz agent to store results
    # It's not part of the core student profile. The underscore indicates a private-like attribute.
    _quiz_results: List[Dict[str, Any]] = []
