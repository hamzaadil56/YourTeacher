/**
 * Message list component with auto-scroll
 */

"use client";

import { useEffect, useRef } from "react";
import { Message } from "@/types";
import { ScrollArea } from "@/components/ui/scroll-area";
import { MessageItem } from "./MessageItem";

interface MessageListProps {
	messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
	const bottomRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		// Auto-scroll to bottom when new messages arrive
		bottomRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [messages]);

	if (messages.length === 0) {
		return (
			<div className="flex items-center justify-center h-full">
				<div className="text-center space-y-2">
					<div className="text-4xl">🎓</div>
					<h3 className="text-lg font-medium">
						Welcome to YourTeacher
					</h3>
					<p className="text-sm text-muted-foreground max-w-md">
						Your personalized AI learning companion. Start a
						conversation to begin your learning journey!
					</p>
				</div>
			</div>
		);
	}

	return (
		<ScrollArea className="flex-1 px-4">
			<div className="space-y-4 py-4">
				{messages.map((message) => (
					<MessageItem key={message.id} message={message} />
				))}
				<div ref={bottomRef} />
			</div>
		</ScrollArea>
	);
}
