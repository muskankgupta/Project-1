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

function toServiceStatus(value: string | undefined, expectOk: boolean): ServiceStatus {
  if (value === undefined) {
    return "offline";
  }

  return (expectOk && value !== "ok") || value === "error" ? "offline" : "online";
}

export function useApiStatus(): {
  status: ApiStatusSnapshot;
  refresh: () => Promise<void>;
} {
  const [status, setStatus] = useState<ApiStatusSnapshot>(INITIAL);
  const mounted = useRef(true);

  const refresh = useCallback(async () => {
    setStatus((prev) => ({ ...prev, backend: "checking" }));

    try {
      const controller = new AbortController();
      const timer = window.setTimeout(() => controller.abort(), 8000);

      const response = await fetch(`${API_BASE_URL}/health`, {
        signal: controller.signal,
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
        backend: "online",
        semanticLayer: toServiceStatus(health.semantic_layer, true),
        databricks:
          health.databricks === "configured" ||
          health.databricks === "ok" ||
          health.databricks?.startsWith("connected")
            ? "online"
            : "offline",
        llm: toServiceStatus(health.llm_provider, true),
        // The backend uses "fallback" when no LLM provider key is loaded.
        provider: health.llm_provider === "fallback" ? null : health.llm_provider,
        health,
        checkedAt: new Date(),
      });
    } catch {
      if (!mounted.current) {
        return;
      }

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

  return { status, refresh };
}

