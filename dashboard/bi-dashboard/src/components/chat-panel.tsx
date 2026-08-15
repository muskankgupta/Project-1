"use client";

import { useEffect, useRef, useState } from "react";

import { Eraser, Send, Sparkles, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ChatChart } from "@/components/chat/chat-chart";
import { useChat, type ChatMessage } from "@/hooks/use-chat";

const SUGGESTIONS = [
  "What was total revenue?",
  "Top 5 states by revenue",
  "Best selling category",
  "How many orders were cancelled?",
  "Average order value",
];

function MessageBubble({ message }: { message: ChatMessage }) {
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-2xl rounded-br-sm bg-cyan-400/15 px-4 py-2.5 text-sm leading-6 text-cyan-50">
          {message.content}
        </div>
      </div>
    );
  }

  const showTyping = Boolean(message.isTyping);

  return (
    <div className="flex justify-start">
      <div className="max-w-[92%] space-y-2">
        <div
          className={`rounded-2xl rounded-bl-sm border px-4 py-3 text-sm leading-6 ${
            message.isError
              ? "border-rose-400/20 bg-rose-400/10 text-rose-100"
              : "border-white/10 bg-white/5 text-zinc-200"
          }`}
        >
          {showTyping ? <TypingIndicator label="MetricMind is analyzing" /> : message.content}
        </div>

        {message.rewrittenQuestion &&
          message.rewrittenQuestion !== message.content &&
          !showTyping && (
            <div className="rounded-2xl border border-white/5 bg-white/[0.03] px-4 py-2.5">
              <p className="text-[11px] uppercase tracking-wide text-zinc-500">Parsed question</p>
              <p className="mt-0.5 text-xs text-zinc-400">{message.rewrittenQuestion}</p>
            </div>
          )}

        {message.insights && message.insights.length > 0 && (
          <div className="rounded-2xl border border-cyan-400/10 bg-cyan-400/5 px-4 py-3">
            <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-cyan-300">
              Insights
            </p>
            <ul className="space-y-1">
              {message.insights.map((insight, i) => (
                <li key={i} className="text-xs leading-5 text-zinc-400">
                  • {insight}
                </li>
              ))}
            </ul>
          </div>
        )}

        {message.explanation && !showTyping && (
          <div className="rounded-2xl border border-white/5 bg-white/[0.03] px-4 py-3">
            <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
              Explanation
            </p>
            <p className="text-xs leading-5 text-zinc-400">{message.explanation}</p>
          </div>
        )}

        {message.llmText && !showTyping && (
          <div className="rounded-2xl border border-fuchsia-400/15 bg-fuchsia-400/5 px-4 py-3">
            <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-fuchsia-300">
              Executive Summary
            </p>
            <p className="text-xs leading-5 text-zinc-300">{message.llmText}</p>
          </div>
        )}

        {message.sql && (
          <details className="rounded-2xl border border-white/5 bg-white/[0.03] px-4 py-3">
            <summary className="cursor-pointer text-xs font-medium text-zinc-400">
              View SQL
            </summary>
            <pre className="mt-2 overflow-x-auto whitespace-pre-wrap text-[11px] leading-5 text-zinc-500">
              {message.sql}
            </pre>
          </details>
        )}

{message.chart &&
          message.chart !== "No chart recommended." &&
          message.chartData &&
          !showTyping && (
            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-3">
              <div className="mb-2 flex items-center gap-1.5">
                <Sparkles className="h-3 w-3 text-cyan-400" />
                <span className="text-[11px] font-medium text-zinc-400">
                  {message.chart}
                </span>
              </div>
              <ChatChart
                chart={message.chart}
                columns={message.chartData.columns}
                rows={message.chartData.rows}
              />
            </div>
          )}

        {message.chart &&
          message.chart !== "No chart recommended." &&
          !message.chartData &&
          !showTyping && (
            <div className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[11px] text-zinc-400">
              <Sparkles className="h-3 w-3 text-cyan-400" />
              Recommended visual: {message.chart}
            </div>
          )}
      </div>
    </div>
  );
}

function TypingIndicator({ label }: { label: string }) {
  return (
    <span className="inline-flex items-center gap-1.5 text-zinc-400">
      <span className="flex items-center gap-1">
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-cyan-400 [animation-delay:0ms]" />
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-cyan-400 [animation-delay:150ms]" />
        <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-cyan-400 [animation-delay:300ms]" />
      </span>
      <span className="text-xs">{label}…</span>
    </span>
  );
}

interface ChatPanelProps {
  open: boolean;
  onClose: () => void;
}

export function ChatPanel({ open, onClose }: ChatPanelProps) {
  const { messages, isSending, sendMessage, clear } = useChat();
  const [draft, setDraft] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (open) {
      scrollRef.current?.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages, open]);

  if (!open) {
    return null;
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const question = draft.trim();

    if (!question || isSending) {
      return;
    }

    setDraft("");
    await sendMessage(question);
  };

  return (
    <Card className="fixed bottom-6 right-6 z-50 flex h-[560px] w-[min(400px,calc(100vw-2rem))] flex-col overflow-hidden bg-[#0a0f1e]/95 shadow-2xl backdrop-blur-xl">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-cyan-400/15 text-cyan-300">
            <Sparkles className="h-4 w-4" />
          </div>
          <div>
            <p className="text-sm font-semibold text-white">MetricMind AI</p>
            <p className="text-[11px] text-zinc-500">
              {isSending ? "Working…" : "Ask about your sales data"}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          {messages.length > 0 && (
            <Button
              type="button"
              variant="ghost"
              className="px-2"
              onClick={clear}
              aria-label="Clear conversation"
              title="Clear conversation"
            >
              <Eraser className="h-4 w-4" />
            </Button>
          )}
          <Button
            type="button"
            variant="ghost"
            className="px-2"
            onClick={onClose}
            aria-label="Close chat"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto px-4 py-4">
        {messages.length === 0 && (
          <div className="space-y-3">
            <div className="rounded-2xl rounded-bl-sm border border-white/10 bg-white/5 px-4 py-3 text-sm leading-6 text-zinc-300">
              Hi! I&apos;m your analytics assistant. Ask me about revenue, orders,
              top states, cancellations, or anything in your Amazon sales data.
            </div>
            <div className="flex flex-wrap gap-2">
              {SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-zinc-400 transition hover:border-cyan-400/30 hover:text-cyan-200"
                  onClick={() => sendMessage(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isSending && (
          <div className="flex items-center gap-2 text-xs text-zinc-500">
            <span className="h-2 w-2 animate-pulse rounded-full bg-cyan-400" />
            MetricMind is analyzing…
          </div>
        )}
      </div>

      {/* Input */}
      <form
        onSubmit={handleSubmit}
        className="flex items-center gap-2 border-t border-white/10 px-3 py-3"
      >
        <Input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Ask a question…"
          className="flex-1"
          disabled={isSending}
        />
        <Button
          type="submit"
          className="px-3"
          disabled={isSending || !draft.trim()}
          aria-label="Send question"
        >
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </Card>
  );
}

