"use client";

import { StudentContext } from "@/models/StudentContext";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { User, Brain, Palette, Gauge } from "lucide-react";

interface StudentProfileCardProps {
  context: StudentContext;
}

export function StudentProfileCard({ context }: StudentProfileCardProps) {
  if (!context.screening_complete) return null;

  return (
    <Card className="mb-4 border-[rgb(var(--primary))] animate-slide-in-left">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg flex items-center gap-2">
          <User className="h-5 w-5" />
          Your Learning Profile
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {context.student_name && (
          <div className="flex items-center justify-between">
            <span className="text-sm text-[rgb(var(--muted-foreground))]">Name</span>
            <span className="font-semibold">{context.student_name}</span>
          </div>
        )}
        
        {context.cognitive_ability && (
          <div className="flex items-center justify-between">
            <span className="text-sm text-[rgb(var(--muted-foreground))] flex items-center gap-1">
              <Brain className="h-4 w-4" />
              Cognitive Ability
            </span>
            <Badge variant="default">{context.cognitive_ability}</Badge>
          </div>
        )}
        
        {context.learning_style && (
          <div className="flex items-center justify-between">
            <span className="text-sm text-[rgb(var(--muted-foreground))] flex items-center gap-1">
              <Palette className="h-4 w-4" />
              Learning Style
            </span>
            <Badge variant="secondary">{context.learning_style}</Badge>
          </div>
        )}
        
        {context.learning_pace && (
          <div className="flex items-center justify-between">
            <span className="text-sm text-[rgb(var(--muted-foreground))] flex items-center gap-1">
              <Gauge className="h-4 w-4" />
              Learning Pace
            </span>
            <Badge variant="outline">{context.learning_pace}</Badge>
          </div>
        )}

        {context.subjects_of_interest.length > 0 && (
          <div className="pt-2 border-t border-[rgb(var(--border))]">
            <span className="text-sm text-[rgb(var(--muted-foreground))] block mb-2">
              Interests
            </span>
            <div className="flex flex-wrap gap-2">
              {context.subjects_of_interest.map((subject) => (
                <Badge key={subject} variant="outline" className="text-xs">
                  {subject}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

