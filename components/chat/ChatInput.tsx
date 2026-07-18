"use client";

import { useState } from "react";

type ChatInputProps = {
  onSend: (message: string) => void;
  loading: boolean;
};

export default function ChatInput({
  onSend,
  loading,
}: ChatInputProps) {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (!message.trim()) return;

    onSend(message);
    setMessage("");
  };

  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="border-t border-slate-800 bg-slate-950/90 backdrop-blur-xl p-6">

      {/* Suggestion Buttons */}

      <div className="flex flex-wrap gap-3 mb-5">

        <button className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:border-cyan-500 hover:text-cyan-400 transition">
          📈 Revenue
        </button>

        <button className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:border-cyan-500 hover:text-cyan-400 transition">
          📊 KPI
        </button>

        <button className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:border-cyan-500 hover:text-cyan-400 transition">
          👥 Customers
        </button>

        <button className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:border-cyan-500 hover:text-cyan-400 transition">
          📉 Forecast
        </button>

      </div>

      {/* Input */}

      <div className="flex items-center gap-3 rounded-2xl border border-slate-700 bg-slate-900 p-3 shadow-xl">

        {/* Attachment */}

        <button
          className="h-11 w-11 rounded-xl bg-slate-800 hover:bg-slate-700 transition"
          title="Attach"
        >
          📎
        </button>

        {/* Voice */}

        <button
          className="h-11 w-11 rounded-xl bg-slate-800 hover:bg-slate-700 transition"
          title="Voice"
        >
          🎤
        </button>

        {/* Input */}

        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask your business question..."
          className="flex-1 bg-transparent outline-none text-white placeholder:text-slate-500"
        />

        {/* Send */}

        <button
          onClick={handleSend}
          disabled={loading}
          className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 px-6 py-3 font-semibold text-white hover:scale-105 transition disabled:opacity-50"
        >
          {loading ? "..." : "Send ➜"}
        </button>

      </div>

      <p className="mt-3 text-center text-xs text-slate-500">
        AI responses are generated for demonstration purposes.
      </p>

    </div>
  );
}