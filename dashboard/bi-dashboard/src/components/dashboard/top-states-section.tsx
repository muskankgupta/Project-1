"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { SectionEmptyState, SectionLoadingState } from "@/components/dashboard/section-state";
import { formatCompactCurrency, formatNumber, formatPercent } from "@/lib/dashboard-format";

import type { TopStatePoint } from "@/types/dashboard";

interface TopStatesSectionProps {
  data: TopStatePoint[];
  isLoading: boolean;
}

export function TopStatesSection({ data, isLoading }: TopStatesSectionProps) {
  if (isLoading) {
    return <SectionLoadingState title="Top States" description="Loading state ranking data." />;
  }

  if (data.length === 0) {
    return (
      <SectionEmptyState
        title="No state ranking data available"
        description="State-level sales rankings will render here once the backend is connected."
      />
    );
  }

  return (
    <Card className="bg-white/6">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle>Top States</CardTitle>
            <CardDescription>Ranked sales contribution from the highest-performing states.</CardDescription>
          </div>
          <Badge>Regional heat map</Badge>
        </div>
      </CardHeader>
      <CardContent className="h-[380px] pb-8">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 12 }}>
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
              dataKey="state"
              width={120}
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
              formatter={(value, name) => {
                const numericValue = Number(value ?? 0);

                if (name === "Sales") {
                  return [formatCompactCurrency(numericValue), name];
                }

                if (name === "Orders") {
                  return [formatNumber(numericValue), name];
                }

                return [formatPercent(numericValue), name];
              }}
            />
            <Bar dataKey="sales" name="Sales" radius={[0, 16, 16, 0]} fill="#22d3ee" />
          </BarChart>
        </ResponsiveContainer>

        <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
          {data.map((item, index) => (
            <div key={item.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">Rank {index + 1}</p>
              <p className="mt-2 text-sm font-medium text-white">{item.state}</p>
              <p className="mt-1 text-sm text-zinc-400">{formatCompactCurrency(item.sales)}</p>
              <p className="mt-3 text-xs text-zinc-500">{formatNumber(item.orders)} orders</p>
              <p className="text-xs text-cyan-200">{formatPercent(item.share)} share</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}