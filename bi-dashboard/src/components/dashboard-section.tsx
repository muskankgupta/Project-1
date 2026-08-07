"use client";

import { useMemo, useState } from "react";
import { FileDown, FileText, RefreshCw } from "lucide-react";

import { useDashboardData } from "@/hooks/use-dashboard-data";
import { Button } from "@/components/ui/button";
import { FilterBar, type DashboardFilters } from "@/components/dashboard/filter-bar";
import { KpiSection } from "@/components/dashboard/kpi-section";
import { ImpactAnalysisSection } from "@/components/dashboard/impact-analysis-section";
import { RevenueOrderTrendSection } from "@/components/dashboard/revenue-order-trend-section";
import { TopStatesSection } from "@/components/dashboard/top-states-section";
import { RankingSection } from "@/components/dashboard/ranking-section";
import { AovTrendSection } from "@/components/dashboard/aov-trend-section";
import { exportDashboardCsv, exportDashboardPdf } from "@/lib/export";

import type { DashboardData, RevenueOrderTrendPoint } from "@/types/dashboard";

export function DashboardSection() {
  const { data, isLoading, refresh } = useDashboardData();
  const [filters, setFilters] = useState<DashboardFilters>({
    search: "",
    state: null,
    category: null,
    fromPeriod: null,
    toPeriod: null,
  });

  /** Apply client-side filters to produce the filtered dashboard payload. */
  const filtered = useMemo<DashboardData | null>(() => {
    if (!data) {
      return null;
    }

    const search = filters.search.trim().toLowerCase();
    const inRange = (period: string): boolean => {
      const month = period.slice(0, 7);
      if (filters.fromPeriod && month < filters.fromPeriod) return false;
      if (filters.toPeriod && month > filters.toPeriod) return false;
      return true;
    };

    const revenueOrderTrend = (data.revenueOrderTrend ?? []).filter((point) =>
      inRange(point.period),
    );
    const aovTrend = (data.aovTrend ?? []).filter((point) => inRange(point.period));

    let topStates = (data.topStates ?? []).filter((state) =>
      filters.state ? state.state === filters.state : true,
    );
    if (search) {
      topStates = topStates.filter((state) => state.state.toLowerCase().includes(search));
    }

    let topPerformers = (data.topPerformers ?? []).filter((item) =>
      filters.category ? item.category === filters.category : true,
    );
    let worstPerformers = (data.worstPerformers ?? []).filter((item) =>
      filters.category ? item.category === filters.category : true,
    );
    if (search) {
      topPerformers = topPerformers.filter((item) =>
        item.name.toLowerCase().includes(search),
      );
      worstPerformers = worstPerformers.filter((item) =>
        item.name.toLowerCase().includes(search),
      );
    }

    return {
      ...data,
      revenueOrderTrend,
      aovTrend: aovTrend as DashboardData["aovTrend"],
      topStates,
      topPerformers,
      worstPerformers,
    };
  }, [data, filters]);

  const trendPayload: RevenueOrderTrendPoint[] = useMemo(
    () => filtered?.revenueOrderTrend ?? [],
    [filtered],
  );

  return (
    <div className="flex flex-col gap-5">
      <div className="flex flex-col gap-3 border border-white/10 bg-white/5 p-3 lg:flex-row lg:items-center lg:justify-between">
        <FilterBar data={data} filters={filters} onFiltersChange={setFilters} />

        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            className="px-3"
            onClick={refresh}
            disabled={isLoading}
            title="Refresh dashboard data"
            aria-label="Refresh dashboard data"
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
            <span className="ml-1.5 hidden text-xs sm:inline">Refresh</span>
          </Button>
          <Button
            variant="ghost"
            className="px-3"
            onClick={() => filtered && exportDashboardCsv(filtered)}
            disabled={!filtered}
            title="Export dashboard as CSV"
            aria-label="Export dashboard as CSV"
          >
            <FileDown className="h-4 w-4" />
            <span className="ml-1.5 hidden text-xs sm:inline">CSV</span>
          </Button>
          <Button
            variant="ghost"
            className="px-3"
            onClick={() => filtered && exportDashboardPdf(filtered)}
            disabled={!filtered}
            title="Export dashboard as PDF"
            aria-label="Export dashboard as PDF"
          >
            <FileText className="h-4 w-4" />
            <span className="ml-1.5 hidden text-xs sm:inline">PDF</span>
          </Button>
        </div>
      </div>

      <KpiSection data={filtered?.kpis ?? []} isLoading={isLoading} />

      <ImpactAnalysisSection
        data={filtered?.impactAnalysis ?? { statuses: [], comparison: [] }}
        isLoading={isLoading}
      />

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1.35fr)_minmax(0,0.95fr)]">
        <RevenueOrderTrendSection data={trendPayload} isLoading={isLoading} />
        <TopStatesSection data={filtered?.topStates ?? []} isLoading={isLoading} />
      </section>

      <section className="grid gap-5 xl:grid-cols-2">
        <RankingSection
          title="Top Performing Products/Categories"
          description="Reusable ranking block for any high-performing product or category data."
          badgeLabel="Top performers"
          data={filtered?.topPerformers ?? []}
          isLoading={isLoading}
        />
        <RankingSection
          title="Worst Performing Products/Categories"
          description="Reusable ranking block for underperforming product or category data."
          badgeLabel="Worst performers"
          data={filtered?.worstPerformers ?? []}
          isLoading={isLoading}
        />
      </section>

      <AovTrendSection data={filtered?.aovTrend ?? []} isLoading={isLoading} />
    </div>
  );
}

