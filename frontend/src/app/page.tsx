/**
 * Main application page
 */

"use client";

import { Header } from "@/components/layout/Header";
import { ChatContainer } from "@/components/chat/ChatContainer";
import { Sidebar } from "@/components/sidebar/Sidebar";

export default function Home() {
	return (
		<div className="flex flex-col h-screen">
			<Header />
			<div className="flex flex-1 overflow-hidden">
				<main className="flex-1 flex flex-col overflow-hidden">
					<ChatContainer />
				</main>
				<Sidebar />
			</div>
		</div>
	);
}
