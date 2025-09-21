"""
Example usage of the Educational Agent System

This file demonstrates how to use each agent individually and together.
"""

from agents import Runner
from your_teacher_agents import educational_system
import asyncio


async def example_screening_only():
    """Example: Using only the screening agent"""
    print("🔍 Example: Student Screening Only")
    print("-" * 40)

    screener = educational_system.get_screening_agent()

    # Example with initial student info
    student_info = {
        "name": "Sarah Chen",
        "age": 14,
        "current_grade": "9th",
        "subjects_of_interest": ["Biology", "Chemistry"],
        "learning_challenges": "Difficulty with mathematical concepts"
    }

    agent, prompt = screener.screen_student(student_info)
    result = Runner.run_sync(agent, prompt)

    print("Screening Result:")
    print(result.final_output)
    print("\n")


async def example_teaching_only():
    """Example: Using only the teaching agent"""
    print("👨‍🏫 Example: Personalized Teaching Only")
    print("-" * 40)

    teacher = educational_system.get_teaching_agent()

    # Example student profile (from previous screening)
    student_profile = {
        "grade": "9th",
        "field": "Life Sciences",
        "cognitive_ability": "Average",
        "learning_style": "Visual",
        "strengths": ["Memorization", "Pattern recognition"],
        "areas_for_improvement": ["Mathematical reasoning", "Abstract thinking"]
    }

    # Teaching Biology - Cell Structure
    agent, prompt = teacher.teach_student(
        student_profile=student_profile,
        subject="Biology",
        topic="Cell Structure and Function",
        learning_objectives=[
            "Identify major cell organelles",
            "Understand organelle functions",
            "Compare plant and animal cells"
        ]
    )

    result = Runner.run_sync(agent, prompt)

    print("Teaching Session:")
    print(result.final_output)
    print("\n")


async def example_feedback():
    """Example: Providing feedback on student work"""
    print("📝 Example: Providing Feedback")
    print("-" * 40)

    teacher = educational_system.get_teaching_agent()

    student_profile = {
        "grade": "10th",
        "field": "STEM",
        "cognitive_ability": "High",
        "learning_style": "Analytical"
    }

    # Student's work on a math problem
    student_work = """
    Problem: Solve for x: 2x² + 5x - 3 = 0
    
    My solution:
    Using the quadratic formula: x = (-b ± √(b²-4ac)) / 2a
    a = 2, b = 5, c = -3
    
    x = (-5 ± √(25 - 4(2)(-3))) / 2(2)
    x = (-5 ± √(25 + 24)) / 4
    x = (-5 ± √49) / 4
    x = (-5 ± 7) / 4
    
    So x = 2/4 = 0.5 or x = -12/4 = -3
    """

    agent, prompt = teacher.provide_feedback(
        student_profile=student_profile,
        student_work=student_work,
        subject="Mathematics"
    )

    result = Runner.run_sync(agent, prompt)

    print("Feedback:")
    print(result.final_output)
    print("\n")


async def example_coordination():
    """Example: Using the coordinator agent"""
    print("🔄 Example: Coordination and Progress Assessment")
    print("-" * 40)

    coordinator = educational_system.get_coordinator_agent()

    # Assess student progress
    student_profile = {
        "name": "Michael Rodriguez",
        "grade": "11th",
        "field": "Mathematics",
        "cognitive_ability": "High"
    }

    learning_history = [
        {"date": "2024-01-15", "topic": "Algebra", "performance": "Excellent"},
        {"date": "2024-01-20", "topic": "Geometry", "performance": "Good"},
        {"date": "2024-01-25", "topic": "Trigonometry",
            "performance": "Needs improvement"}
    ]

    current_performance = {
        "recent_scores": [85, 92, 78, 88],
        "engagement_level": "High",
        "time_spent_learning": "4 hours/week",
        "areas_of_struggle": ["Complex trigonometric identities"]
    }

    agent, prompt = coordinator.assess_progress(
        student_profile=student_profile,
        learning_history=learning_history,
        current_performance=current_performance
    )

    result = Runner.run_sync(agent, prompt)

    print("Progress Assessment:")
    print(result.final_output)
    print("\n")


async def main():
    """Run all examples"""
    print("🎓 Educational Agent System - Usage Examples")
    print("=" * 60)

    await example_screening_only()
    await example_teaching_only()
    await example_feedback()
    await example_coordination()

    print("✅ All examples completed!")

if __name__ == "__main__":
    asyncio.run(main())
