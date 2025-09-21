from agents import AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api, Runner
from your_teacher_agents import educational_system
import asyncio

# Configure OpenAI client
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)


def main():
    """
    Demonstration of the Educational Agent System
    """
    print("🎓 Welcome to YourTeacher - Personalized Education System")
    print("=" * 60)

    # Example student information
    student_info = {
        "name": "Alex Johnson",
        "age": 15,
        "current_grade": "10th",
        "subjects_of_interest": ["Mathematics", "Physics"],
        "previous_performance": "Above average in STEM subjects"
    }

    print(f"📋 Processing new student: {student_info['name']}")
    print("-" * 40)

    # Step 1: Coordinate new student onboarding
    coordinator = educational_system.get_coordinator_agent()
    coord_agent, coord_prompt = coordinator.coordinate_new_student(
        student_info)

    print("🔄 Coordinator Agent: Planning onboarding process...")
    coord_result = Runner.run_sync(coord_agent, coord_prompt)
    print("Coordination Plan:")
    print(coord_result.final_output)
    print("\n" + "=" * 60)

    # Step 2: Screen the student
    screener = educational_system.get_screening_agent()
    screen_agent, screen_prompt = screener.screen_student(student_info)

    print("🔍 Screening Agent: Assessing student profile...")
    screen_result = Runner.run_sync(screen_agent, screen_prompt)
    print("Student Assessment:")
    print(screen_result.final_output)
    print("\n" + "=" * 60)

    # Step 3: Provide personalized teaching
    teacher = educational_system.get_teaching_agent()

    # Example student profile (would normally come from screening results)
    student_profile = {
        "grade": "10th",
        "field": "STEM",
        "cognitive_ability": "High",
        "learning_style": "Visual-Kinesthetic",
        "strengths": ["Problem-solving", "Logical reasoning"],
        "areas_for_improvement": ["Written communication", "Time management"]
    }

    # Teaching session for Mathematics - Quadratic Equations
    teach_agent, teach_prompt = teacher.teach_student(
        student_profile=student_profile,
        subject="Mathematics",
        topic="Quadratic Equations",
        learning_objectives=[
            "Understand quadratic formula", "Solve real-world problems"]
    )

    print("👨‍🏫 Teaching Agent: Providing personalized lesson...")
    teach_result = Runner.run_sync(teach_agent, teach_prompt)
    print("Personalized Lesson:")
    print(teach_result.final_output)
    print("\n" + "=" * 60)

    print("✅ Educational session completed successfully!")
    print("The system has demonstrated:")
    print("• Student screening and assessment")
    print("• Personalized teaching adaptation")
    print("• Coordinated workflow management")


if __name__ == "__main__":
    main()
