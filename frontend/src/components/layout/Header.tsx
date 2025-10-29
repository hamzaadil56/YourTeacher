/**
 * Application header component
 */

"use client";

import { GraduationCap } from "lucide-react";

export function Header() {
	return (
		<header className="border-b bg-background">
			<div className="container mx-auto px-4 py-4">
				<div className="flex items-center gap-3">
					<GraduationCap className="h-8 w-8 text-primary" />
					<div>
						<h1 className="text-2xl font-bold">YourTeacher</h1>
						<p className="text-sm text-muted-foreground">
							AI-Powered Personalized Learning
						</p>
					</div>
				</div>
			</div>
		</header>
	);
}
