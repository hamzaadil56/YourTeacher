/**
 * Student Learning Context Model
 * Represents the complete state of a student's learning journey
 */

export interface StudentContext {
  student_name: string | null;
  age: number | null;
  grade_level: string | null;
  cognitive_ability: CognitiveAbility | null;
  learning_style: LearningStyle | null;
  learning_pace: LearningPace | null;
  subjects_of_interest: string[];
  current_subject: string | null;
  current_topic: string | null;
  learning_objectives: string[];
  quiz_score: number | null;
  quiz_total: number | null;
  student_profile: Record<string, any>;
  screening_complete: boolean;
  concept_taught: boolean;
}

export type CognitiveAbility = "High" | "Medium" | "Low";
export type LearningStyle = "Visual" | "Auditory" | "Kinesthetic" | "Mixed";
export type LearningPace = "Fast" | "Medium" | "Slow";

export const COGNITIVE_ABILITIES: CognitiveAbility[] = ["High", "Medium", "Low"];
export const LEARNING_STYLES: LearningStyle[] = ["Visual", "Auditory", "Kinesthetic", "Mixed"];
export const LEARNING_PACES: LearningPace[] = ["Fast", "Medium", "Slow"];

/**
 * Creates an empty student context with default values
 */
export const createEmptyContext = (): StudentContext => ({
  student_name: null,
  age: null,
  grade_level: null,
  cognitive_ability: null,
  learning_style: null,
  learning_pace: null,
  subjects_of_interest: [],
  current_subject: null,
  current_topic: null,
  learning_objectives: [],
  quiz_score: null,
  quiz_total: null,
  student_profile: {},
  screening_complete: false,
  concept_taught: false,
});


