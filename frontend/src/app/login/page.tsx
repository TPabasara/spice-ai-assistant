"use client";

import React, { useState, FormEvent, useEffect } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [authMode, setAuthMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [authError, setAuthError] = useState("");
  const [authBusy, setAuthBusy] = useState(false);

  useEffect(() => {
    // If already logged in, push to home by default
    if (localStorage.getItem("spice_access_token")) {
      router.push("/");
    }
  }, [router]);

  const handleAuth = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setAuthBusy(true);
    setAuthError("");

    try {
      if (authMode === "register") {
        await apiClient.post("/auth/register", {
          email,
          password,
          full_name: fullName,
        });
      }

      const response = await apiClient.post(
        "/auth/login",
        new URLSearchParams({ username: email, password }),
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } },
      );

      const token = response.data.access_token;

      // Save token to local storage
      localStorage.setItem("spice_access_token", token);

      // Test admin privileges explicitly passing the new token
      try {
        await apiClient.get("/analytics/dashboard", {
          headers: { Authorization: `Bearer ${token}` }, // <-- FORCE the new token here
        });
        // If successful, this is the admin user
        router.push("/admin");
      } catch (adminError) {
        // If the request fails (403 Forbidden), this is a normal user
        router.push("/");
      }
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      setAuthError(
        detail || "Authentication failed. Please check your details.",
      );
    } finally {
      setAuthBusy(false);
    }
  };

  return (
    <section className="mx-auto w-full max-w-md flex-1 px-4 py-12">
      <h1 className="text-3xl font-bold">Sign in</h1>
      <p className="mt-2 text-slate-600">Sign in to access SpiceCraft AI.</p>
      <form
        onSubmit={handleAuth}
        className="mt-6 space-y-4 rounded-xl border bg-white p-6"
      >
        {authMode === "register" && (
          <label className="block text-sm">
            Full name
            <input
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="mt-1 w-full rounded border px-3 py-2"
            />
          </label>
        )}
        <label className="block text-sm">
          Email
          <input
            required
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full rounded border px-3 py-2"
          />
        </label>
        <label className="block text-sm">
          Password
          <input
            required
            type="password"
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded border px-3 py-2"
          />
        </label>
        {authError && <p className="text-sm text-red-700">{authError}</p>}
        <button
          disabled={authBusy}
          className="w-full rounded bg-orange-600 px-4 py-2 font-semibold text-white disabled:opacity-50"
        >
          {authBusy
            ? "Please wait…"
            : authMode === "login"
              ? "Sign in"
              : "Create account"}
        </button>
        <button
          type="button"
          onClick={() => {
            setAuthMode(authMode === "login" ? "register" : "login");
            setAuthError("");
          }}
          className="w-full text-sm text-orange-700"
        >
          {authMode === "login"
            ? "Need an account? Register"
            : "Already registered? Sign in"}
        </button>
      </form>
    </section>
  );
}
