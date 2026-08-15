"use client";

import { useMemo, useState } from "react";
import { Search, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

import type { DashboardData } from "@/types/dashboard";

/* =========================================================
   SHARED DASHBOARD FILTER TYPE
   ========================================================= */

export interface DashboardFilters {
  search: string;
  state: string | null;
  category: string | null;
  fromPeriod: string | null;
  toPeriod: string | null;
}

/* =========================================================
   PROPS
   ========================================================= */

interface FilterBarProps {
  data: DashboardData | null;
  filters: DashboardFilters;
  onFiltersChange: (filters: DashboardFilters) => void;
}

/* =========================================================
   AVAILABLE FILTER VALUES
   ========================================================= */

function getAvailableValues(data: DashboardData | null) {
  return {
    states: Array.from(
      new Set(
        (data?.topStates ?? [])
          .map((item) => item.state)
          .filter(Boolean),
      ),
    ).sort(),

    categories: Array.from(
      new Set(
        [
          ...(data?.topPerformers ?? []),
          ...(data?.worstPerformers ?? []),
        ]
          .flatMap((item) => [
            item.category,
            item.name,
          ])
          .filter(Boolean),
      ),
    ).sort(),

    periods: Array.from(
      new Set(
        [
          ...(data?.revenueOrderTrend ?? []),
          ...(data?.aovTrend ?? []),
        ]
          .map((item) => item.period?.slice(0, 7))
          .filter(Boolean),
      ),
    ).sort(),
  };
}

/* =========================================================
   SELECT CHIP
   ========================================================= */

function SelectChip({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string | null;
  options: string[];
  onChange: (value: string | null) => void;
}) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <Button
        type="button"
        variant="ghost"
        className={cn(
          "h-9 whitespace-nowrap rounded-2xl border px-3 text-xs font-medium",
          value
            ? "border-cyan-400/30 text-cyan-200"
            : "border-white/10 text-zinc-400",
        )}
        onClick={() => setOpen((current) => !current)}
      >
        {label}

        {value && (
          <span className="ml-1.5 max-w-28 truncate text-cyan-300">
            {value}
          </span>
        )}
      </Button>

      {open && (
        <div
          className="absolute left-0 top-full z-50 mt-2 max-h-64 w-56 overflow-y-auto rounded-2xl border border-white/10 bg-[#0a0f1e] p-1.5 shadow-2xl"
          onClick={(event) => event.stopPropagation()}
        >
          <button
            type="button"
            className="flex w-full items-center justify-between rounded-xl px-3 py-2 text-left text-xs text-zinc-300 hover:bg-white/5"
            onClick={() => {
              onChange(null);
              setOpen(false);
            }}
          >
            <span>All</span>

            {value === null && (
              <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
            )}
          </button>

          {options.map((option) => (
            <button
              key={option}
              type="button"
              className="flex w-full items-center justify-between rounded-xl px-3 py-2 text-left text-xs text-zinc-300 hover:bg-white/5"
              onClick={() => {
                onChange(option);
                setOpen(false);
              }}
            >
              <span>{option}</span>

              {value === option && (
                <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

/* =========================================================
   FILTER BAR
   ========================================================= */

export function FilterBar({
  data,
  filters,
  onFiltersChange,
}: FilterBarProps) {
  const { states, categories, periods } =
    getAvailableValues(data);

  const [searchInput, setSearchInput] = useState(
    filters.search,
  );

  const activeCount =
    (filters.search ? 1 : 0) +
    (filters.state ? 1 : 0) +
    (filters.category ? 1 : 0) +
    (filters.fromPeriod ? 1 : 0) +
    (filters.toPeriod ? 1 : 0);

  const updateFilters = (
    changes: Partial<DashboardFilters>,
  ) => {
    onFiltersChange({
      ...filters,
      ...changes,
    });
  };

  const clearAll = () => {
    setSearchInput("");

    onFiltersChange({
      search: "",
      state: null,
      category: null,
      fromPeriod: null,
      toPeriod: null,
    });
  };

  return (
    <div className="flex flex-wrap items-center gap-2">
      {/* Search */}

      <div className="relative min-w-[220px] flex-1">
        <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-500" />

        <Input
          value={searchInput}
          onChange={(event) => {
            const value = event.target.value;

            setSearchInput(value);

            updateFilters({
              search: value,
            });
          }}
          placeholder="Search states, categories, KPIs..."
          className="h-9 pl-9 pr-9 text-xs"
        />

        {searchInput && (
          <button
            type="button"
            aria-label="Clear search"
            onClick={() => {
              setSearchInput("");

              updateFilters({
                search: "",
              });
            }}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* State */}

      <SelectChip
        label="State"
        value={filters.state}
        options={states}
        onChange={(state) =>
          updateFilters({ state })
        }
      />

      {/* Category */}

      <SelectChip
        label="Category"
        value={filters.category}
        options={categories}
        onChange={(category) =>
          updateFilters({ category })
        }
      />

      {/* From */}

      <SelectChip
        label="From"
        value={filters.fromPeriod}
        options={periods}
        onChange={(fromPeriod) =>
          updateFilters({ fromPeriod })
        }
      />

      {/* To */}

      <SelectChip
        label="To"
        value={filters.toPeriod}
        options={periods}
        onChange={(toPeriod) =>
          updateFilters({ toPeriod })
        }
      />

      {/* Clear */}

      {activeCount > 0 && (
        <Button
          type="button"
          variant="ghost"
          className="h-9 rounded-2xl border border-white/10 px-3 text-xs text-zinc-400 hover:text-white"
          onClick={clearAll}
        >
          Clear ({activeCount})
        </Button>
      )}
    </div>
  );
}