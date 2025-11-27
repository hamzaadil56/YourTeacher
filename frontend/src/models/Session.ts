/**
 * Session Model
 * Represents a learning session
 */

import { StudentContext } from "./StudentContext";
import { ChatMessage, LearningPhase } from "./ChatMessage";

export interface Session {
  id: string;
  context: StudentContext;
  messages: ChatMessage[];
  currentPhase: LearningPhase;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Creates a new session
 */
export const createSession = (): Session => ({
  id: `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
  context: {
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
  },
  messages: [],
  currentPhase: "welcome",
  createdAt: new Date(),
  updatedAt: new Date(),
});


