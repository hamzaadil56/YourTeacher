import random
from agents import RunContextWrapper, function_tool
from app.models.student import StudentLearningContext


@function_tool(
    name_override="cognitive_assessment_tool",
    description_override="Conduct cognitive ability assessment for students"
)
async def cognitive_assessment_tool(
    context: RunContextWrapper[StudentLearningContext],
    assessment_type: str,
    student_response: str
) -> str:
    """
    Assess student's cognitive abilities based on their responses.

    Args:
        assessment_type: Type of assessment (logical_reasoning, memory, problem_solving, comprehension)
        student_response: Student's response to the assessment question
    """
    assessment_type = assessment_type.lower()

    # Simulate cognitive assessment scoring
    if assessment_type == "logical_reasoning":
        if len(student_response) > 50 and any(word in student_response.lower() for word in ["because", "therefore", "if", "then", "since"]):
            score = random.randint(7, 10)
        else:
            score = random.randint(4, 7)
    elif assessment_type == "memory":
        if len(student_response) > 30:
            score = random.randint(6, 10)
        else:
            score = random.randint(3, 6)
    elif assessment_type == "problem_solving":
        if len(student_response) > 40 and any(word in student_response.lower() for word in ["step", "first", "next", "solution"]):
            score = random.randint(7, 10)
        else:
            score = random.randint(4, 7)
    else:  # comprehension
        score = random.randint(5, 9)

    # Determine cognitive ability level
    if score >= 8:
        ability = "High"
    elif score >= 6:
        ability = "Medium"
    else:
        ability = "Low"

    context.context.cognitive_ability = ability

    return f"Assessment '{assessment_type}' completed. Score: {score}/10. Cognitive ability level: {ability}"


@function_tool(
    name_override="save_student_profile",
    description_override="Save the complete student profile after screening"
)
async def save_student_profile(
    context: RunContextWrapper[StudentLearningContext],
    name: str,
    age: int,
    grade_level: str,
    learning_style: str,
    learning_pace: str,
    subjects_of_interest: str
) -> str:
    """
    Save the student's profile information.

    Args:
        name: Student's name
        age: Student's age
        grade_level: Student's grade level
        learning_style: Preferred learning style
        learning_pace: Preferred learning pace
        subjects_of_interest: Comma-separated list of subjects
    """
    context.context.student_name = name
    context.context.age = age
    context.context.grade_level = grade_level
    context.context.learning_style = learning_style
    context.context.learning_pace = learning_pace
    context.context.subjects_of_interest = [
        s.strip() for s in subjects_of_interest.split(",")]
    context.context.screening_complete = True

    # Create comprehensive profile
    context.context.student_profile = {
        "name": name,
        "age": age,
        "grade_level": grade_level,
        "cognitive_ability": context.context.cognitive_ability or "Medium",
        "learning_style": learning_style,
        "learning_pace": learning_pace,
        "subjects_of_interest": context.context.subjects_of_interest
    }

    return f"Student profile saved successfully for {name}. Ready for personalized learning!"
