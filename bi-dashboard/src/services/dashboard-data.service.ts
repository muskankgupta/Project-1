/**
 * dashboard-data.service.ts
 *
 * Data access layer for the BI dashboard.
 *
 * The service calls the live MetricMind backend for every dashboard section.
 * If the backend is unreachable or returns an error, it falls back to the
 * bundled mock datasets so the UI never renders empty while offline.
 */

import kpis from "@/mock-data/kpis.json";
import impactAnalysis from "@/mock-data/impact-analysis.json";
import revenueOrderTrend from "@/mock-data/revenue-order-trend.json";
import rankingData from "@/mock-data/ranking-data.json";
import topStates from "@/mock-data/top-states.json";
import aovTrend from "@/mock-data/aov-trend.json";

import type { DashboardData, KpiMetric } from "@/types/dashboard";

import { postJson } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/api-config";

/** Shape of the backend `/dashboard/*` responses we consume. */
interface DashboardKpisResponse {
  status: "ok" | "error";
  kpis: KpiMetric[];
  insights: string[];
  explanation: string | null;
  sql: string | string[] | null;
}

interface DashboardTrendsResponse {
  status: "ok" | "error";
  revenueOrderTrend: DashboardData["revenueOrderTrend"];
  aovTrend: DashboardData["aovTrend"];
  insights: string[];
  explanation: string | null;
  sql: string | string[] | null;
}

interface DashboardTopStatesResponse {
  status: "ok" | "error";
  topStates: DashboardData["topStates"];
  insights: string[];
  explanation: string | null;
  sql: string | string[] | null;
}

interface DashboardRankingsResponse {
  status: "ok" | "error";
  topPerformers: DashboardData["topPerformers"];
  worstPerformers: DashboardData["worstPerformers"];
  insights: string[];
  explanation: string | null;
  sql: string | string[] | null;
}

interface DashboardImpactResponse {
  status: "ok" | "error";
  impactAnalysis: DashboardData["impactAnalysis"];
  insights: string[];
  explanation: string | null;
  sql: string | string[] | null;
}

interface ApiDashboardBundle {
  kpis: DashboardData["kpis"];
  revenueOrderTrend: DashboardData["revenueOrderTrend"];
  aovTrend: DashboardData["aovTrend"];
  topStates: DashboardData["topStates"];
  topPerformers: DashboardData["topPerformers"];
  worstPerformers: DashboardData["worstPerformers"];
  impactAnalysis: DashboardData["impactAnalysis"];
  insights: string[];
  explanation: string | null;
  sql: string | string[] | null;
}

/** Build a stable `DashboardData` payload from the bundled mock files. */
function buildMockPayload(): DashboardData {
  return {
    kpis: kpis as KpiMetric[],
    impactAnalysis: impactAnalysis as DashboardData["impactAnalysis"],
    revenueOrderTrend: revenueOrderTrend as DashboardData["revenueOrderTrend"],
    topPerformers: rankingData.topPerformers as DashboardData["topPerformers"],
    worstPerformers: rankingData.worstPerformers as DashboardData["worstPerformers"],
    topStates: topStates as DashboardData["topStates"],
    aovTrend: aovTrend as DashboardData["aovTrend"],
    meta: {
      insights: [],
      explanation: null,
      sql: null,
      source: "mock",
      generatedAt: new Date().toISOString(),
    },
  };
}

/** Resolve an error to `true` so counters/aggregation stay simple. */
function isErrorResponse<T extends { status: string }>(response: T | null): boolean {
  return response === null || response.status === "error";
}

/**
 * Fetch all dashboard sections from the live backend in parallel.
 * Returns `null` when any core section fails so the caller can fall back.
 */
async function fetchDashboardFromApi(): Promise<ApiDashboardBundle | null> {
  try {
    const [kpiResult, trendResult, topStatesResult, rankingResult, impactResult] =
      await Promise.all([
        postJson<DashboardKpisResponse>(API_ENDPOINTS.dashboardKpis),
        postJson<DashboardTrendsResponse>(API_ENDPOINTS.dashboardTrends),
        postJson<DashboardTopStatesResponse>(API_ENDPOINTS.dashboardTopStates),
        postJson<DashboardRankingsResponse>(API_ENDPOINTS.dashboardRankings),
        postJson<DashboardImpactResponse>(API_ENDPOINTS.dashboardImpact),
      ]);

    const hasError = [
      kpiResult,
      trendResult,
      topStatesResult,
      rankingResult,
      impactResult,
    ].some(isErrorResponse);

    if (hasError) {
      return null;
    }

    const insights = Array.from(
      new Set(
        [
          ...(kpiResult.insights ?? []),
          ...(trendResult.insights ?? []),
          ...(topStatesResult.insights ?? []),
          ...(rankingResult.insights ?? []),
          ...(impactResult.insights ?? []),
        ].filter(Boolean),
      ),
    );

    const explanation =
      trendResult.explanation ??
      topStatesResult.explanation ??
      rankingResult.explanation ??
      impactResult.explanation ??
      kpiResult.explanation;

    return {
      kpis: kpiResult.kpis ?? [],
      revenueOrderTrend: trendResult.revenueOrderTrend ?? [],
      aovTrend: trendResult.aovTrend ?? [],
      topStates: topStatesResult.topStates ?? [],
      topPerformers: rankingResult.topPerformers ?? [],
      worstPerformers: rankingResult.worstPerformers ?? [],
      impactAnalysis: impactResult.impactAnalysis ?? {
        statuses: [],
        comparison: [],
        totals: { orders: 0, revenue: 0 },
      },
      insights,
      explanation,
      sql: trendResult.sql ?? null,
    };
  } catch {
    return null;
  }
}

/**
 * Load the full dashboard dataset.
 *
 * Sources, in order of preference:
 *  1. Live MetricMind backend (parallel section calls)
 *  2. Bundled mock JSON (offline/development fallback)
 */
export async function getDashboardData(): Promise<DashboardData> {
  const apiPayload = await fetchDashboardFromApi();

  if (apiPayload === null) {
    return buildMockPayload();
  }

  return {
    kpis: apiPayload.kpis,
    impactAnalysis: apiPayload.impactAnalysis,
    revenueOrderTrend: apiPayload.revenueOrderTrend,
    topPerformers: apiPayload.topPerformers,
    worstPerformers: apiPayload.worstPerformers,
    topStates: apiPayload.topStates,
    aovTrend: apiPayload.aovTrend,
    meta: {
      insights: apiPayload.insights,
      explanation: apiPayload.explanation,
      sql: apiPayload.sql,
      source: "api",
      generatedAt: new Date().toISOString(),
    },
  };
}

