/**
 * api-client.ts
 *
 * Shared HTTP client for the MetricMind frontend.
 */

import { API_BASE_URL } from "@/lib/api-config";

/**
 * Generic JSON POST request.
 *
 * The second argument is the request body.
 * Dashboard filters are sent through this argument.
 */
export async function postJson<T>(
  endpoint: string,
  body?: unknown,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const errorBody = await response.json();

      if (typeof errorBody?.detail === "string") {
        message = errorBody.detail;
      } else if (typeof errorBody?.error === "string") {
        message = errorBody.error;
      }
    } catch {
      // Ignore JSON parsing errors.
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

/**
 * Generic JSON GET request.
 */
export async function getJson<T>(
  endpoint: string,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "GET",

    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const errorBody = await response.json();

      if (typeof errorBody?.detail === "string") {
        message = errorBody.detail;
      } else if (typeof errorBody?.error === "string") {
        message = errorBody.error;
      }
    } catch {
      // Ignore JSON parsing errors.
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}