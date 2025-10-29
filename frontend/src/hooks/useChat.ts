/**
 * Chat hook for managing messages and streaming
 */

import { useState, useCallback, useRef } from "react";
import { Message, StreamEvent, AgentInfo } from "@/types";
import { useWebSocket } from "./useWebSocket";

interface UseChatOptions {
	sessionId: string;
	onContextUpdate?: (context: any) => void;
	onAgentUpdate?: (agent: AgentInfo) => void;
}

export function useChat({
	sessionId,
	onContextUpdate,
	onAgentUpdate,
}: UseChatOptions) {
	const [messages, setMessages] = useState<Message[]>([]);
	const [isProcessing, setIsProcessing] = useState(false);
	const currentStreamingMessageRef = useRef<string>("");
	const streamingMessageIdRef = useRef<string>("");

	const handleStreamEvent = useCallback(
		(event: StreamEvent) => {
			const timestamp = event.timestamp
				? new Date(event.timestamp)
				: new Date();

			switch (event.type) {
				case "connected":
					console.log("Connected to session:", event.data.session_id);
					break;

				case "token":
					// Update streaming message
					setIsProcessing(true);
					currentStreamingMessageRef.current += event.data.delta;

					// Update or create streaming message
					setMessages((prev) => {
						const existingIndex = prev.findIndex(
							(m) =>
								m.id === streamingMessageIdRef.current &&
								m.isStreaming
						);

						const message: Message = {
							id:
								streamingMessageIdRef.current ||
								`stream-${Date.now()}`,
							type: "agent",
							content: currentStreamingMessageRef.current,
							agent_name: event.data.agent_name,
							timestamp,
							isStreaming: true,
						};

						if (!streamingMessageIdRef.current) {
							streamingMessageIdRef.current = message.id;
						}

						if (existingIndex >= 0) {
							const newMessages = [...prev];
							newMessages[existingIndex] = message;
							return newMessages;
						}

						return [...prev, message];
					});
					break;

				case "message_complete":
					// Finalize streaming message
					setMessages((prev) => {
						const streamingIndex = prev.findIndex(
							(m) =>
								m.id === streamingMessageIdRef.current &&
								m.isStreaming
						);

						if (streamingIndex >= 0) {
							const newMessages = [...prev];
							newMessages[streamingIndex] = {
								...newMessages[streamingIndex],
								content: event.data.message,
								isStreaming: false,
							};
							return newMessages;
						}

						// Add new message if not found
						return [
							...prev,
							{
								id: `msg-${Date.now()}`,
								type: "agent",
								content: event.data.message,
								agent_name: event.data.agent_name,
								agent_icon: event.data.icon,
								timestamp,
								isStreaming: false,
							},
						];
					});

					// Reset streaming state
					currentStreamingMessageRef.current = "";
					streamingMessageIdRef.current = "";
					setIsProcessing(false);
					break;

				case "agent_update":
					onAgentUpdate?.(event.data.agent_info);
					break;

				case "tool_call":
					setMessages((prev) => [
						...prev,
						{
							id: `tool-${Date.now()}`,
							type: "tool_call",
							content: `Using tool...`,
							agent_name: event.data.agent_name,
							agent_icon: event.data.icon,
							timestamp,
						},
					]);
					break;

				case "tool_result":
					setMessages((prev) => [
						...prev,
						{
							id: `result-${Date.now()}`,
							type: "tool_result",
							content: event.data.output,
							timestamp,
						},
					]);
					break;

				case "handoff":
					setMessages((prev) => [
						...prev,
						{
							id: `handoff-${Date.now()}`,
							type: "handoff",
							source_agent: event.data.source_agent,
							target_agent: event.data.target_agent,
							timestamp,
						},
					]);
					onAgentUpdate?.(event.data.target_info);
					break;

				case "context_update":
					onContextUpdate?.(event.data.context);
					setIsProcessing(false);
					break;

				case "error":
					console.error("Stream error:", event.data.error);
					setMessages((prev) => [
						...prev,
						{
							id: `error-${Date.now()}`,
							type: "system",
							content: `Error: ${
								event.data.message || event.data.error
							}`,
							timestamp,
						},
					]);
					setIsProcessing(false);
					currentStreamingMessageRef.current = "";
					streamingMessageIdRef.current = "";
					break;
			}
		},
		[onContextUpdate, onAgentUpdate]
	);

	const {
		sendMessage: wsSendMessage,
		isConnected,
		isReconnecting,
	} = useWebSocket({
		sessionId,
		onMessage: handleStreamEvent,
	});

	const sendMessage = useCallback(
		(content: string) => {
			if (!content.trim()) return;

			// Add user message immediately
			const userMessage: Message = {
				id: `user-${Date.now()}`,
				type: "user",
				content,
				timestamp: new Date(),
			};

			setMessages((prev) => [...prev, userMessage]);
			setIsProcessing(true);

			// Send through WebSocket
			wsSendMessage(content);
		},
		[wsSendMessage]
	);

	return {
		messages,
		sendMessage,
		isProcessing,
		isConnected,
		isReconnecting,
	};
}
