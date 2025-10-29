/**
 * Student profile display component
 */

"use client";

import { StudentLearningContext } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { User, Brain, Palette, Zap, BookOpen } from "lucide-react";

interface StudentProfileProps {
	context: StudentLearningContext;
}

export function StudentProfile({ context }: StudentProfileProps) {
	if (!context.screening_complete) {
		return null;
	}

	return (
		<Card>
			<CardHeader>
				<CardTitle className="text-sm font-medium">
					Student Profile
				</CardTitle>
			</CardHeader>
			<CardContent className="space-y-3">
				{/* Name and Age */}
				{context.student_name && (
					<div className="flex items-center gap-2">
						<User className="h-4 w-4 text-muted-foreground" />
						<div className="flex-1">
							<p className="text-sm font-medium">
								{context.student_name}
							</p>
							<p className="text-xs text-muted-foreground">
								{context.age} years old • Grade{" "}
								{context.grade_level}
							</p>
						</div>
					</div>
				)}

				{/* Cognitive Ability */}
				{context.cognitive_ability && (
					<div className="flex items-center gap-2">
						<Brain className="h-4 w-4 text-muted-foreground" />
						<div className="flex-1">
							<p className="text-xs text-muted-foreground">
								Cognitive Ability
							</p>
							<Badge variant="secondary" className="mt-1">
								{context.cognitive_ability}
							</Badge>
						</div>
					</div>
				)}

				{/* Learning Style */}
				{context.learning_style && (
					<div className="flex items-center gap-2">
						<Palette className="h-4 w-4 text-muted-foreground" />
						<div className="flex-1">
							<p className="text-xs text-muted-foreground">
								Learning Style
							</p>
							<Badge variant="secondary" className="mt-1">
								{context.learning_style}
							</Badge>
						</div>
					</div>
				)}

				{/* Learning Pace */}
				{context.learning_pace && (
					<div className="flex items-center gap-2">
						<Zap className="h-4 w-4 text-muted-foreground" />
						<div className="flex-1">
							<p className="text-xs text-muted-foreground">
								Learning Pace
							</p>
							<Badge variant="secondary" className="mt-1">
								{context.learning_pace}
							</Badge>
						</div>
					</div>
				)}

				{/* Subjects of Interest */}
				{context.subjects_of_interest.length > 0 && (
					<div className="flex items-start gap-2">
						<BookOpen className="h-4 w-4 text-muted-foreground mt-1" />
						<div className="flex-1">
							<p className="text-xs text-muted-foreground mb-1">
								Interests
							</p>
							<div className="flex flex-wrap gap-1">
								{context.subjects_of_interest.map((subject) => (
									<Badge
										key={subject}
										variant="outline"
										className="text-xs"
									>
										{subject}
									</Badge>
								))}
							</div>
						</div>
					</div>
				)}
			</CardContent>
		</Card>
	);
}
