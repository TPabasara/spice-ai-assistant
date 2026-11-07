import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import ThemeToggle from "./theme-toggle";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Spice AI Assistant",
  description: "Your intelligent guide to premium spices and recipes.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.className} min-h-screen flex flex-col bg-slate-50 text-slate-900`}
      >
        <nav className="sticky top-0 z-50 w-full border-b bg-white shadow-sm">
          <div className="container mx-auto flex h-16 items-center justify-between px-4">
            <Link
              href="/"
              className="text-xl font-bold tracking-tight text-orange-600"
            >
              SpiceCraft AI
            </Link>
            <div className="flex items-center gap-3 text-sm font-medium sm:gap-6">
              <Link
                href="/products"
                className="hover:text-orange-600 transition-colors"
              >
                Products
              </Link>
              <Link
                href="/chat"
                className="hover:text-orange-600 transition-colors"
              >
                AI Assistant
              </Link>
              <Link
                href="/login"
                className="hover:text-orange-600 transition-colors"
              >
                Login
              </Link>
              <ThemeToggle />
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 flex flex-col">{children}</main>
      </body>
    </html>
  );
}
