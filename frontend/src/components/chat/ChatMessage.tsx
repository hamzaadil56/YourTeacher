"use client";

import { ChatMessage as ChatMessageType } from "@/models/ChatMessage";
import { cn } from "@/lib/utils";
import { User, Bot } from "lucide-react";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";
  const isStreaming = message.isStreaming;

  return (
    <div
      className={cn(
        "flex gap-4 p-4 rounded-xl animate-slide-up",
        isUser
          ? "bg-[rgb(var(--primary))]/5 ml-8"
          : "bg-[rgb(var(--muted))] mr-8"
      )}
    >
      <div
        className={cn(
          "flex h-10 w-10 shrink-0 items-center justify-center rounded-full",
          isUser
            ? "bg-[rgb(var(--primary))] text-white"
            : "bg-[rgb(var(--accent))] text-white"
        )}
      >
        {isUser ? <User className="h-5 w-5" /> : <Bot className="h-5 w-5" />}
      </div>

      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-sm">
            {isUser ? "You" : "YourTeacher"}
          </span>
          <span className="text-xs text-[rgb(var(--muted-foreground))]">
            {message.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
          {isStreaming && (
            <span className="text-xs text-[rgb(var(--primary))] animate-pulse-glow">
              Thinking...
            </span>
          )}
        </div>

        <div className="prose prose-sm max-w-none">
          <p className="whitespace-pre-wrap text-[rgb(var(--foreground))]">
            {message.content}
            {isStreaming && <span className="animate-pulse-glow ml-1">▋</span>}
          </p>
        </div>
      </div>
    </div>
  );
}


