"use client";

import { useEffect, useRef } from "react";
import { ChatMessage as ChatMessageType } from "@/models/ChatMessage";
import { ChatMessage } from "./ChatMessage";
import { Spinner } from "@/components/ui/spinner";

interface ChatContainerProps {
  messages: ChatMessageType[];
  isLoading?: boolean;
}

export function ChatContainer({ messages, isLoading }: ChatContainerProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto px-4 py-6 space-y-4"
    >
      <div className="container max-w-4xl mx-auto">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center py-12">
            <div className="rounded-full bg-gradient-to-br from-[rgb(var(--primary))] to-[rgb(var(--accent))] p-6 mb-6">
              <svg
                className="h-12 w-12 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
            </div>
            <h2 className="font-[var(--font-display)] text-2xl font-bold mb-2">
              Welcome to YourTeacher
            </h2>
            <p className="text-[rgb(var(--muted-foreground))] max-w-md">
              Start your personalized learning journey! I'll assess your learning
              style, teach you new concepts, and help you master them through
              interactive quizzes.
            </p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="flex justify-center py-4">
                <Spinner size="md" />
              </div>
            )}
          </>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}


