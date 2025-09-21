from __future__ import annotations as _annotations

import asyncio
import random
import uuid
import json
from typing import Dict, Any, List

from pydantic import BaseModel
from openai.types.responses import ResponseTextDeltaEvent

from agents import (
    Agent,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    RunContextWrapper,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    handoff,
    trace,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    AsyncOpenAI
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)


# CONTEXT - Student Learning Context
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

    if not hasattr(context.context, '_quiz_results'):
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
    if not hasattr(context.context, '_quiz_results'):
        return "No quiz results found"

    results = context.context._quiz_results
    total_questions = len(results)
    correct_answers = sum(1 for result in results if result["is_correct"])

    score_percentage = (correct_answers / total_questions) * \
        100 if total_questions > 0 else 0

    context.context.quiz_score = correct_answers
    context.context.quiz_total = total_questions

    # Determine understanding level
    if score_percentage >= 80:
        understanding = "Excellent understanding! Ready for advanced topics."
    elif score_percentage >= 60:
        understanding = "Good understanding with some areas for improvement."
    else:
        understanding = "Concept needs reinforcement. Consider reviewing the material."

    return f"Quiz completed: {correct_answers}/{total_questions} ({score_percentage:.1f}%). {understanding}"


# HANDOFF HOOKS

async def on_teaching_handoff(context: RunContextWrapper[StudentLearningContext]) -> None:
    """Hook called when handing off to teaching agent"""
    if not context.context.screening_complete:
        raise ValueError("Student screening must be completed before teaching")


async def on_quiz_handoff(context: RunContextWrapper[StudentLearningContext]) -> None:
    """Hook called when handing off to quiz agent"""
    if not context.context.concept_taught:
        raise ValueError("A concept must be taught before taking a quiz")


# AGENTS

screener_agent = Agent[StudentLearningContext](
    name="Student Screener Agent",
    handoff_description="Agent responsible for comprehensive student assessment and profile creation",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a Student Screener Agent responsible for comprehensive student assessment.
    
    Your routine:
    1. Welcome the student warmly and explain the screening process
    2. Collect basic information: name, age, grade level
    3. Assess cognitive abilities through targeted questions:
       - Logical reasoning: Present a simple logic problem
       - Memory: Ask them to remember and repeat information
       - Problem-solving: Give a practical problem to solve
       - Comprehension: Test understanding of a short passage
    4. Identify learning preferences (visual, auditory, kinesthetic, mixed)
    5. Determine preferred learning pace (fast, medium, slow)
    6. Ask about subjects of interest
    7. Use tools to assess responses and save the complete profile
    8. Once screening is complete, hand off to the teaching agent
    
    Be encouraging, supportive, and make the assessment feel conversational, not intimidating.
    Use the cognitive_assessment_tool for each assessment type and save_student_profile when complete.
    """,
    tools=[cognitive_assessment_tool, save_student_profile],
    model="gemini-2.0-flash",
)

teaching_agent = Agent[StudentLearningContext](
    name="Teaching Agent",
    handoff_description="Agent that provides personalized teaching based on student profile",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a Teaching Agent that provides personalized education based on student profiles.
    
    Your routine:
    1. Review the student's profile and greet them personally
    2. Ask what subject and topic they'd like to learn about
    3. Set the learning topic and objectives using the appropriate tool
    4. Adapt your teaching style based on their profile:
       - Cognitive ability (High/Medium/Low): Adjust complexity
       - Learning style (Visual/Auditory/Kinesthetic/Mixed): Choose appropriate methods
       - Learning pace (Fast/Medium/Slow): Adjust speed and detail
    5. Use generate_personalized_content to create tailored explanations
    6. Provide examples, exercises, and check for understanding
    7. Once the concept is well explained and student shows understanding, hand off to quiz agent
    
    Always be patient, encouraging, and adapt your teaching in real-time based on student responses.
    """,
    tools=[set_learning_topic, generate_personalized_content],
    model="gemini-2.0-flash",
)

