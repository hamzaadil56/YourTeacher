/**
 * Individual message item component
 */

"use client";

import { Message } from "@/types";
import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

interface MessageItemProps {
	message: Message;
}

export function MessageItem({ message }: MessageItemProps) {
	if (message.type === "user") {
		return (
			<div className="flex gap-3 justify-end">
				<div className="flex flex-col items-end max-w-[80%]">
					<div className="bg-blue-600 text-white px-4 py-3 rounded-2xl rounded-tr-sm">
						<p className="text-sm leading-relaxed">
							{message.content}
						</p>
					</div>
					<span className="text-xs text-muted-foreground mt-1">
						{message.timestamp.toLocaleTimeString([], {
							hour: "2-digit",
							minute: "2-digit",
						})}
					</span>
				</div>
				<Avatar className="h-8 w-8 mt-1">
					<AvatarFallback className="bg-blue-100 text-blue-700">
						You
					</AvatarFallback>
				</Avatar>
			</div>
		);
	}

	if (message.type === "agent") {
		return (
			<div className="flex gap-3">
				<Avatar className="h-8 w-8 mt-1">
					<AvatarFallback className="bg-purple-100 text-purple-700">
						{message.agent_icon || "🤖"}
					</AvatarFallback>
				</Avatar>
				<div className="flex flex-col max-w-[80%]">
					<div className="flex items-center gap-2 mb-1">
						<span className="text-xs font-medium text-purple-700">
							{message.agent_name}
						</span>
						{message.isStreaming && (
							<span className="flex items-center gap-1 text-xs text-muted-foreground">
								<span className="animate-pulse">●</span>
								typing...
							</span>
						)}
					</div>
					<div className="bg-gray-100 dark:bg-gray-800 px-4 py-3 rounded-2xl rounded-tl-sm">
						<p className="text-sm leading-relaxed whitespace-pre-wrap">
							{message.content}
						</p>
					</div>
					<span className="text-xs text-muted-foreground mt-1">
						{message.timestamp.toLocaleTimeString([], {
							hour: "2-digit",
							minute: "2-digit",
						})}
					</span>
				</div>
			</div>
		);
	}

	if (message.type === "handoff") {
		return (
			<div className="flex justify-center my-4">
				<div className="bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 px-4 py-2 rounded-full">
					<p className="text-xs font-medium text-center">
						🔄 Agent Handoff: {message.source_agent} →{" "}
						{message.target_agent}
					</p>
				</div>
			</div>
		);
	}

	if (message.type === "tool_call") {
		return (
			<div className="flex justify-center my-2">
				<div className="bg-amber-50 dark:bg-amber-900/20 px-3 py-1.5 rounded-lg border border-amber-200 dark:border-amber-800">
					<p className="text-xs text-amber-900 dark:text-amber-200">
						🔧 {message.agent_icon} {message.agent_name}:{" "}
						{message.content}
					</p>
				</div>
			</div>
		);
	}

	if (message.type === "tool_result") {
		return (
			<div className="flex justify-center my-2">
				<div className="bg-green-50 dark:bg-green-900/20 px-3 py-1.5 rounded-lg border border-green-200 dark:border-green-800">
					<p className="text-xs text-green-900 dark:text-green-200">
						✅ {message.content}
					</p>
				</div>
			</div>
		);
	}

	if (message.type === "system") {
		return (
			<div className="flex justify-center my-2">
				<div className="bg-red-50 dark:bg-red-900/20 px-3 py-1.5 rounded-lg border border-red-200 dark:border-red-800">
					<p className="text-xs text-red-900 dark:text-red-200">
						{message.content}
					</p>
				</div>
			</div>
		);
	}

	return null;
}
