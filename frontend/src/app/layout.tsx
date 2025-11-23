import type { Metadata } from "next";
import { Inter, Poppins } from "next/font/google";
import "./globals.css";

// Educational-friendly body font with excellent readability
const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

// Strong display font for headings
const poppins = Poppins({
  variable: "--font-poppins",
  weight: ["400", "500", "600", "700", "800"],
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "YourTeacher - AI-Powered Personalized Learning",
  description: "Revolutionary AI-driven educational system with personalized learning experiences through intelligent multi-agent coordination",
  keywords: ["AI Education", "Personalized Learning", "AI Tutor", "Educational Technology"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${poppins.variable}`}>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
