import random
from agents import function_tool, RunContextWrapper
from app.domain.entities.student_context import StudentLearningContext

# TOOLS FOR SCREENING AGENT

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


# TOOLS FOR TEACHING AGENT

@function_tool(
    name_override="set_learning_topic",
    description_override="Set the current learning topic and objectives"
)
async def set_learning_topic(
    context: RunContextWrapper[StudentLearningContext],
    subject: str,
    topic: str,
    objectives: str
) -> str:
    context.context.current_subject = subject
    context.context.current_topic = topic
    context.context.learning_objectives = [
        obj.strip() for obj in objectives.split(",")]

    return f"Learning topic set: {subject} - {topic}. Objectives: {objectives}"


@function_tool(
    name_override="generate_personalized_content",
    description_override="Generate personalized learning content based on student profile"
)
async def generate_personalized_content(
    context: RunContextWrapper[StudentLearningContext],
    content_type: str
) -> str:
    profile = context.context.student_profile
    topic = context.context.current_topic
    cognitive_ability = profile.get("cognitive_ability", "Medium")
    learning_style = profile.get("learning_style", "Mixed")

    if content_type == "explanation":
        if cognitive_ability == "High":
            complexity = "advanced concepts with detailed analysis"
        elif cognitive_ability == "Medium":
            complexity = "moderate complexity with clear examples"
        else:
            complexity = "simple, step-by-step explanations"

        if learning_style == "Visual":
            approach = "with diagrams, charts, and visual representations"
        elif learning_style == "Auditory":
            approach = "with verbal explanations and discussions"
        elif learning_style == "Kinesthetic":
            approach = "with hands-on examples and practical applications"
        else:
            approach = "using multiple teaching methods"

        return f"Generated personalized explanation for {topic} using {complexity} {approach}"

    context.context.concept_taught = True
    return f"Generated {content_type} content for {topic} tailored to {learning_style} learner with {cognitive_ability} cognitive ability"


# TOOLS FOR QUIZ AGENT

@function_tool(
    name_override="generate_quiz",
    description_override="Generate a quiz based on the taught concept"
)
async def generate_quiz(
    context: RunContextWrapper[StudentLearningContext],
    difficulty_level: str,
    question_count: int
) -> str:
    topic = context.context.current_topic
    cognitive_ability = context.context.cognitive_ability or "Medium"

    if cognitive_ability == "High" and difficulty_level == "easy":
        difficulty_level = "medium"
    elif cognitive_ability == "Low" and difficulty_level == "hard":
        difficulty_level = "medium"

    return f"Generated {question_count} {difficulty_level} questions for {topic} quiz tailored to {cognitive_ability} cognitive ability"


@function_tool(
    name_override="evaluate_quiz_response",
    description_override="Evaluate student's quiz responses"
)
async def evaluate_quiz_response(
    context: RunContextWrapper[StudentLearningContext],
    question_number: int,
    student_answer: str,
    correct_answer: str
) -> str:
    is_correct = student_answer.lower().strip() == correct_answer.lower().strip()

    if not hasattr(context.context, '_quiz_results') or context.context._quiz_results is None:
        context.context._quiz_results = []

    context.context._quiz_results.append({
        "question": question_number,
        "student_answer": student_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct
    })

    return f"Question {question_number}: {'Correct' if is_correct else 'Incorrect'}"


@function_tool(
    name_override="calculate_quiz_score",
    description_override="Calculate final quiz score and provide feedback"
)
async def calculate_quiz_score(
    context: RunContextWrapper[StudentLearningContext]
) -> str:
    if not hasattr(context.context, '_quiz_results') or not context.context._quiz_results:
        return "No quiz results found"

    results = context.context._quiz_results
    total_questions = len(results)
    correct_answers = sum(1 for result in results if result["is_correct"])

    score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    context.context.quiz_score = correct_answers
    context.context.quiz_total = total_questions

    if score_percentage >= 80:
        understanding = "Excellent understanding! Ready for advanced topics."
    elif score_percentage >= 60:
        understanding = "Good understanding with some areas for improvement."
    else:
        understanding = "Concept needs reinforcement. Consider reviewing the material."

    return f"Quiz completed: {correct_answers}/{total_questions} ({score_percentage:.1f}%). {understanding}"

