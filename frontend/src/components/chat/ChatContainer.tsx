/**
 * Main chat container component
 */

"use client";

import { useChat } from "@/hooks/useChat";
import { useSession } from "@/contexts/SessionContext";
import { MessageList } from "./MessageList";
import { InputArea } from "./InputArea";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { WifiOff, Loader2 } from "lucide-react";

export function ChatContainer() {
	const { session, updateContext, updateAgent } = useSession();

	const { messages, sendMessage, isProcessing, isConnected, isReconnecting } =
		useChat({
			sessionId: session?.session_id || "",
			onContextUpdate: updateContext,
			onAgentUpdate: updateAgent,
		});

	if (!session) {
		return (
			<div className="flex items-center justify-center h-full">
				<div className="text-center space-y-4">
					<Loader2 className="h-12 w-12 animate-spin mx-auto text-muted-foreground" />
					<p className="text-sm text-muted-foreground">
						Initializing session...
					</p>
				</div>
			</div>
		);
	}

	return (
		<Card className="flex flex-col h-full border-0 shadow-none">
			{/* Connection Status */}
			{!isConnected && (
				<div className="bg-yellow-50 dark:bg-yellow-900/20 border-b border-yellow-200 dark:border-yellow-800 px-4 py-2">
					<div className="flex items-center justify-center gap-2 text-sm">
						{isReconnecting ? (
							<>
								<Loader2 className="h-4 w-4 animate-spin text-yellow-700 dark:text-yellow-300" />
								<span className="text-yellow-700 dark:text-yellow-300">
									Reconnecting...
								</span>
							</>
						) : (
							<>
								<WifiOff className="h-4 w-4 text-yellow-700 dark:text-yellow-300" />
								<span className="text-yellow-700 dark:text-yellow-300">
									Disconnected
								</span>
							</>
						)}
					</div>
				</div>
			)}

			{/* Current Agent Badge */}
			<div className="border-b px-4 py-3 flex items-center justify-between">
				<div className="flex items-center gap-2">
					<span className="text-2xl">
						{session.current_agent.icon}
					</span>
					<div>
						<h3 className="font-medium text-sm">
							{session.current_agent.name}
						</h3>
						<p className="text-xs text-muted-foreground">
							{session.current_agent.description}
						</p>
					</div>
				</div>
				<Badge variant="outline">{session.current_agent.phase}</Badge>
			</div>

			{/* Messages */}
			<MessageList messages={messages} />

			{/* Input Area */}
			<InputArea
				onSendMessage={sendMessage}
				disabled={!isConnected}
				isProcessing={isProcessing}
			/>
		</Card>
	);
}
