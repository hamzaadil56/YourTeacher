/**
 * Chat ViewModel Hook
 * Manages chat state and interactions with the API
 * Follows MVVM pattern - handles all business logic for chat
 */

"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { ChatMessage, createMessage, LearningPhase } from "@/models/ChatMessage";
import { Session, createSession } from "@/models/Session";
import { streamChat, getSession, resetSession as apiResetSession } from "@/services/api";

export interface ChatViewModel {
  session: Session;
  messages: ChatMessage[];
  isStreaming: boolean;
  isLoading: boolean;
  error: string | null;
  currentPhase: LearningPhase;
  sendMessage: (content: string) => Promise<void>;
  resetSession: () => Promise<void>;
  loadSession: (sessionId: string) => Promise<void>;
}

export function useChatViewModel(): ChatViewModel {
  const [session, setSession] = useState<Session>(() => createSession());
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPhase, setCurrentPhase] = useState<LearningPhase>("welcome");
  
  const streamingMessageRef = useRef<ChatMessage | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  /**
   * Sends a message and streams the response
   */
  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isStreaming) return;

    try {
      setError(null);
      setIsStreaming(true);

      // Add user message
      const userMessage = createMessage("user", content, currentPhase);
      setMessages(prev => [...prev, userMessage]);

      // Create a new streaming message for the assistant
      const assistantMessage = createMessage("assistant", "", currentPhase);
      assistantMessage.isStreaming = true;
      streamingMessageRef.current = assistantMessage;
      setMessages(prev => [...prev, assistantMessage]);

      // Stream the response
      let accumulatedContent = "";
      
      for await (const event of streamChat(session.id, content)) {
        if (event.type === "text") {
          accumulatedContent += event.data;
          
          // Update the streaming message
          setMessages(prev => {
            const updated = [...prev];
            const lastMessage = updated[updated.length - 1];
            if (lastMessage && lastMessage.id === assistantMessage.id) {
              lastMessage.content = accumulatedContent;
            }
            return updated;
          });
        } else if (event.type === "phase_change") {
          setCurrentPhase(event.data.phase);
          setSession(prev => ({
            ...prev,
            currentPhase: event.data.phase,
            updatedAt: new Date(),
          }));
        } else if (event.type === "error") {
          setError(event.data);
        } else if (event.type === "done") {
          // Finalize the message
          setMessages(prev => {
            const updated = [...prev];
            const lastMessage = updated[updated.length - 1];
            if (lastMessage && lastMessage.id === assistantMessage.id) {
              lastMessage.isStreaming = false;
            }
            return updated;
          });
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
      console.error("Error sending message:", err);
    } finally {
      setIsStreaming(false);
      streamingMessageRef.current = null;
    }
  }, [session.id, currentPhase, isStreaming]);

  /**
   * Resets the current session
   */
  const resetSession = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      await apiResetSession(session.id);
      
      // Create a new session
      const newSession = createSession();
      setSession(newSession);
      setMessages([]);
      setCurrentPhase("welcome");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to reset session");
      console.error("Error resetting session:", err);
    } finally {
      setIsLoading(false);
    }
  }, [session.id]);

  /**
   * Loads an existing session
   */
  const loadSession = useCallback(async (sessionId: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const context = await getSession(sessionId);
      
      setSession(prev => ({
        ...prev,
        id: sessionId,
        context,
        updatedAt: new Date(),
      }));
      
      // Determine current phase from context
      if (!context.screening_complete) {
        setCurrentPhase("screening");
      } else if (context.concept_taught) {
        setCurrentPhase("quiz");
      } else {
        setCurrentPhase("teaching");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load session");
      console.error("Error loading session:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Save session to localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("yourteacher_session_id", session.id);
    }
  }, [session.id]);

  return {
    session,
    messages,
    isStreaming,
    isLoading,
    error,
    currentPhase,
    sendMessage,
    resetSession,
    loadSession,
  };
}


