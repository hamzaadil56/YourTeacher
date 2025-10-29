/**
 * Type definitions for the application
 */

export interface AgentInfo {
	name: string;
	icon: string;
	description: string;
	phase: string;
	color: string;
}

export interface StudentLearningContext {
	student_name: string | null;
	age: number | null;
	grade_level: string | null;
	cognitive_ability: string | null;
	learning_style: string | null;
	learning_pace: string | null;
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

export interface SessionResponse {
	session_id: string;
	current_agent: AgentInfo;
	context: StudentLearningContext;
	created_at: string;
	message_count: number;
}

export type MessageType =
	| "user"
	| "agent"
	| "tool_call"
	| "tool_result"
	| "handoff"
	| "system";

export interface Message {
	id: string;
	type: MessageType;
	content?: string;
	agent_name?: string;
	agent_icon?: string;
	source_agent?: string;
	target_agent?: string;
	timestamp: Date;
	isStreaming?: boolean;
}

export type StreamEventType =
	| "token"
	| "agent_update"
	| "tool_call"
	| "tool_result"
	| "handoff"
	| "message_complete"
	| "error"
	| "context_update"
	| "connected";

export interface StreamEvent {
	type: StreamEventType;
	data: Record<string, any>;
	timestamp: string | null;
}

export interface SessionCreateRequest {
	initial_message?: string;
}
