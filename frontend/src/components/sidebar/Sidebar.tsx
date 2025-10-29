/**
 * Main sidebar component
 */

"use client";

import { useSession } from "@/contexts/SessionContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ProgressTracker } from "./ProgressTracker";
import { StudentProfile } from "./StudentProfile";
import { RotateCcw, Lightbulb } from "lucide-react";

export function Sidebar() {
	const { session, resetSession, isLoading } = useSession();

	if (!session) {
		return null;
	}

	const tips = [
		"Be honest during assessment for better personalization",
		"Ask for clarification if you don't understand",
		"Take your time with quiz questions",
		"You can learn multiple topics in one session",
	];

	return (
		<div className="w-80 border-l bg-muted/20 p-4 space-y-4 overflow-y-auto">
			{/* Progress Tracker */}
			<ProgressTracker context={session.context} />

			{/* Student Profile */}
			<StudentProfile context={session.context} />

			{/* Session Controls */}
			<Card>
				<CardHeader>
					<CardTitle className="text-sm font-medium">
						Session
					</CardTitle>
				</CardHeader>
				<CardContent className="space-y-2">
					<Button
						variant="outline"
						size="sm"
						className="w-full"
						onClick={resetSession}
						disabled={isLoading}
					>
						<RotateCcw className="h-4 w-4 mr-2" />
						Reset Session
					</Button>
					<p className="text-xs text-muted-foreground text-center">
						Session ID: {session.session_id}
					</p>
				</CardContent>
			</Card>

			{/* Tips */}
			<Card>
				<CardHeader>
					<CardTitle className="text-sm font-medium flex items-center gap-2">
						<Lightbulb className="h-4 w-4" />
						Tips
					</CardTitle>
				</CardHeader>
				<CardContent className="space-y-2">
					{tips.map((tip, index) => (
						<div key={index} className="flex gap-2">
							<span className="text-xs text-muted-foreground flex-shrink-0">
								💡
							</span>
							<p className="text-xs text-muted-foreground">
								{tip}
							</p>
						</div>
					))}
				</CardContent>
			</Card>
		</div>
	);
}
