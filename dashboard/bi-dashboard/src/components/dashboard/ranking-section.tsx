"use client";

import { ChevronRight } from "lucide-react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { SectionEmptyState, SectionLoadingState } from "@/components/dashboard/section-state";
import { formatCompactCurrency, formatNumber, formatSignedPercent } from "@/lib/dashboard-format";

import type { RankingItem } from "@/types/dashboard";

interface RankingSectionProps {
  title: string;
  description: string;
  badgeLabel: string;
  data: RankingItem[];
  isLoading: boolean;
}

export function RankingSection({ title, description, badgeLabel, data, isLoading }: RankingSectionProps) {
  if (isLoading) {
    return <SectionLoadingState title={title} description={description} />;
  }

  if (data.length === 0) {
    return (
      <SectionEmptyState
        title={`No data for ${title.toLowerCase()}`}
        description="Ranking data will appear here once the backend starts returning products or categories."
      />
    );
  }

  return (
    <Card className="bg-white/6">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle>{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </div>
          <Badge>{badgeLabel}</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid gap-3">
          {data.map((item, index) => (
            <div
              key={item.id}
              className="rounded-3xl border border-white/10 bg-white/5 p-4 transition hover:border-white/20 hover:bg-white/7"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <div className="flex items-center gap-3">
                    <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-sm font-semibold text-white">
                      {index + 1}
                    </span>
                    <div className="min-w-0">
                      <p className="truncate font-medium text-white">{item.name}</p>
                      <p className="text-sm text-zinc-500">{item.category}</p>
                    </div>
                  </div>
                </div>

                <ChevronRight className="mt-1 h-4 w-4 shrink-0 text-zinc-500" />
              </div>

              <div className="mt-4 grid gap-3 sm:grid-cols-3">
                <div className="rounded-2xl border border-white/10 bg-black/10 px-3 py-3">
                  <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">{badgeLabel}</p>
                  <p className="mt-1 text-base font-semibold text-white">{formatCompactCurrency(item.value)}</p>
                </div>
                <div className="rounded-2xl border border-white/10 bg-black/10 px-3 py-3">
                  <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">Momentum</p>
                  <p className="mt-1 text-base font-semibold text-white">{formatSignedPercent(item.change)}</p>
                </div>
                <div className="rounded-2xl border border-white/10 bg-black/10 px-3 py-3">
                  <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">Share</p>
                  <p className="mt-1 text-base font-semibold text-white">{formatNumber(item.share)}%</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="h-[240px] rounded-3xl border border-white/10 bg-black/10 p-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical">
              <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
              <XAxis
                type="number"
                tick={{ fill: "#94a3b8", fontSize: 12 }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(value) => formatCompactCurrency(value as number)}
              />
              <YAxis
                type="category"
                dataKey="name"
                width={140}
                tick={{ fill: "#94a3b8", fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{
                  background: "rgba(5, 8, 22, 0.92)",
                  border: "1px solid rgba(255,255,255,0.12)",
                  borderRadius: 20,
                  color: "#fff",
                }}
                formatter={(value) => [formatCompactCurrency(Number(value ?? 0)), badgeLabel]}
              />
              <Bar dataKey="value" radius={[0, 16, 16, 0]} fill="#22d3ee" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}