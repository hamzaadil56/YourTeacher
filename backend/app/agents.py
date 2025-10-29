import os
from dotenv import load_dotenv

from agents import (
    Agent,
    handoff,
    RunContextWrapper,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    AsyncOpenAI
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from app.models.student import StudentLearningContext
from app.services.screening_service import cognitive_assessment_tool, save_student_profile
from app.services.teaching_service import set_learning_topic, generate_personalized_content
from app.services.quiz_service import generate_quiz, evaluate_quiz_response, calculate_quiz_score

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure agents SDK
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

if gemini_api_key:
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    set_default_openai_client(external_client)

# AGENT DEFINITIONS

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

# HANDOFF HOOKS and SETUP


async def on_teaching_handoff(context: RunContextWrapper[StudentLearningContext]) -> None:
    """Hook called when handing off to teaching agent"""
    if not context.context.screening_complete:
        raise ValueError("Student screening must be completed before teaching")


async def on_quiz_handoff(context: RunContextWrapper[StudentLearningContext]) -> None:
    """Hook called when handing off to quiz agent"""
    if not context.context.concept_taught:
        raise ValueError("A concept must be taught before taking a quiz")

screener_agent.handoffs = [
    handoff(agent=teaching_agent, on_handoff=on_teaching_handoff)
]

teaching_agent.handoffs = [
    screener_agent,
    handoff(agent=quiz_agent, on_handoff=on_quiz_handoff)
]

quiz_agent.handoffs = [
    teaching_agent,
    screener_agent
]

# A dictionary to easily access agents by name
agents_dict = {
    "Student Screener Agent": screener_agent,
    "Teaching Agent": teaching_agent,
    "Quiz Agent": quiz_agent,
}
