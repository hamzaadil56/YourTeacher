/**
 * Chat Message Model
 * Represents a single message in the learning conversation
 */

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
  phase?: LearningPhase;
  isStreaming?: boolean;
}

export type LearningPhase = "screening" | "teaching" | "quiz" | "welcome";

/**
 * Creates a new chat message
 */
export const createMessage = (
  role: ChatMessage["role"],
  content: string,
  phase?: LearningPhase
): ChatMessage => ({
  id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
  role,
  content,
  timestamp: new Date(),
  phase,
  isStreaming: false,
});

