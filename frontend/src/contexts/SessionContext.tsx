/**
 * Session Context - Global state management
 */

"use client";

import React, {
	createContext,
	useContext,
	useState,
	useCallback,
	useEffect,
} from "react";
import { SessionResponse, StudentLearningContext, AgentInfo } from "@/types";
import { apiClient } from "@/lib/api";

interface SessionContextType {
	session: SessionResponse | null;
	isLoading: boolean;
	error: string | null;
	createSession: () => Promise<void>;
	resetSession: () => Promise<void>;
	updateContext: (context: StudentLearningContext) => void;
	updateAgent: (agent: AgentInfo) => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export function SessionProvider({ children }: { children: React.ReactNode }) {
	const [session, setSession] = useState<SessionResponse | null>(null);
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const createSession = useCallback(async () => {
		setIsLoading(true);
		setError(null);

		try {
			const newSession = await apiClient.createSession({
				initial_message:
					"Hello! I'm ready to start my personalized learning journey.",
			});
			setSession(newSession);

			// Store session ID in localStorage for persistence
			localStorage.setItem(
				"yourteacher_session_id",
				newSession.session_id
			);
		} catch (err) {
			const errorMessage =
				err instanceof Error ? err.message : "Failed to create session";
			setError(errorMessage);
			console.error("Failed to create session:", err);
		} finally {
			setIsLoading(false);
		}
	}, []);

	const resetSession = useCallback(async () => {
		if (!session) return;

		setIsLoading(true);
		setError(null);

		try {
			const resetSession = await apiClient.resetSession(
				session.session_id
			);
			setSession(resetSession);
		} catch (err) {
			const errorMessage =
				err instanceof Error ? err.message : "Failed to reset session";
			setError(errorMessage);
			console.error("Failed to reset session:", err);
		} finally {
			setIsLoading(false);
		}
	}, [session]);

	const updateContext = useCallback((context: StudentLearningContext) => {
		setSession((prev) => {
			if (!prev) return prev;
			return {
				...prev,
				context,
			};
		});
	}, []);

	const updateAgent = useCallback((agent: AgentInfo) => {
		setSession((prev) => {
			if (!prev) return prev;
			return {
				...prev,
				current_agent: agent,
			};
		});
	}, []);

	// Try to restore session from localStorage on mount
	useEffect(() => {
		const storedSessionId = localStorage.getItem("yourteacher_session_id");

		if (storedSessionId) {
			setIsLoading(true);
			apiClient
				.getSession(storedSessionId)
				.then((session) => {
					setSession(session);
				})
				.catch((err) => {
					console.error("Failed to restore session:", err);
					// Session no longer exists, create a new one
					createSession();
				})
				.finally(() => {
					setIsLoading(false);
				});
		} else {
			// No stored session, create a new one
			createSession();
		}
	}, [createSession]);

	return (
		<SessionContext.Provider
			value={{
				session,
				isLoading,
				error,
				createSession,
				resetSession,
				updateContext,
				updateAgent,
			}}
		>
			{children}
		</SessionContext.Provider>
	);
}

export function useSession() {
	const context = useContext(SessionContext);
	if (context === undefined) {
		throw new Error("useSession must be used within a SessionProvider");
	}
	return context;
}
