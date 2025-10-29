/**
 * API client for backend communication
 */

import { SessionResponse, SessionCreateRequest } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiClient {
	private baseUrl: string;

	constructor(baseUrl: string = API_URL) {
		this.baseUrl = baseUrl;
	}

	/**
	 * Create a new learning session
	 */
	async createSession(
		request: SessionCreateRequest = {}
	): Promise<SessionResponse> {
		const response = await fetch(`${this.baseUrl}/api/session/start`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(request),
		});

		if (!response.ok) {
			throw new Error(`Failed to create session: ${response.statusText}`);
		}

		return response.json();
	}

	/**
	 * Get session information
	 */
	async getSession(sessionId: string): Promise<SessionResponse> {
		const response = await fetch(
			`${this.baseUrl}/api/session/${sessionId}`
		);

		if (!response.ok) {
			throw new Error(`Failed to get session: ${response.statusText}`);
		}

		return response.json();
	}

	/**
	 * Reset a session
	 */
	async resetSession(sessionId: string): Promise<SessionResponse> {
		const response = await fetch(
			`${this.baseUrl}/api/session/${sessionId}/reset`,
			{
				method: "POST",
			}
		);

		if (!response.ok) {
			throw new Error(`Failed to reset session: ${response.statusText}`);
		}

		return response.json();
	}

	/**
	 * Delete a session
	 */
	async deleteSession(sessionId: string): Promise<void> {
		const response = await fetch(
			`${this.baseUrl}/api/session/${sessionId}`,
			{
				method: "DELETE",
			}
		);

		if (!response.ok) {
			throw new Error(`Failed to delete session: ${response.statusText}`);
		}
	}

	/**
	 * Health check
	 */
	async healthCheck(): Promise<any> {
		const response = await fetch(`${this.baseUrl}/api/health`);

		if (!response.ok) {
			throw new Error(`Health check failed: ${response.statusText}`);
		}

		return response.json();
	}
}

// Export singleton instance
export const apiClient = new ApiClient();
