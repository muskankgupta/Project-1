/**
 * query.service.ts
 *
 * Data access layer for the MetricMind natural-language chat interface.
 *
 * Calls the live backend `/api/query` endpoint through the shared
 * API client. If the backend is unreachable, it returns a structured
 * offline error message so the UI can degrade gracefully.
 */

import { postJson } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/api-config";

import type { QueryResponse } from "@/types/query";

export interface AskQuestionResult {
  ok: boolean;
  response: QueryResponse | null;
  error: string | null;
}

const OFFLINE_ERROR =
  "The MetricMind backend is not reachable. Start the FastAPI server to ask questions against live data.";

export async function askQuestion(
  question: string,
  includeSql = true,
): Promise<AskQuestionResult> {
  const trimmed = question.trim();

  if (!trimmed) {
    return { ok: false, response: null, error: "Please enter a question." };
  }

  try {
    const response = await postJson<QueryResponse>(API_ENDPOINTS.query, {
      question: trimmed,
      include_sql: includeSql,
    });

    if (response.status === "error") {
      return {
        ok: false,
        response,
        error: response.error ?? response.answer ?? "Query execution failed.",
      };
    }

    return { ok: true, response, error: null };
  } catch {
    return { ok: false, response: null, error: OFFLINE_ERROR };
  }
}

