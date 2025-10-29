"""
Agent Streaming Service
Handles agent interactions and streaming responses
"""
from typing import AsyncGenerator, Dict, Any
from datetime import datetime
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from app.models.responses import StreamEvent
from app.models.context import StudentLearningContext
from app.agents import get_agent_info
from .session_service import SessionData


class AgentStreamingService:
    """Service for handling agent streaming interactions"""

    @staticmethod
    async def process_message_stream(
        session: SessionData,
        user_message: str
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        Process a user message and stream the agent's response

        Args:
            session: The session data
            user_message: The user's message

        Yields:
            StreamEvent: Events representing the streaming response
        """
        try:
            # Add user message to input items
            session.input_items.append({
                "content": user_message,
                "role": "user"
            })
            session.message_count += 1

            # Track previous agent for handoff detection
            previous_agent_name = session.current_agent.name

            # Use streaming runner
            streaming_result = Runner.run_streamed(
                session.current_agent,
                session.input_items,
                context=session.context
            )

            current_message = ""
            current_agent_name = previous_agent_name

            # Process streaming events
            async for event in streaming_result.stream_events():

                # Handle raw response events for real-time text streaming
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    if event.data.delta:
                        current_message += event.data.delta

                        # Send token event
                        yield StreamEvent(
                            type="token",
                            data={
                                "delta": event.data.delta,
                                "agent_name": current_agent_name,
                                "full_message": current_message
                            },
                            timestamp=datetime.now()
                        )

                # Handle agent updates
                elif event.type == "agent_updated_stream_event":
                    new_agent_name = event.new_agent.name

                    # Only send update if agent actually changed
                    if current_agent_name != new_agent_name:
                        agent_info = get_agent_info(new_agent_name)

                        yield StreamEvent(
                            type="agent_update",
                            data={
                                "previous_agent": current_agent_name,
                                "new_agent": new_agent_name,
                                "agent_info": agent_info.model_dump()
                            },
                            timestamp=datetime.now()
                        )

                    current_agent_name = new_agent_name

                # Handle run item events
                elif event.type == "run_item_stream_event":

                    if event.item.type == "tool_call_item":
                        agent_info = get_agent_info(event.item.agent.name)

                        yield StreamEvent(
                            type="tool_call",
                            data={
                                "agent_name": event.item.agent.name,
                                "icon": agent_info.icon,
                                "tool_name": getattr(event.item, 'tool_name', 'unknown')
                            },
                            timestamp=datetime.now()
                        )

                    elif event.item.type == "tool_call_output_item":
                        yield StreamEvent(
                            type="tool_result",
                            data={
                                "output": event.item.output
                            },
                            timestamp=datetime.now()
                        )

                    elif event.item.type == "message_output_item":
                        # Message complete
                        if current_message:
                            final_message = current_message
                        else:
                            # Fallback to item message
                            from agents import ItemHelpers
                            final_message = ItemHelpers.text_message_output(
                                event.item)

                        agent_info = get_agent_info(event.item.agent.name)

                        yield StreamEvent(
                            type="message_complete",
                            data={
                                "agent_name": event.item.agent.name,
                                "message": final_message,
                                "icon": agent_info.icon
                            },
                            timestamp=datetime.now()
                        )

                        # Reset current message
                        current_message = ""

                    elif event.item.type == "handoff_output_item":
                        source_name = event.item.source_agent.name
                        target_name = event.item.target_agent.name

                        # Only send if agents are different
                        if source_name != target_name:
                            source_info = get_agent_info(source_name)
                            target_info = get_agent_info(target_name)

                            yield StreamEvent(
                                type="handoff",
                                data={
                                    "source_agent": source_name,
                                    "target_agent": target_name,
                                    "source_info": source_info.model_dump(),
                                    "target_info": target_info.model_dump()
                                },
                                timestamp=datetime.now()
                            )

            # Update session with final state
            session.input_items = streaming_result.to_input_list()
            session.current_agent = streaming_result.last_agent
            session.message_count += 1

            # Send context update
            yield StreamEvent(
                type="context_update",
                data={
                    "context": session.context.model_dump(),
                    "current_agent": session.current_agent.name,
                    "message_count": session.message_count
                },
                timestamp=datetime.now()
            )

        except Exception as e:
            # Send error event
            yield StreamEvent(
                type="error",
                data={
                    "error": str(e),
                    "message": "An error occurred while processing your message"
                },
                timestamp=datetime.now()
            )

    @staticmethod
    async def process_initial_greeting(
        session: SessionData
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        Process initial greeting when session starts

        Args:
            session: The session data

        Yields:
            StreamEvent: Events representing the streaming response
        """
        async for event in AgentStreamingService.process_message_stream(
            session,
            "Hello! I'm ready to start my personalized learning journey."
        ):
            yield event
