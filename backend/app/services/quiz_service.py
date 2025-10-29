from agents import RunContextWrapper, function_tool
from app.models.student import StudentLearningContext


@function_tool(
    name_override="generate_quiz",
    description_override="Generate a quiz based on the taught concept"
)
async def generate_quiz(
    context: RunContextWrapper[StudentLearningContext],
    difficulty_level: str,
    question_count: int
) -> str:
    """
    Generate a quiz for the current topic.

    Args:
        difficulty_level: Difficulty level (easy, medium, hard)
        question_count: Number of questions to generate
    """
    topic = context.context.current_topic
    cognitive_ability = context.context.cognitive_ability or "Medium"

    # Adjust difficulty based on cognitive ability
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
    """
    Evaluate a single quiz response.

    Args:
        question_number: Question number
        student_answer: Student's answer
        correct_answer: The correct answer
    """
    # Simple evaluation logic
    is_correct = student_answer.lower().strip() == correct_answer.lower().strip()

    if not context.context._quiz_results:
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
    """
    Calculate the final quiz score and determine if concept is understood.
    """
    if not context.context._quiz_results:
        return "No quiz results found"

    results = context.context._quiz_results
    total_questions = len(results)
    correct_answers = sum(1 for result in results if result["is_correct"])

    score_percentage = (correct_answers / total_questions) * \
        100 if total_questions > 0 else 0

    context.context.quiz_score = correct_answers
    context.context.quiz_total = total_questions

    # Reset quiz results after calculation
    context.context._quiz_results = []

    # Determine understanding level
    if score_percentage >= 80:
        understanding = "Excellent understanding! Ready for advanced topics."
    elif score_percentage >= 60:
        understanding = "Good understanding with some areas for improvement."
    else:
        understanding = "Concept needs reinforcement. Consider reviewing the material."

    return f"Quiz completed: {correct_answers}/{total_questions} ({score_percentage:.1f}%). {understanding}"
