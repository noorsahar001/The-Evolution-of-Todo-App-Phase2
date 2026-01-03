import type { Metadata } from "next";
import "./globals.css";

/**
 * Root layout for the application.
 *
 * Per FR-024 to FR-030: Provides global styles and structure.
 */

export const metadata: Metadata = {
  title: "Todo App",
  description: "A full-stack todo application with user authentication",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 antialiased">{children}</body>
    </html>
  );
}
