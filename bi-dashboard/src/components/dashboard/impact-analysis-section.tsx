"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { SectionEmptyState, SectionLoadingState } from "@/components/dashboard/section-state";
import { formatCompactCurrency, formatNumber, formatPercent } from "@/lib/dashboard-format";

import type { ImpactAnalysisData, ImpactStatusMetric } from "@/types/dashboard";

interface ImpactAnalysisSectionProps {
  data: ImpactAnalysisData;
  isLoading: boolean;
}

function ImpactMetricCard({ status }: { status: ImpactStatusMetric }) {
  return (
    <Card className="bg-white/6">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm text-zinc-400">{status.label}</p>
            <div className="mt-3 text-2xl font-semibold tracking-tight text-white">
              {formatNumber(status.orders)}
            </div>
            <p className="mt-1 text-sm text-zinc-500">orders</p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 px-3 py-2 text-right">
            <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">Revenue</p>
            <p className="mt-1 text-sm font-semibold text-white">
              {formatCompactCurrency(status.revenue)}
            </p>
          </div>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
            <p className="text-zinc-500">Order share</p>
            <p className="mt-1 font-semibold text-white">{formatPercent(status.orderShare)}</p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
            <p className="text-zinc-500">Revenue share</p>
            <p className="mt-1 font-semibold text-white">{formatPercent(status.revenueShare)}</p>
          </div>
        </div>

        <div className="mt-5 h-2 overflow-hidden rounded-full bg-white/10">
          <div
            className="h-full rounded-full"
            style={{ backgroundColor: status.color, width: `${Math.max(status.revenueShare, 6)}%` }}
          />
        </div>
      </CardContent>
    </Card>
  );
}

export function ImpactAnalysisSection({ data, isLoading }: ImpactAnalysisSectionProps) {
  if (isLoading) {
    return <SectionLoadingState title="Impact Analysis" description="Loading order impact visuals." />;
  }

  if (data.statuses.length === 0 || data.comparison.length === 0) {
    return (
      <SectionEmptyState
        title="No impact analysis data available"
        description="Delivered and cancelled order impact will render here when the data source is connected."
      />
    );
  }

  return (
    <section className="grid gap-5 xl:grid-cols-[minmax(0,0.95fr)_minmax(0,1.1fr)]">
      <div className="grid gap-5 md:grid-cols-2">
        {data.statuses.map((status) => (
          <ImpactMetricCard key={status.id} status={status} />
        ))}
      </div>

      <Card className="bg-white/6">
        <CardHeader>
          <div className="flex items-start justify-between gap-3">
            <div>
              <CardTitle>Delivered vs Cancelled Impact</CardTitle>
              <CardDescription>Compare contribution to revenue and order count.</CardDescription>
            </div>
            <Badge>Order / revenue mix</Badge>
          </div>
        </CardHeader>
        <CardContent className="h-[320px] pb-8">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.comparison}>
              <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="label" tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis yAxisId="left" tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis
                yAxisId="right"
                orientation="right"
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

                  if (name === "Revenue") {
                    return [formatCompactCurrency(numericValue), name];
                  }

                  return [formatNumber(numericValue), name];
                }}
              />
              <Bar yAxisId="left" dataKey="orders" name="Orders" radius={[14, 14, 4, 4]} fill="#22d3ee" />
              <Bar yAxisId="right" dataKey="revenue" name="Revenue" radius={[14, 14, 4, 4]} fill="#fb7185" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </section>
  );
}