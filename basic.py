
from agents import Agent, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api, Runner
from your_teacher_agents import educational_system
import asyncio
from pydantic import BaseModel


class AcademicQualification(BaseModel):
    name: str
    date: str
    grade: str
    field: str
    cognitive_ability: str
    learning_style: str
    strengths: list[str]
    areas_for_improvement: list[str]


# Configure OpenAI client
gemini_api_key = "AIzaSyAnL1jqcxeQzM5tRaE4GCKhStSdVkWlarY"
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

agent = Agent(
    name="Academic Qualification Agent",
    instructions="You are an agent that gets the student's academic qualification from the user.",
    model="gemini-2.0-flash",
)

result = Runner.run_sync(
    agent, "Please enter your highest academic qualification (e.g., High School, Bachelor's, Master's, PhD): If you doesn't got any information, please ask again and again until you get the information.")
print(result.final_output)
