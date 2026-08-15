"use client";

import { useCallback, useEffect, useState } from "react";

import {
  getDashboardData,
  type DashboardApiFilters,
} from "@/services/dashboard-data.service";

import type { DashboardData } from "@/types/dashboard";

interface UseDashboardDataResult {
  data: DashboardData | null;
  isLoading: boolean;
  error: string | null;
  refresh: () => void;
}

export function useDashboardData(
  filters: DashboardApiFilters,
): UseDashboardDataResult {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const refresh = useCallback(() => {
    setRefreshKey((key) => key + 1);
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function loadDashboard() {
      setIsLoading(true);
      setError(null);

      try {
        const result = await getDashboardData(filters);

        if (!isMounted) {
          return;
        }

        setData(result);
      } catch (err: unknown) {
        if (!isMounted) {
          return;
        }

        console.error("Dashboard API error:", err);

        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Unable to load dashboard data.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      isMounted = false;
    };
  }, [
    filters.search,
    filters.state,
    filters.category,
    filters.fromPeriod,
    filters.toPeriod,
    refreshKey,
  ]);

  return {
    data,
    isLoading,
    error,
    refresh,
  };
}