"use client";

import { useEffect, useState } from "react";
import { useChatViewModel } from "@/viewmodels/useChatViewModel";
import { useStudentViewModel } from "@/viewmodels/useStudentViewModel";
import { Header } from "@/components/layout/Header";
import { WelcomeScreen } from "@/components/phases/WelcomeScreen";
import { PhaseIndicator } from "@/components/phases/PhaseIndicator";
import { StudentProfileCard } from "@/components/phases/StudentProfileCard";
import { ChatContainer } from "@/components/chat/ChatContainer";
import { ChatInput } from "@/components/chat/ChatInput";
import { createMessage } from "@/models/ChatMessage";

export default function Home() {
  const [showWelcome, setShowWelcome] = useState(true);
  const chatViewModel = useChatViewModel();
  const studentViewModel = useStudentViewModel(chatViewModel.session.context);

  // Sync student context with chat session
  useEffect(() => {
    studentViewModel.updateContext(chatViewModel.session.context);
  }, [chatViewModel.session.context]);

  const handleStart = async () => {
    setShowWelcome(false);
    
    // Send initial greeting to start the screening process
    const greeting = "Hi! I'm ready to start my learning journey.";
    await chatViewModel.sendMessage(greeting);
  };

  const handleReset = async () => {
    if (confirm("Are you sure you want to reset your session? All progress will be lost.")) {
      await chatViewModel.resetSession();
      studentViewModel.resetContext();
      setShowWelcome(true);
    }
  };

  const handleSendMessage = async (message: string) => {
    await chatViewModel.sendMessage(message);
  };

  // Get appropriate placeholder based on current phase
  const getPlaceholder = () => {
    switch (chatViewModel.currentPhase) {
      case "screening":
        return "Answer the assessment questions...";
      case "teaching":
        return "Ask questions or request to continue...";
      case "quiz":
        return "Submit your answer...";
      default:
        return "Type your message...";
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <Header
        currentPhase={chatViewModel.currentPhase}
        onReset={handleReset}
        isLoading={chatViewModel.isLoading}
      />

      {showWelcome ? (
        <div className="flex-1 overflow-y-auto">
          <WelcomeScreen onStart={handleStart} />
        </div>
      ) : (
        <>
          <PhaseIndicator currentPhase={chatViewModel.currentPhase} />
          
          <div className="flex-1 overflow-y-auto flex">
            <div className="flex-1 flex flex-col">
              <div className="container max-w-4xl mx-auto px-4 py-4">
                <StudentProfileCard context={studentViewModel.context} />
              </div>
              
              <ChatContainer
                messages={chatViewModel.messages}
                isLoading={chatViewModel.isLoading}
              />
            </div>
          </div>

          <ChatInput
            onSend={handleSendMessage}
            isDisabled={chatViewModel.isStreaming}
            placeholder={getPlaceholder()}
          />
        </>
      )}

      {chatViewModel.error && (
        <div className="fixed bottom-20 right-4 max-w-md bg-[rgb(var(--destructive))] text-[rgb(var(--destructive-foreground))] px-4 py-3 rounded-lg shadow-lg animate-slide-up">
          <p className="text-sm font-medium">Error: {chatViewModel.error}</p>
        </div>
      )}
    </div>
  );
}
