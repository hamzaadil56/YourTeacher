"""
Agent Definitions - Three specialized AI agents
"""
from agents import Agent, handoff, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from app.models.context import StudentLearningContext
from app.models.responses import AgentInfo
from .tools import (
    cognitive_assessment_tool,
    save_student_profile,
    set_learning_topic,
    generate_personalized_content,
    generate_quiz,
    evaluate_quiz_response,
    calculate_quiz_score
)


# ============================================================================
# HANDOFF HOOKS
# ============================================================================

async def on_teaching_handoff(context: RunContextWrapper[StudentLearningContext]) -> None:
    """Hook called when handing off to teaching agent"""
    if not context.context.screening_complete:
        raise ValueError("Student screening must be completed before teaching")


async def on_quiz_handoff(context: RunContextWrapper[StudentLearningContext]) -> None:
    """Hook called when handing off to quiz agent"""
    if not context.context.concept_taught:
        raise ValueError("A concept must be taught before taking a quiz")


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

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


# ============================================================================
# AGENT UTILITIES
# ============================================================================

def get_agent_info(agent_name: str) -> AgentInfo:
    """Get agent information for display"""
    agent_info_map = {
        "Student Screener Agent": AgentInfo(
            name="Student Screener Agent",
            icon="🔍",
            description="Assessing your learning profile and cognitive abilities",
            phase="Assessment Phase",
            color="purple"
        ),
        "Teaching Agent": AgentInfo(
            name="Teaching Agent",
            icon="👨‍🏫",
            description="Providing personalized lessons based on your profile",
            phase="Learning Phase",
            color="blue"
        ),
        "Quiz Agent": AgentInfo(
            name="Quiz Agent",
            icon="📝",
            description="Testing your understanding with customized quizzes",
            phase="Validation Phase",
            color="green"
        )
    }

    return agent_info_map.get(agent_name, AgentInfo(
        name=agent_name,
        icon="🤖",
        description="AI Assistant",
        phase="Active",
        color="gray"
    ))
