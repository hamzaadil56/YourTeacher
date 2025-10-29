"""
WebSocket endpoint for real-time streaming
"""
import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from app.services.session_service import get_session_service
from app.services.agent_service import AgentStreamingService

router = APIRouter(tags=["websocket"])


@router.websocket("/api/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for streaming agent responses

    Args:
        websocket: The WebSocket connection
        session_id: The session identifier
    """
    await websocket.accept()

    session_service = get_session_service()
    session = session_service.get_session(session_id)

    if not session:
        await websocket.send_json({
            "type": "error",
            "data": {"error": "Session not found"},
            "timestamp": None
        })
        await websocket.close(code=1008, reason="Session not found")
        return

    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "data": {
                "session_id": session_id,
                "agent_name": session.current_agent.name
            },
            "timestamp": None
        })

        # If this is a new session with initial message, process it
        if session.message_count == 0 and session.input_items:
            streaming_service = AgentStreamingService()

            async for event in streaming_service.process_initial_greeting(session):
                await websocket.send_json({
                    "type": event.type,
                    "data": event.data,
                    "timestamp": event.timestamp.isoformat() if event.timestamp else None
                })

        # Main message loop
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            message_type = message_data.get("type")
            message_content = message_data.get("content")

            if message_type == "message" and message_content:
                # Process the message with streaming
                streaming_service = AgentStreamingService()

                async for event in streaming_service.process_message_stream(
                    session,
                    message_content
                ):
                    await websocket.send_json({
                        "type": event.type,
                        "data": event.data,
                        "timestamp": event.timestamp.isoformat() if event.timestamp else None
                    })

            elif message_type == "ping":
                # Respond to ping for connection keepalive
                await websocket.send_json({
                    "type": "pong",
                    "data": {},
                    "timestamp": None
                })

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")

    except Exception as e:
        print(f"WebSocket error for session {session_id}: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "data": {"error": str(e)},
                "timestamp": None
            })
        except:
            pass
        finally:
            try:
                await websocket.close(code=1011, reason="Internal error")
            except:
                pass
