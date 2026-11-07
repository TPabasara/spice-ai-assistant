"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import ThemeToggle from "../theme-toggle";

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Re-check authentication status whenever the route changes
  useEffect(() => {
    setIsAuthenticated(!!localStorage.getItem("spice_access_token"));
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem("spice_access_token");
    setIsAuthenticated(false);
    router.push("/login");
  };

  return (
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

          {/* Dynamically swap links based on auth state */}
          {isAuthenticated ? (
            <>
              <Link
                href="/admin"
                className="hover:text-orange-600 transition-colors"
              >
                Admin Dashboard
              </Link>
              <button
                onClick={handleLogout}
                className="hover:text-red-600 transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <Link
              href="/login"
              className="hover:text-orange-600 transition-colors"
            >
              Login
            </Link>
          )}
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
}
