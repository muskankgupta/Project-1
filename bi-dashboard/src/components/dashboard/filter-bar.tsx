"use client";

import { useEffect, useMemo, useState } from "react";
import { Search, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

import type { DashboardData } from "@/types/dashboard";

export interface DashboardFilters {
  search: string;
  state: string | null;
  category: string | null;
  fromPeriod: string | null;
  toPeriod: string | null;
}

interface FilterBarProps {
  data: DashboardData | null;
  filters: DashboardFilters;
  onFiltersChange: (filters: DashboardFilters) => void;
}

const PERIODS = [
  "2022-03",
  "2022-04",
  "2022-05",
  "2022-06",
] as const;

/** Derive the distinct states and categories present in the data. */
function useAvailableValues(data: DashboardData | null) {
  return useMemo(() => {
    const states = new Set<string>();
    const categories = new Set<string>();

    for (const state of data?.topStates ?? []) {
      states.add(state.state);
    }
    for (const item of data?.topPerformers ?? []) {
      if (item.category) categories.add(item.category);
    }
    for (const item of data?.worstPerformers ?? []) {
      if (item.category) categories.add(item.category);
    }

    return {
      states: Array.from(states).sort(),
      categories: Array.from(categories).sort(),
    };
  }, [data]);
}

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

  useEffect(() => {
    const handler = () => setOpen(false);
    document.addEventListener("click", handler);
    return () => document.removeEventListener("click", handler);
  }, []);

  return (
    <div
      className="relative"
      onClick={(event) => event.stopPropagation()}
    >
      <Button
        type="button"
        variant="ghost"
        className={cn(
          "h-9 whitespace-nowrap rounded-2xl border px-3 text-xs font-medium",
          value
            ? "border-cyan-400/30 text-cyan-200"
            : "border-white/10 text-zinc-400",
        )}
        onClick={() => setOpen((openValue) => !openValue)}
        aria-label={`${label} filter`}
      >
        {label}
      </Button>

      {open && (
        <div className="absolute left-0 z-40 mt-2 max-h-64 w-52 overflow-y-auto rounded-2xl border border-white/10 bg-[#0a0f1e] p-1.5 shadow-2xl">
          <button
            type="button"
            className="flex w-full items-center justify-between rounded-xl px-3 py-2 text-left text-xs text-zinc-300 transition hover:bg-white/5"
            onClick={() => onChange(null)}
          >
            <span>All</span>
            {value === null && <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />}
          </button>
          {options.map((option) => (
            <button
              key={option}
              type="button"
              className="flex w-full items-center justify-between rounded-xl px-3 py-2 text-left text-xs text-zinc-300 transition hover:bg-white/5"
              onClick={() => onChange(option)}
            >
              <span>{option}</span>
              {value === option && <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export function FilterBar({ data, filters, onFiltersChange }: FilterBarProps) {
  const { states, categories } = useAvailableValues(data);
  const [search, setSearch] = useState(filters.search);

  const activeCount =
    (filters.state ? 1 : 0) +
    (filters.category ? 1 : 0) +
    (filters.fromPeriod ? 1 : 0) +
    (filters.toPeriod ? 1 : 0);

  const applySearch = (value: string) => {
    setSearch(value);
    onFiltersChange({ ...filters, search: value });
  };

  const clearAll = () => {
    setSearch("");
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
      <div className="relative min-w-[200px] flex-1 sm:max-w-xs">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-zinc-500" />
        <Input
          value={search}
          onChange={(event) => applySearch(event.target.value)}
          placeholder="Search states, categories, KPIs…"
          className="h-9 pl-9 text-xs"
        />
        {filters.search && (
          <button
            type="button"
            aria-label="Clear search"
            onClick={() => applySearch("")}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        )}
      </div>

      <SelectChip
        label="State"
        value={filters.state}
        options={states}
        onChange={(state) => onFiltersChange({ ...filters, state })}
      />

      <SelectChip
        label="Category"
        value={filters.category}
        options={categories}
        onChange={(category) => onFiltersChange({ ...filters, category })}
      />

      <SelectChip
        label="From"
        value={filters.fromPeriod}
        options={Array.from(PERIODS)}
        onChange={(fromPeriod) => onFiltersChange({ ...filters, fromPeriod })}
      />

      <SelectChip
        label="To"
        value={filters.toPeriod}
        options={Array.from(PERIODS)}
        onChange={(toPeriod) => onFiltersChange({ ...filters, toPeriod })}
      />

      {activeCount > 0 && (
        <Button
          type="button"
          variant="ghost"
          className="h-9 rounded-2xl border border-white/10 px-3 text-xs text-zinc-400"
          onClick={clearAll}
        >
          Clear ({activeCount})
        </Button>
      )}
    </div>
  );
}

