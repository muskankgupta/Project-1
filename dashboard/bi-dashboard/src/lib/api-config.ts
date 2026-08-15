/**
 * api-config.ts
 *
 * Central configuration for the MetricMind backend API.
 * The URL can be overridden at build/runtime via NEXT_PUBLIC_API_BASE_URL.
 */

export const API_BASE_URL =
  (process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000").replace(/\/+$/, "");

export const API_ENDPOINTS = {
  query: "/query",
  dashboardKpis: "/dashboard/kpis",
  dashboardTrends: "/dashboard/trends",
  dashboardTopStates: "/dashboard/top-states",
  dashboardRankings: "/dashboard/rankings",
  dashboardImpact: "/dashboard/impact",
  health: "/health",
} as const;

