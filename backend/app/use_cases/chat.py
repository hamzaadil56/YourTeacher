import json
import logging
from typing import AsyncGenerator

from agents import Runner, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent

from app.domain.interfaces.session_repository import ISessionRepository, SessionData
from app.domain.entities.student_context import StudentLearningContext
from app.infrastructure.agents.definitions import get_agent_by_name

logger = logging.getLogger(__name__)


async def chat_stream(
    session_id: str,
    user_message: str,
    repo: ISessionRepository
) -> AsyncGenerator[str, None]:

    # 1. Retrieve or Create Session
    session = await repo.get_session(session_id)
    if not session:
        session = SessionData(
            session_id=session_id,
            context=StudentLearningContext(),
            history=[],
            current_agent_name="Student Screener Agent"
        )
        # Add initial system/welcome logic if needed?
        # In main.py, it started with a user message "Hello! I'm ready..." to trigger the welcome.
        # But here the user sends the first message.
        # If history is empty, we might want to inject a hidden system prompt or just let the user start.
        # main.py: input_items.append({"content": "Hello! ...", "role": "user"}) -> this triggers the welcome.
        # If the user just opened the app, maybe we should treat empty history as "Start".

    # 2. Prepare Inputs
    current_agent = get_agent_by_name(session.current_agent_name)
    input_items = session.history.copy()

    # If it's a new session and user didn't say anything (or we want to trigger welcome),
    # we might handle that differently. But for now assume user sent a message.
    input_items.append({"role": "user", "content": user_message})

    # 3. Run Streaming
    # We yield a "start" event
    yield f"data: {json.dumps({'type': 'start', 'agent': current_agent.name})}\n\n"

    try:
        result = Runner.run_streamed(
            current_agent, input_items, context=session.context)

        current_message = ""

        async for event in result.stream_events():
            # Text Delta
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                if event.data.delta:
                    yield f"data: {json.dumps({'type': 'text_delta', 'content': event.data.delta})}\n\n"
                    current_message += event.data.delta

            # Agent Switch
            elif event.type == "agent_updated_stream_event":
                new_agent_name = event.new_agent.name
                if new_agent_name != session.current_agent_name:
                    yield f"data: {json.dumps({'type': 'agent_switch', 'from': session.current_agent_name, 'to': new_agent_name})}\n\n"
                    session.current_agent_name = new_agent_name

            # Tool Calls / Results
            elif event.type == "run_item_stream_event":
                item = event.item
                if item.type == "tool_call_item":
                    # function.name, function.arguments
                    yield f"data: {json.dumps({'type': 'tool_call', 'tool': item.function.name})}\n\n"

                elif item.type == "tool_call_output_item":
                    yield f"data: {json.dumps({'type': 'tool_result', 'output': item.output})}\n\n"

                    # Send updated context (subset) if needed, e.g. progress
                    # For now, we can send the whole profile if it changed, but maybe just on specific tools
                    if "profile" in item.output or "Assessment" in item.output:
                        yield f"data: {json.dumps({'type': 'context_update', 'data': session.context.model_dump(mode='json')})}\n\n"

        # 4. Save Session
        session.history = result.to_input_list()
        session.current_agent_name = result.last_agent.name
        await repo.save_session(session)

        yield f"data: {json.dumps({'type': 'end'})}\n\n"

    except Exception as e:
        logger.error(f"Error in chat stream: {e}")
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
