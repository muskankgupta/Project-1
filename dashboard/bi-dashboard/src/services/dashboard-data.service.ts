/**
 * dashboard-data.service.ts
 *
 * Data access layer for the BI dashboard.
 *
 * Sends dashboard filters to all backend dashboard endpoints.
 */

import kpis from "@/mock-data/kpis.json";
import impactAnalysis from "@/mock-data/impact-analysis.json";
import revenueOrderTrend from "@/mock-data/revenue-order-trend.json";
import rankingData from "@/mock-data/ranking-data.json";
import topStates from "@/mock-data/top-states.json";
import aovTrend from "@/mock-data/aov-trend.json";

import type {
  DashboardData,
  KpiMetric,
} from "@/types/dashboard";

import { postJson } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/api-config";

/* =========================================================
   FILTER TYPE
   ========================================================= */

export interface DashboardApiFilters {
  search: string;
  state: string | null;
  category: string | null;
  fromPeriod: string | null;
  toPeriod: string | null;
}

/* =========================================================
   API RESPONSE TYPES
   ========================================================= */

interface DashboardKpisResponse {
  status: "ok" | "error";
  kpis: KpiMetric[];
  insights?: string[];
  explanation?: string | null;
  sql?: string | string[] | null;
  error?: string | null;
}

interface DashboardTrendsResponse {
  status: "ok" | "error";
  revenueOrderTrend: DashboardData["revenueOrderTrend"];
  aovTrend: DashboardData["aovTrend"];
  insights?: string[];
  explanation?: string | null;
  sql?: string | string[] | null;
  error?: string | null;
}

interface DashboardTopStatesResponse {
  status: "ok" | "error";
  topStates: DashboardData["topStates"];
  insights?: string[];
  explanation?: string | null;
  sql?: string | string[] | null;
  error?: string | null;
}

interface DashboardRankingsResponse {
  status: "ok" | "error";
  topPerformers: DashboardData["topPerformers"];
  worstPerformers: DashboardData["worstPerformers"];
  insights?: string[];
  explanation?: string | null;
  sql?: string | string[] | null;
  error?: string | null;
}

interface DashboardImpactResponse {
  status: "ok" | "error";
  impactAnalysis: DashboardData["impactAnalysis"];
  insights?: string[];
  explanation?: string | null;
  sql?: string | string[] | null;
  error?: string | null;
}

/* =========================================================
   DEFAULT FILTERS
   ========================================================= */

export const DEFAULT_DASHBOARD_FILTERS: DashboardApiFilters = {
  search: "",
  state: null,
  category: null,
  fromPeriod: null,
  toPeriod: null,
};

/* =========================================================
   MOCK DATA
   ========================================================= */

function buildMockPayload(): DashboardData {
  return {
    kpis: kpis as KpiMetric[],

    impactAnalysis:
      impactAnalysis as DashboardData["impactAnalysis"],

    revenueOrderTrend:
      revenueOrderTrend as DashboardData["revenueOrderTrend"],

    topPerformers:
      rankingData.topPerformers as DashboardData["topPerformers"],

    worstPerformers:
      rankingData.worstPerformers as DashboardData["worstPerformers"],

    topStates:
      topStates as DashboardData["topStates"],

    aovTrend:
      aovTrend as DashboardData["aovTrend"],

    meta: {
      insights: [],
      explanation: null,
      sql: null,
      source: "mock",
      generatedAt: new Date().toISOString(),
    },
  };
}

/* =========================================================
   ERROR CHECK
   ========================================================= */

function isErrorResponse(
  response:
    | {
        status: string;
      }
    | null,
): boolean {
  return response === null || response.status === "error";
}

/* =========================================================
   FETCH DASHBOARD FROM BACKEND
   ========================================================= */

async function fetchDashboardFromApi(
  filters: DashboardApiFilters,
): Promise<{
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
} | null> {
  try {
    /*
     * IMPORTANT:
     * The SAME filters object is sent to all five endpoints.
     */

    const [
      kpiResult,
      trendResult,
      topStatesResult,
      rankingResult,
      impactResult,
    ] = await Promise.all([
      postJson<DashboardKpisResponse>(
        API_ENDPOINTS.dashboardKpis,
        filters,
      ),

      postJson<DashboardTrendsResponse>(
        API_ENDPOINTS.dashboardTrends,
        filters,
      ),

      postJson<DashboardTopStatesResponse>(
        API_ENDPOINTS.dashboardTopStates,
        filters,
      ),

      postJson<DashboardRankingsResponse>(
        API_ENDPOINTS.dashboardRankings,
        filters,
      ),

      postJson<DashboardImpactResponse>(
        API_ENDPOINTS.dashboardImpact,
        filters,
      ),
    ]);

    /* -----------------------------------------
       Check API errors
       ----------------------------------------- */

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

    /* -----------------------------------------
       Combine insights
       ----------------------------------------- */

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

    /* -----------------------------------------
       Choose explanation
       ----------------------------------------- */

    const explanation =
      trendResult.explanation ??
      topStatesResult.explanation ??
      rankingResult.explanation ??
      impactResult.explanation ??
      kpiResult.explanation ??
      null;

    /* -----------------------------------------
       Return combined dashboard data
       ----------------------------------------- */

    return {
      kpis: kpiResult.kpis ?? [],

      revenueOrderTrend:
        trendResult.revenueOrderTrend ?? [],

      aovTrend:
        trendResult.aovTrend ?? [],

      topStates:
        topStatesResult.topStates ?? [],

      topPerformers:
        rankingResult.topPerformers ?? [],

      worstPerformers:
        rankingResult.worstPerformers ?? [],

      impactAnalysis:
        impactResult.impactAnalysis ?? {
          statuses: [],
          comparison: [],
          totals: {
            orders: 0,
            revenue: 0,
          },
        },

      insights,

      explanation,

      sql:
        trendResult.sql ??
        topStatesResult.sql ??
        rankingResult.sql ??
        impactResult.sql ??
        kpiResult.sql ??
        null,
    };
  } catch (error) {
    console.error(
      "Failed to fetch dashboard data:",
      error,
    );

    return null;
  }
}

/* =========================================================
   PUBLIC FUNCTION
   ========================================================= */

export async function getDashboardData(
  filters: DashboardApiFilters = DEFAULT_DASHBOARD_FILTERS,
): Promise<DashboardData> {
  const apiPayload = await fetchDashboardFromApi(filters);

  /*
   * If backend fails, use mock data.
   */

  if (apiPayload === null) {
    return buildMockPayload();
  }

  return {
    kpis: apiPayload.kpis,

    impactAnalysis:
      apiPayload.impactAnalysis,

    revenueOrderTrend:
      apiPayload.revenueOrderTrend,

    topPerformers:
      apiPayload.topPerformers,

    worstPerformers:
      apiPayload.worstPerformers,

    topStates:
      apiPayload.topStates,

    aovTrend:
      apiPayload.aovTrend,

    meta: {
      insights: apiPayload.insights,

      explanation:
        apiPayload.explanation,

      sql:
        apiPayload.sql,

      source: "api",

      generatedAt:
        new Date().toISOString(),
    },
  };
}