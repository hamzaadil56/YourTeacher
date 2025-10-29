/**
 * Chat input area component
 */

"use client";

import { useState, KeyboardEvent } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Loader2 } from "lucide-react";

interface InputAreaProps {
	onSendMessage: (message: string) => void;
	disabled?: boolean;
	isProcessing?: boolean;
}

export function InputArea({
	onSendMessage,
	disabled,
	isProcessing,
}: InputAreaProps) {
	const [input, setInput] = useState("");

	const handleSend = () => {
		if (!input.trim() || disabled) return;

		onSendMessage(input);
		setInput("");
	};

	const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			handleSend();
		}
	};

	return (
		<div className="border-t bg-background p-4">
			<div className="flex gap-2 max-w-4xl mx-auto">
				<Input
					value={input}
					onChange={(e) => setInput(e.target.value)}
					onKeyPress={handleKeyPress}
					placeholder={
						disabled
							? "Connecting..."
							: isProcessing
							? "Agent is responding..."
							: "Type your message..."
					}
					disabled={disabled || isProcessing}
					className="flex-1"
				/>
				<Button
					onClick={handleSend}
					disabled={!input.trim() || disabled || isProcessing}
					size="icon"
				>
					{isProcessing ? (
						<Loader2 className="h-4 w-4 animate-spin" />
					) : (
						<Send className="h-4 w-4" />
					)}
				</Button>
			</div>
			{isProcessing && (
				<p className="text-xs text-center text-muted-foreground mt-2">
					Agent is processing your request...
				</p>
			)}
		</div>
	);
}
