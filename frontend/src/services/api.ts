/**
 * API Service Layer
 * Handles all communication with the backend API including streaming
 */

import { StudentContext } from "@/models/StudentContext";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export interface ChatRequest {
  message: string;
  session_id: string;
}

export interface StreamEvent {
  type: "text" | "tool_use" | "tool_result" | "phase_change" | "error" | "done";
  data: any;
}

/**
 * Streams chat responses from the backend
 * Yields events as they arrive in real-time
 */
export async function* streamChat(
  sessionId: string,
  message: string
): AsyncGenerator<StreamEvent, void, unknown> {
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      message: message,
    }),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  if (!response.body) {
    throw new Error("Response body is null");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        yield { type: "done", data: null };
        break;
      }

      // Decode the chunk and add to buffer
      buffer += decoder.decode(value, { stream: true });

      // Process complete lines (SSE format)
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        const trimmedLine = line.trim();
        
        if (trimmedLine === "") continue;
        if (trimmedLine.startsWith(":")) continue; // SSE comment
        
        if (trimmedLine.startsWith("data: ")) {
          const data = trimmedLine.slice(6);
          
          if (data === "[DONE]") {
            yield { type: "done", data: null };
            continue;
          }

          try {
            const parsed = JSON.parse(data);
            
            // Handle different event types from the streaming API
            if (parsed.type === "text_delta") {
              // Backend sends text_delta with content field
              yield { type: "text", data: parsed.content };
            } else if (parsed.type === "text") {
              yield { type: "text", data: parsed.content };
            } else if (parsed.type === "start") {
              // Ignore start events
              continue;
            } else if (parsed.type === "end") {
              yield { type: "done", data: null };
            } else if (parsed.type === "agent_switch") {
              // Handle agent/phase changes
              yield { type: "phase_change", data: parsed };
            } else if (parsed.type === "tool_call") {
              yield { type: "tool_use", data: parsed };
            } else if (parsed.type === "tool_result") {
              yield { type: "tool_result", data: parsed };
            } else if (parsed.type === "context_update") {
              // Handle context updates (student profile changes)
              yield { type: "phase_change", data: parsed };
            } else if (parsed.type === "error") {
              yield { type: "error", data: parsed.message || "Unknown error" };
            }
            // Ignore any other event types silently
          } catch (e) {
            // If it's not JSON, treat it as plain text
            yield { type: "text", data: data };
          }
        }
      }
    }
  } catch (error) {
    yield { 
      type: "error", 
      data: error instanceof Error ? error.message : "Unknown error" 
    };
  } finally {
    reader.releaseLock();
  }
}

/**
 * Fetches session information
 */
export async function getSession(sessionId: string): Promise<StudentContext> {
  const response = await fetch(`${API_BASE_URL}/session/${sessionId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch session: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Resets a session
 */
export async function resetSession(sessionId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/session/${sessionId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to reset session: ${response.statusText}`);
  }
}

