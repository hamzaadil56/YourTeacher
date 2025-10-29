import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { SessionProvider } from "@/contexts/SessionContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
	title: "YourTeacher - AI-Powered Personalized Learning",
	description:
		"Revolutionary AI-driven educational system with real-time streaming",
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en" suppressHydrationWarning>
			<body className={inter.className}>
				<SessionProvider>{children}</SessionProvider>
			</body>
		</html>
	);
}
