/**
 * Student ViewModel Hook
 * Manages student context and profile state
 * Follows MVVM pattern - handles all business logic for student data
 */

"use client";

import { useState, useCallback } from "react";
import { StudentContext, createEmptyContext, CognitiveAbility, LearningStyle, LearningPace } from "@/models/StudentContext";

export interface StudentViewModel {
  context: StudentContext;
  updateContext: (updates: Partial<StudentContext>) => void;
  resetContext: () => void;
  isProfileComplete: boolean;
  getProfileCompletionPercentage: () => number;
}

export function useStudentViewModel(initialContext?: StudentContext): StudentViewModel {
  const [context, setContext] = useState<StudentContext>(
    initialContext || createEmptyContext()
  );

  /**
   * Updates the student context with partial updates
   */
  const updateContext = useCallback((updates: Partial<StudentContext>) => {
    setContext(prev => ({
      ...prev,
      ...updates,
    }));
  }, []);

  /**
   * Resets the student context to empty state
   */
  const resetContext = useCallback(() => {
    setContext(createEmptyContext());
  }, []);

  /**
   * Checks if the student profile is complete
   */
  const isProfileComplete = 
    context.student_name !== null &&
    context.age !== null &&
    context.grade_level !== null &&
    context.cognitive_ability !== null &&
    context.learning_style !== null &&
    context.learning_pace !== null;

  /**
   * Calculates profile completion percentage
   */
  const getProfileCompletionPercentage = useCallback(() => {
    const requiredFields = [
      context.student_name,
      context.age,
      context.grade_level,
      context.cognitive_ability,
      context.learning_style,
      context.learning_pace,
    ];

    const completedFields = requiredFields.filter(field => field !== null).length;
    return Math.round((completedFields / requiredFields.length) * 100);
  }, [context]);

  return {
    context,
    updateContext,
    resetContext,
    isProfileComplete,
    getProfileCompletionPercentage,
  };
}


