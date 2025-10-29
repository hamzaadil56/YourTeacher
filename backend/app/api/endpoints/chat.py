import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, AsyncGenerator

from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent

from app.models.student import StudentLearningContext
from app.agents import agents_dict, screener_agent

router = APIRouter()


class ChatRequest(BaseModel):
    input_items: List[Dict[str, Any]]
    context: StudentLearningContext
    current_agent_name: str | None = None


async def event_stream(request: ChatRequest) -> AsyncGenerator[str, None]:
    if request.current_agent_name and request.current_agent_name in agents_dict:
        current_agent = agents_dict[request.current_agent_name]
    else:
        current_agent = screener_agent

    try:
        result_stream = Runner.run_streamed(
            current_agent,
            request.input_items,
            context=request.context,
        )

        async for event in result_stream.stream_events():
            # Convert event to a dictionary
            event_data = {
                "type": event.type,
                "data": {}
            }
            if hasattr(event, 'item') and event.item:
                event_data["data"]["item"] = event.item.model_dump(
                    exclude_none=True) if hasattr(event.item, 'model_dump') else str(event.item)
            if hasattr(event, 'new_agent') and event.new_agent:
                event_data["data"]["new_agent"] = event.new_agent.model_dump(
                    exclude_none=True) if hasattr(event.new_agent, 'model_dump') else str(event.new_agent)

            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                event_data["data"]["delta"] = event.data.delta

            # Send event as a Server-Sent Event (SSE)
            yield f"data: {json.dumps(event_data)}\n\n"

        # After streaming, get the final result
        final_result = result_stream

        # Send a final 'end' event with the complete result
        final_data = {
            "type": "end",
            "data": {
                "last_agent": final_result.last_agent.model_dump(exclude_none=True),
                "final_context": final_result.context.model_dump(exclude_none=True),
                "input_list": final_result.to_input_list()
            }
        }
        yield f"data: {json.dumps(final_data)}\n\n"

    except Exception as e:
        error_data = {"type": "error", "data": {"message": str(e)}}
        yield f"data: {json.dumps(error_data)}\n\n"


@router.post("/chat/streaming")
async def chat_streaming(request: ChatRequest):
    return StreamingResponse(event_stream(request), media_type="text/event-stream")
