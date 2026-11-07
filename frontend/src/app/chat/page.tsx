"use client";

import { FormEvent, useState } from "react";
import { apiClient } from "@/lib/api";

type Message = { role: "user" | "assistant"; content: string };

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const message = input.trim();
    if (!message || busy) return;
    setInput("");
    setError("");
    setMessages((current) => [...current, { role: "user", content: message }]);
    setBusy(true);
    try {
      const response = await apiClient.post("/chat/query", {
        message,
        session_id: sessionId,
      });
      setSessionId(response.data.session_id);
      setMessages((current) => [
        ...current,
        { role: "assistant", content: response.data.response },
      ]);
    } catch (requestError: unknown) {
      const detail =
        typeof requestError === "object" &&
        requestError !== null &&
        "response" in requestError
          ? (requestError as { response?: { data?: { detail?: string } } })
              .response?.data?.detail
          : undefined;
      setError(
        detail ||
          "Could not reach the assistant. Check that the API is running and configured.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="mx-auto flex w-full max-w-3xl flex-1 flex-col px-4 py-10">
      <h1 className="text-3xl font-bold">Spice AI Assistant</h1>
      <p className="mt-2 text-slate-600">
        Ask about spices, products, recipes, or store policies.
      </p>
      <div
        className="mt-8 flex-1 space-y-4 rounded-xl border bg-white p-5"
        aria-live="polite"
      >
        {messages.length === 0 && (
          <p className="text-slate-500">
            Start by asking a question, such as “What can I use instead of
            cumin?”
          </p>
        )}
        {messages.map((message, index) => (
          <div
            key={`${index}-${message.role}`}
            className={`max-w-[85%] whitespace-pre-wrap rounded-lg px-4 py-3 ${message.role === "user" ? "ml-auto bg-orange-600 text-white" : "bg-slate-100 text-slate-900"}`}
          >
            {message.content}
          </div>
        ))}
        {busy && <p className="text-sm text-slate-500">Thinking…</p>}
        {error && (
          <p
            role="alert"
            className="rounded bg-red-50 p-3 text-sm text-red-700"
          >
            {error}
          </p>
        )}
      </div>
      <form onSubmit={sendMessage} className="mt-4 flex gap-2">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          maxLength={4000}
          aria-label="Your message"
          placeholder="Ask about spices…"
          className="min-w-0 flex-1 rounded-md border bg-white px-4 py-3"
        />
        <button
          disabled={busy || !input.trim()}
          className="rounded-md bg-orange-600 px-5 py-3 font-semibold text-white disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </section>
  );
}
