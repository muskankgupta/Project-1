
"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { API_BASE_URL } from "@/lib/api-config";

export type ServiceStatus = "online" | "offline" | "checking";

export interface HealthInfo {
  status: string;
  semantic_layer: string;
  databricks: string;
  llm_provider: string;
}

export interface ApiStatusSnapshot {
  backend: ServiceStatus;
  semanticLayer: ServiceStatus;
  databricks: ServiceStatus;
  llm: ServiceStatus;
  provider: string | null;
  health: HealthInfo | null;
  checkedAt: Date | null;
}

const INITIAL: ApiStatusSnapshot = {
  backend: "checking",
  semanticLayer: "checking",
  databricks: "checking",
  llm: "checking",
  provider: null,
  health: null,
  checkedAt: null,
};

/**
 * Convert a backend health value into a frontend service status.
 *
 * Important:
 * - Backend health = "ok" means healthy.
 * - Semantic layer returns its actual name, e.g. "amazon_sale_report".
 * - LLM returns its provider name, e.g. "gemini".
 * - Databricks returns "configured".
 */
function semanticLayerStatus(value: string | undefined): ServiceStatus {
  if (!value) {
    return "offline";
  }

  if (value === "error" || value === "fallback") {
    return "offline";
  }

  return "online";
}

function databricksStatus(value: string | undefined): ServiceStatus {
  if (!value) {
    return "offline";
  }

  if (
    value === "configured" ||
    value === "ok" ||
    value.startsWith("connected")
  ) {
    return "online";
  }

  return "offline";
}

function llmStatus(value: string | undefined): ServiceStatus {
  if (!value) {
    return "offline";
  }

  if (value === "error" || value === "fallback") {
    return "offline";
  }

  // Any configured provider such as "gemini", "openai", etc. is online.
  return "online";
}

export function useApiStatus(): {
  status: ApiStatusSnapshot;
  refresh: () => Promise<void>;
} {
  const [status, setStatus] = useState<ApiStatusSnapshot>(INITIAL);
  const mounted = useRef(true);

  const refresh = useCallback(async () => {
    setStatus((prev) => ({
      ...prev,
      backend: "checking",
      semanticLayer: "checking",
      databricks: "checking",
      llm: "checking",
    }));

    const controller = new AbortController();

    const timer = window.setTimeout(() => {
      controller.abort();
    }, 8000);

    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
        signal: controller.signal,
        cache: "no-store",
      });

      window.clearTimeout(timer);

      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }

      const health = (await response.json()) as HealthInfo;

      if (!mounted.current) {
        return;
      }

      setStatus({
        backend: health.status === "ok" ? "online" : "offline",

        semanticLayer: semanticLayerStatus(
          health.semantic_layer
        ),

        databricks: databricksStatus(
          health.databricks
        ),

        llm: llmStatus(
          health.llm_provider
        ),

        provider:
          health.llm_provider &&
          health.llm_provider !== "fallback"
            ? health.llm_provider
            : null,

        health,

        checkedAt: new Date(),
      });
    } catch (error) {
      window.clearTimeout(timer);

      if (!mounted.current) {
        return;
      }

      console.error("MetricMind health check failed:", error);

      setStatus({
        backend: "offline",
        semanticLayer: "offline",
        databricks: "offline",
        llm: "offline",
        provider: null,
        health: null,
        checkedAt: new Date(),
      });
    }
  }, []);

  useEffect(() => {
    mounted.current = true;

    void refresh();

    const interval = window.setInterval(() => {
      void refresh();
    }, 30_000);

    return () => {
      mounted.current = false;
      window.clearInterval(interval);
    };
  }, [refresh]);

  return {
    status,
    refresh,
  };
}