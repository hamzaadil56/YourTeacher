/**
 * Learning progress tracker component
 */

"use client";

import { StudentLearningContext } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, Circle, Clock } from "lucide-react";

interface ProgressTrackerProps {
	context: StudentLearningContext;
}

export function ProgressTracker({ context }: ProgressTrackerProps) {
	const phases = [
		{
			name: "Assessment",
			icon: "🔍",
			completed: context.screening_complete,
			info: context.screening_complete
				? `${context.cognitive_ability} cognitive ability, ${context.learning_style} learner`
				: "Profile creation in progress",
		},
		{
			name: "Learning",
			icon: "👨‍🏫",
			completed: context.concept_taught,
			info:
				context.concept_taught && context.current_topic
					? `${context.current_subject}: ${context.current_topic}`
					: context.screening_complete
					? "Ready for learning"
					: "Waiting for assessment",
		},
		{
			name: "Quiz",
			icon: "📝",
			completed: context.quiz_score !== null,
			info:
				context.quiz_score !== null
					? `Score: ${context.quiz_score}/${context.quiz_total}`
					: context.concept_taught
					? "Ready for quiz"
					: "Waiting for teaching",
		},
	];

	return (
		<Card>
			<CardHeader>
				<CardTitle className="text-sm font-medium">
					Learning Progress
				</CardTitle>
			</CardHeader>
			<CardContent className="space-y-3">
				{phases.map((phase, index) => (
					<div key={phase.name} className="flex items-start gap-3">
						<div className="flex-shrink-0 mt-0.5">
							{phase.completed ? (
								<CheckCircle2 className="h-5 w-5 text-green-600" />
							) : index === 0 || phases[index - 1].completed ? (
								<Clock className="h-5 w-5 text-blue-600 animate-pulse" />
							) : (
								<Circle className="h-5 w-5 text-gray-300" />
							)}
						</div>
						<div className="flex-1 space-y-1">
							<div className="flex items-center gap-2">
								<span className="text-lg">{phase.icon}</span>
								<span className="font-medium text-sm">
									{phase.name}
								</span>
							</div>
							<p className="text-xs text-muted-foreground">
								{phase.info}
							</p>
						</div>
					</div>
				))}
			</CardContent>
		</Card>
	);
}
