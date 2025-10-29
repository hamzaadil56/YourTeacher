/**
 * WebSocket hook for real-time streaming
 */

import { useEffect, useRef, useCallback, useState } from "react";
import { StreamEvent } from "@/types";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

interface UseWebSocketOptions {
	sessionId: string;
	onMessage: (event: StreamEvent) => void;
	onConnect?: () => void;
	onDisconnect?: () => void;
	onError?: (error: Event) => void;
}

export function useWebSocket({
	sessionId,
	onMessage,
	onConnect,
	onDisconnect,
	onError,
}: UseWebSocketOptions) {
	const wsRef = useRef<WebSocket | null>(null);
	const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
	const [isConnected, setIsConnected] = useState(false);
	const [isReconnecting, setIsReconnecting] = useState(false);

	const connect = useCallback(() => {
		if (!sessionId) return;

		try {
			const ws = new WebSocket(`${WS_URL}/api/ws/${sessionId}`);

			ws.onopen = () => {
				console.log("WebSocket connected");
				setIsConnected(true);
				setIsReconnecting(false);
				onConnect?.();
			};

			ws.onmessage = (event) => {
				try {
					const data = JSON.parse(event.data) as StreamEvent;
					onMessage(data);
				} catch (error) {
					console.error("Failed to parse WebSocket message:", error);
				}
			};

			ws.onerror = (error) => {
				console.error("WebSocket error:", error);
				onError?.(error);
			};

			ws.onclose = () => {
				console.log("WebSocket disconnected");
				setIsConnected(false);
				onDisconnect?.();

				// Attempt to reconnect after 3 seconds
				setIsReconnecting(true);
				reconnectTimeoutRef.current = setTimeout(() => {
					console.log("Attempting to reconnect...");
					connect();
				}, 3000);
			};

			wsRef.current = ws;
		} catch (error) {
			console.error("Failed to create WebSocket connection:", error);
		}
	}, [sessionId, onMessage, onConnect, onDisconnect, onError]);

	const disconnect = useCallback(() => {
		if (reconnectTimeoutRef.current) {
			clearTimeout(reconnectTimeoutRef.current);
		}

		if (wsRef.current) {
			wsRef.current.close();
			wsRef.current = null;
		}

		setIsConnected(false);
		setIsReconnecting(false);
	}, []);

	const sendMessage = useCallback((content: string) => {
		if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
			wsRef.current.send(
				JSON.stringify({
					type: "message",
					content,
				})
			);
		} else {
			console.error("WebSocket is not connected");
		}
	}, []);

	useEffect(() => {
		connect();

		return () => {
			disconnect();
		};
	}, [connect, disconnect]);

	return {
		sendMessage,
		isConnected,
		isReconnecting,
		disconnect,
		reconnect: connect,
	};
}
