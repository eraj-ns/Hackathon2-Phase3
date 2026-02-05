/**
 * Root Layout Component
 * Updated with modern UI design
 */

import type { Metadata, Viewport } from "next";
import "@/styles/globals.css";
import Navigation from "@/components/Navigation";
import { AuthProvider } from "@/contexts/AuthContext";
import { ThemeProvider } from "@/contexts/ThemeContext";

export const metadata: Metadata = {
  title: "Todo App",
  description: "Full-stack todo application with authentication and task management",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="theme-color" content="#4f46e5" />
      </head>
      <body>
        <ThemeProvider>
          <AuthProvider>
            <div className="app-container">
              <Navigation />
              <div className="main-content">
                {children}
              </div>
            </div>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