quiz_agent = Agent[StudentLearningContext](
    name="Quiz Agent",
    handoff_description="Agent that creates and evaluates quizzes to validate concept understanding",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a Quiz Agent that validates student understanding through assessments.
    
    Your routine:
    1. Review the taught topic and student's cognitive ability
    2. Generate an appropriate quiz using the generate_quiz tool
    3. Ask questions one by one, adapted to the student's level
    4. Evaluate each response using evaluate_quiz_response
    5. Provide immediate feedback for each answer
    6. After all questions, calculate the final score
    7. Based on the score:
       - 80%+: Congratulate and offer to teach a new topic (hand back to teaching agent)
       - 60-79%: Provide encouragement and offer review or new topic
       - <60%: Recommend reviewing the concept (hand back to teaching agent)
    
    Make the quiz engaging and provide constructive feedback. Celebrate successes and encourage improvement.
    """,
    tools=[generate_quiz, evaluate_quiz_response, calculate_quiz_score],
    model="gemini-2.0-flash",
)

# Set up handoffs
screener_agent.handoffs = [
    handoff(agent=teaching_agent, on_handoff=on_teaching_handoff)
]

teaching_agent.handoffs = [
    screener_agent,  # Can go back for re-assessment if needed
    handoff(agent=quiz_agent, on_handoff=on_quiz_handoff)
]

quiz_agent.handoffs = [
    teaching_agent,  # Go back to teaching for review or new topics
    screener_agent   # Go back to screener if profile needs updating
]


# STREAMING FUNCTIONS

async def process_streaming_response(streaming_result, previous_agent_name=None):
    """
    Process streaming response with real-time updates
    """
    current_message = ""
    current_agent_name = previous_agent_name or ""

    print("🔄 Processing agent response...")

    async for event in streaming_result.stream_events():
        # Handle raw response events for real-time text streaming
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            if event.data.delta:
                print(event.data.delta, end="", flush=True)
                current_message += event.data.delta

        # Handle agent updates - only show if agent actually changed
        elif event.type == "agent_updated_stream_event":
            new_agent_name = event.new_agent.name
            # Only show handoff if agent actually changed
            if current_agent_name and new_agent_name != current_agent_name:
                print(
                    f"\n\n🔄 Agent Handoff: {current_agent_name} → {new_agent_name}")
                print("-" * 50)
            current_agent_name = new_agent_name

        # Handle run item events for structured updates
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print(f"\n🔧 {current_agent_name or 'Agent'}: Using a tool...")

            elif event.item.type == "tool_call_output_item":
                print(f"✅ Tool Result: {event.item.output}")

            elif event.item.type == "message_output_item":
                if current_message:
                    print(
                        f"\n\n🤖 {current_agent_name or 'Agent'}: {current_message}")
                    current_message = ""
                else:
                    message = ItemHelpers.text_message_output(event.item)
                    print(f"\n🤖 {current_agent_name or 'Agent'}: {message}")

            elif event.item.type == "handoff_output_item":
                # Only show handoff if agents are actually different
                source_name = event.item.source_agent.name
                target_name = event.item.target_agent.name
                if source_name != target_name:
                    print(f"\n🔄 Handoff: {source_name} → {target_name}")

    # Print any remaining message content
    if current_message:
        print(f"\n🤖 {current_agent_name or 'Agent'}: {current_message}")

    return streaming_result


# MAIN APPLICATION WITH STREAMING

async def main():
    """
    Main educational application with streaming support
    """
    print("🎓 Welcome to YourTeacher - AI-Powered Personalized Learning System (Streaming)")
    print("=" * 80)
    print("This system will:")
    print("1. 📋 Assess your learning profile and cognitive abilities")
    print("2. 👨‍🏫 Provide personalized teaching based on your profile")
    print("3. 📝 Test your understanding with customized quizzes")
    print("4. 🔄 Stream responses in real-time for better experience")
    print("=" * 80)

    # Initialize the system
    current_agent: Agent[StudentLearningContext] = screener_agent
    input_items: list[TResponseInputItem] = []
    context = StudentLearningContext()

    # Generate unique conversation ID for tracing
    conversation_id = uuid.uuid4().hex[:16]

    # Start with welcome message
    input_items.append({
        "content": "Hello! I'm ready to start my personalized learning journey.",
        "role": "user"
    })

    print("\n🤖 Starting your personalized learning journey...")
    print("-" * 50)

    while True:
        try:
            with trace("Educational System Streaming", group_id=conversation_id):
                # Use streaming runner instead of regular runner
                result = Runner.run_streamed(
                    current_agent, input_items, context=context)

                # Track previous agent name for handoff detection
                previous_agent_name = current_agent.name

                # Process streaming response
                final_result = await process_streaming_response(result, previous_agent_name)

                # Update for next iteration
                input_items = final_result.to_input_list()
                current_agent = final_result.last_agent

                # Get user input
                print(f"\n📝 Your response to {current_agent.name}:")
                user_input = input(">>> ").strip()

                # Handle exit conditions
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print(
                        f"\n🎓 Thank you for using YourTeacher, {context.student_name or 'Student'}!")
                    print("Keep learning and growing! 🌟")
                    break

                # Add user input for next iteration
                input_items.append({"content": user_input, "role": "user"})

        except KeyboardInterrupt:
            print(f"\n\n🎓 Session ended. Thank you for using YourTeacher!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or type 'quit' to exit.")

            # Get user input to continue or quit
            user_input = input(">>> ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
            input_items.append({"content": user_input, "role": "user"})


if __name__ == "__main__":
    asyncio.run(main())
