from agents import RunContextWrapper, function_tool
from app.models.student import StudentLearningContext


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
    """
    Set the current learning topic and objectives.

    Args:
        subject: The subject to teach
        topic: The specific topic within the subject
        objectives: Learning objectives (comma-separated)
    """
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
    """
    Generate personalized learning content.

    Args:
        content_type: Type of content (explanation, example, exercise, visual_aid)
    """
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
