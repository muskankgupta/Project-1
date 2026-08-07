"use client";

import { useCallback, useEffect, useState } from "react";

import { getDashboardData } from "@/services/dashboard-data.service";

import type { DashboardData } from "@/types/dashboard";

interface UseDashboardDataResult {
  data: DashboardData | null;
  isLoading: boolean;
  error: string | null;
  refresh: () => void;
}

export function useDashboardData(): UseDashboardDataResult {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const refresh = useCallback(() => {
    setRefreshKey((key) => key + 1);
  }, []);

  useEffect(() => {
    let isMounted = true;

    setIsLoading(true);
    setError(null);

    getDashboardData()
      .then((result) => {
        if (!isMounted) {
          return;
        }

        setData(result);
      })
      .catch(() => {
        if (!isMounted) {
          return;
        }

        setError("Unable to load dashboard data.");
      })
      .finally(() => {
        if (!isMounted) {
          return;
        }

        setIsLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [refreshKey]);

  return { data, isLoading, error, refresh };
}
