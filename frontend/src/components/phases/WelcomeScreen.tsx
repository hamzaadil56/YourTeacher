"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain, BookOpen, ClipboardCheck, ArrowRight } from "lucide-react";

interface WelcomeScreenProps {
  onStart: () => void;
}

export function WelcomeScreen({ onStart }: WelcomeScreenProps) {
  return (
    <div className="container max-w-6xl mx-auto px-4 py-12">
      <div className="text-center mb-12 animate-fade-in">
        <div className="inline-flex items-center justify-center rounded-full bg-gradient-to-br from-[rgb(var(--primary))] to-[rgb(var(--accent))] p-4 mb-6">
          <svg
            className="h-16 w-16 text-white"
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
        <h1 className="font-[var(--font-display)] text-5xl font-bold mb-4 bg-gradient-to-r from-[rgb(var(--primary))] to-[rgb(var(--accent))] bg-clip-text text-transparent">
          Welcome to YourTeacher
        </h1>
        <p className="text-xl text-[rgb(var(--muted-foreground))] max-w-2xl mx-auto">
          Revolutionary AI-powered personalized learning system that adapts to your
          unique learning style
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <Card className="animate-slide-up border-[rgb(var(--screener))]" style={{ animationDelay: "0.1s" }}>
          <CardHeader>
            <div className="rounded-lg bg-[rgb(var(--screener))] w-12 h-12 flex items-center justify-center mb-3">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <CardTitle className="text-[rgb(var(--screener))]">1. Assessment</CardTitle>
            <CardDescription>
              We'll evaluate your cognitive abilities, learning style, and pace through
              interactive questions
            </CardDescription>
          </CardHeader>
        </Card>

        <Card className="animate-slide-up border-[rgb(var(--teaching))]" style={{ animationDelay: "0.2s" }}>
          <CardHeader>
            <div className="rounded-lg bg-[rgb(var(--teaching))] w-12 h-12 flex items-center justify-center mb-3">
              <BookOpen className="h-6 w-6 text-white" />
            </div>
            <CardTitle className="text-[rgb(var(--teaching))]">2. Learning</CardTitle>
            <CardDescription>
              Receive personalized lessons tailored to your cognitive ability and
              preferred learning style
            </CardDescription>
          </CardHeader>
        </Card>

        <Card className="animate-slide-up border-[rgb(var(--quiz))]" style={{ animationDelay: "0.3s" }}>
          <CardHeader>
            <div className="rounded-lg bg-[rgb(var(--quiz))] w-12 h-12 flex items-center justify-center mb-3">
              <ClipboardCheck className="h-6 w-6 text-white" />
            </div>
            <CardTitle className="text-[rgb(var(--quiz))]">3. Validation</CardTitle>
            <CardDescription>
              Test your understanding with customized quizzes and receive detailed
              feedback
            </CardDescription>
          </CardHeader>
        </Card>
      </div>

      <div className="text-center">
        <Button
          size="xl"
          onClick={onStart}
          className="gap-3 animate-slide-up font-[var(--font-display)] text-lg"
          style={{ animationDelay: "0.4s" }}
        >
          Start Your Learning Journey
          <ArrowRight className="h-5 w-5" />
        </Button>
        <p className="text-sm text-[rgb(var(--muted-foreground))] mt-4">
          No account required • Completely free • Personalized for you
        </p>
      </div>
    </div>
  );
}


