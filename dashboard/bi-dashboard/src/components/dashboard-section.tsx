"use client";

import { useState } from "react";
import { FileDown, FileText, RefreshCw } from "lucide-react";

import { useDashboardData } from "@/hooks/use-dashboard-data";

import {
  FilterBar,
  type DashboardFilters,
} from "@/components/dashboard/filter-bar";

import { Button } from "@/components/ui/button";

import { KpiSection } from "@/components/dashboard/kpi-section";
import { ImpactAnalysisSection } from "@/components/dashboard/impact-analysis-section";
import { RevenueOrderTrendSection } from "@/components/dashboard/revenue-order-trend-section";
import { TopStatesSection } from "@/components/dashboard/top-states-section";
import { RankingSection } from "@/components/dashboard/ranking-section";
import { AovTrendSection } from "@/components/dashboard/aov-trend-section";

import {
  exportDashboardCsv,
  exportDashboardPdf,
} from "@/lib/export";

export function DashboardSection() {
  /*
   * ============================================================
   * FILTER STATE
   * ============================================================
   */

  const [filters, setFilters] = useState<DashboardFilters>({
    search: "",
    state: null,
    category: null,
    fromPeriod: null,
    toPeriod: null,
  });

  /*
   * ============================================================
   * LOAD DASHBOARD DATA
   *
   * IMPORTANT:
   * The filters are passed to the API hook.
   *
   * This means changing a filter causes the backend to be
   * requested again with the selected filters.
   * ============================================================
   */

  const {
    data,
    isLoading,
    error,
    refresh,
  } = useDashboardData({
    search: filters.search,
    state: filters.state,
    category: filters.category,
    fromPeriod: filters.fromPeriod,
    toPeriod: filters.toPeriod,
  });

  /*
   * ============================================================
   * FILTER HANDLER
   * ============================================================
   */

  const handleFiltersChange = (
    nextFilters: DashboardFilters,
  ) => {
    setFilters(nextFilters);
  };

  /*
   * ============================================================
   * CLEAR FILTERS
   * ============================================================
   */

  const hasActiveFilters =
    filters.search !== "" ||
    filters.state !== null ||
    filters.category !== null ||
    filters.fromPeriod !== null ||
    filters.toPeriod !== null;

  /*
   * ============================================================
   * EXPORT DATA
   *
   * `data` is already filtered by the backend.
   * ============================================================
   */

  const handleExportCsv = () => {
    if (!data) {
      return;
    }

    exportDashboardCsv(data);
  };

  const handleExportPdf = () => {
    if (!data) {
      return;
    }

    exportDashboardPdf(data);
  };

  return (
    <div className="space-y-5">
      {/* ========================================================
          FILTER BAR
          ======================================================== */}

      <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-3">
        <FilterBar
          data={data}
          filters={filters}
          onFiltersChange={handleFiltersChange}
        />
      </div>

      {/* ========================================================
          ERROR
          ======================================================== */}

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-3 py-2 text-xs text-red-300">
          {error}
        </div>
      )}

      {/* ========================================================
          ACTIVE FILTER INDICATOR
          ======================================================== */}

      {hasActiveFilters && (
        <div className="text-xs text-zinc-500">
          Dashboard filtered by selected filters.
        </div>
      )}

      {/* ========================================================
          ACTIONS
          ======================================================== */}

      <div className="flex items-center justify-end gap-2">
        <Button
          variant="ghost"
          className="px-3"
          onClick={refresh}
          disabled={isLoading}
          title="Refresh dashboard data"
          aria-label="Refresh dashboard data"
        >
          <RefreshCw
            className={`h-4 w-4 ${
              isLoading ? "animate-spin" : ""
            }`}
          />

          <span className="ml-1.5 hidden text-xs sm:inline">
            Refresh
          </span>
        </Button>

        <Button
          variant="ghost"
          className="px-3"
          onClick={handleExportCsv}
          disabled={!data || isLoading}
          title="Export dashboard as CSV"
          aria-label="Export dashboard as CSV"
        >
          <FileDown className="h-4 w-4" />

          <span className="ml-1.5 hidden text-xs sm:inline">
            CSV
          </span>
        </Button>

        <Button
          variant="ghost"
          className="px-3"
          onClick={handleExportPdf}
          disabled={!data || isLoading}
          title="Export dashboard as PDF"
          aria-label="Export dashboard as PDF"
        >
          <FileText className="h-4 w-4" />

          <span className="ml-1.5 hidden text-xs sm:inline">
            PDF
          </span>
        </Button>
      </div>

      {/* ========================================================
          KPI SECTION
          ======================================================== */}

      <KpiSection
        data={data?.kpis ?? []}
        isLoading={isLoading}
      />

      {/* ========================================================
          IMPACT ANALYSIS
          ======================================================== */}

      <ImpactAnalysisSection
        data={
          data?.impactAnalysis ?? {
            statuses: [],
            comparison: [],
          }
        }
        isLoading={isLoading}
      />

      {/* ========================================================
          REVENUE + ORDER TREND / TOP STATES
          ======================================================== */}

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1.35fr)_minmax(0,0.95fr)]">
        <RevenueOrderTrendSection
          data={data?.revenueOrderTrend ?? []}
          isLoading={isLoading}
        />

        <TopStatesSection
          data={data?.topStates ?? []}
          isLoading={isLoading}
        />
      </section>

      {/* ========================================================
          TOP / WORST PERFORMERS
          ======================================================== */}

      <section className="grid gap-5 xl:grid-cols-2">
        <RankingSection
          title="Top Performing Products/Categories"
          description="Reusable ranking block for any high-performing product or category data."
          badgeLabel="Top performers"
          data={data?.topPerformers ?? []}
          isLoading={isLoading}
        />

        <RankingSection
          title="Worst Performing Products/Categories"
          description="Reusable ranking block for underperforming product or category data."
          badgeLabel="Worst performers"
          data={data?.worstPerformers ?? []}
          isLoading={isLoading}
        />
      </section>

      {/* ========================================================
          AOV TREND
          ======================================================== */}

      <AovTrendSection
        data={data?.aovTrend ?? []}
        isLoading={isLoading}
      />
    </div>
  );
}