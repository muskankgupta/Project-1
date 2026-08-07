/**
 * api-client.ts
 *
 * Minimal typed fetch helper for the MetricMind backend.
 * Every request is wrapped so callers receive stable, typed results
 * with a consistent error path.
 */

import { API_BASE_URL } from "@/lib/api-config";

export interface ApiErrorPayload {
  detail?: unknown;
}

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function parseError(response: Response, fallback: string): Promise<ApiError> {
  let message = fallback;

  try {
    const payload = (await response.json()) as ApiErrorPayload;
    const detail = payload.detail;

    if (typeof detail === "string") {
      message = detail;
    } else if (detail) {
      message = JSON.stringify(detail);
    }
  } catch {
    // ignore malformed error bodies
  }

  return new ApiError(message, response.status);
}

/**
 * POST a JSON body to the MetricMind backend.
 * @throws {ApiError} when the response is not 2xx or the network fails.
 */
export async function postJson<TResponse, TBody = Record<string, unknown>>(
  endpoint: string,
  body?: TBody,
): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    throw await parseError(response, `Request to ${endpoint} failed.`);
  }

  return (await response.json()) as TResponse;
}

