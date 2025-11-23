"use client";

import { LearningPhase } from "@/models/ChatMessage";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { GraduationCap, RefreshCw } from "lucide-react";

interface HeaderProps {
  currentPhase: LearningPhase;
  onReset: () => void;
  isLoading?: boolean;
}

const phaseLabels: Record<LearningPhase, string> = {
  welcome: "Welcome",
  screening: "Student Assessment",
  teaching: "Learning",
  quiz: "Quiz",
};

const phaseVariants: Record<LearningPhase, "default" | "screener" | "teaching" | "quiz"> = {
  welcome: "default",
  screening: "screener",
  teaching: "teaching",
  quiz: "quiz",
};

export function Header({ currentPhase, onReset, isLoading }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[rgb(var(--border))] bg-[rgb(var(--background))]/95 backdrop-blur supports-[backdrop-filter]:bg-[rgb(var(--background))]/80">
      <div className="container flex h-16 items-center justify-between px-4 md:px-6">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="rounded-lg bg-gradient-to-br from-[rgb(var(--primary))] to-[rgb(var(--accent))] p-2">
              <GraduationCap className="h-6 w-6 text-white" />
            </div>
            <h1 className="font-[var(--font-display)] text-2xl font-bold tracking-tight">
              YourTeacher
            </h1>
          </div>
          <Badge variant={phaseVariants[currentPhase]} className="hidden sm:inline-flex">
            {phaseLabels[currentPhase]}
          </Badge>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={onReset}
          disabled={isLoading}
          className="gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
          <span className="hidden sm:inline">Reset Session</span>
        </Button>
      </div>
    </header>
  );
}

