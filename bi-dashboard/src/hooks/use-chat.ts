"use client";

import { useRef, useState } from "react";

import { askQuestion } from "@/services/query.service";

import type { QueryResponse } from "@/types/query";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sql?: string | null;
  insights?: string[];
  chart?: string | null;
  explanation?: string | null;
  rewrittenQuestion?: string | null;
  llmText?: string | null;
  chartData?: {
    columns: string[];
    rows: Array<unknown[]>;
  } | null;
  isError?: boolean;
  isTyping?: boolean;
}

interface UseChatResult {
  messages: ChatMessage[];
  isSending: boolean;
  sendMessage: (question: string) => Promise<void>;
  clear: () => void;
}

function buildId(): string {
  return `msg-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

export function useChat(): UseChatResult {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isSending, setIsSending] = useState(false);
  const idCounter = useRef(0);

  const sendMessage = async (question: string): Promise<void> => {
    const trimmed = question.trim();

    if (!trimmed || isSending) {
      return;
    }

    const userMessage: ChatMessage = {
      id: buildId(),
      role: "user",
      content: trimmed,
    };

    const assistantPlaceholder: ChatMessage = {
      id: buildId(),
      role: "assistant",
      content: "Thinking…",
      isTyping: true,
    };

    setMessages((prev) => [...prev, userMessage, assistantPlaceholder]);
    setIsSending(true);
    idCounter.current += 1;

    const result = await askQuestion(trimmed);

    setMessages((prev) =>
      prev.map((message) => {
        if (message.id !== assistantPlaceholder.id) {
          return message;
        }

        if (!result.ok || result.response === null) {
          return {
            ...message,
            content: result.error ?? "Something went wrong while asking the backend.",
            isError: true,
          };
        }

        const response: QueryResponse = result.response;

        return {
          ...message,
          content: response.answer ?? "No answer was returned.",
          sql: response.sql,
          insights: response.insights ?? [],
          chart: response.chart,
          explanation: response.explanation ?? null,
          rewrittenQuestion: response.rewritten_question ?? null,
          llmText: response.llm?.text ?? null,
          chartData: response.data
            ? { columns: response.data.columns, rows: response.data.rows }
            : null,
          isError: false,
        };
      }),
    );

    setIsSending(false);
  };

  const clear = () => {
    setMessages([]);
  };

  return { messages, isSending, sendMessage, clear };
}
