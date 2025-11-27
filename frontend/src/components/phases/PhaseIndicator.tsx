"use client";

import { LearningPhase } from "@/models/ChatMessage";
import { Progress } from "@/components/ui/progress";
import { Brain, BookOpen, ClipboardCheck } from "lucide-react";
import { cn } from "@/lib/utils";

interface PhaseIndicatorProps {
  currentPhase: LearningPhase;
}

const phases = [
  { id: "screening" as LearningPhase, label: "Assessment", icon: Brain, color: "screener" },
  { id: "teaching" as LearningPhase, label: "Learning", icon: BookOpen, color: "teaching" },
  { id: "quiz" as LearningPhase, label: "Quiz", icon: ClipboardCheck, color: "quiz" },
];

export function PhaseIndicator({ currentPhase }: PhaseIndicatorProps) {
  if (currentPhase === "welcome") return null;

  const currentIndex = phases.findIndex((p) => p.id === currentPhase);
  const progress = ((currentIndex + 1) / phases.length) * 100;

  return (
    <div className="border-b border-[rgb(var(--border))] bg-[rgb(var(--muted))]/30 py-6 px-4">
      <div className="container max-w-4xl mx-auto">
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            {phases.map((phase, index) => {
              const Icon = phase.icon;
              const isActive = index === currentIndex;
              const isCompleted = index < currentIndex;

              return (
                <div key={phase.id} className="flex items-center gap-3 flex-1">
                  <div
                    className={cn(
                      "rounded-full p-3 transition-all duration-300",
                      isActive && `bg-[rgb(var(--${phase.color}))] text-white shadow-lg scale-110`,
                      isCompleted && `bg-[rgb(var(--${phase.color}))] text-white`,
                      !isActive && !isCompleted && "bg-[rgb(var(--muted))] text-[rgb(var(--muted-foreground))]"
                    )}
                  >
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="hidden sm:block flex-1">
                    <p
                      className={cn(
                        "font-semibold text-sm",
                        isActive && "text-[rgb(var(--foreground))]",
                        !isActive && "text-[rgb(var(--muted-foreground))]"
                      )}
                    >
                      {phase.label}
                    </p>
                    <p className="text-xs text-[rgb(var(--muted-foreground))]">
                      Step {index + 1} of {phases.length}
                    </p>
                  </div>
                  {index < phases.length - 1 && (
                    <div className="flex-1 h-1 bg-[rgb(var(--muted))] rounded-full overflow-hidden hidden md:block">
                      <div
                        className={cn(
                          "h-full transition-all duration-500",
                          isCompleted && `bg-[rgb(var(--${phases[index + 1].color}))]`
                        )}
                        style={{ width: isCompleted ? "100%" : "0%" }}
                      />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          <Progress value={progress} variant={phases[currentIndex]?.color as any} />
        </div>
      </div>
    </div>
  );
}


