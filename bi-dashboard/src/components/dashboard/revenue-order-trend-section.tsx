"use client";

import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { SectionEmptyState, SectionLoadingState } from "@/components/dashboard/section-state";
import { formatCompactCurrency, formatNumber } from "@/lib/dashboard-format";

import type { RevenueOrderTrendPoint } from "@/types/dashboard";

interface RevenueOrderTrendSectionProps {
  data: RevenueOrderTrendPoint[];
  isLoading: boolean;
}

export function RevenueOrderTrendSection({ data, isLoading }: RevenueOrderTrendSectionProps) {
  if (isLoading) {
    return <SectionLoadingState title="Revenue vs Order Trend" description="Loading time-series data." />;
  }

  if (data.length === 0) {
    return (
      <SectionEmptyState
        title="No trend data available"
        description="The revenue and order trend will render here once the backend data is connected."
      />
    );
  }

  return (
    <Card className="bg-white/6">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle>Revenue vs Order Trend</CardTitle>
            <CardDescription>Combined time-series view for revenue and order volume.</CardDescription>
          </div>
          <Badge>API-ready</Badge>
        </div>
      </CardHeader>
      <CardContent className="h-[340px] pb-8">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data}>
            <defs>
              <linearGradient id="revenueTrendFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.45} />
                <stop offset="100%" stopColor="#22d3ee" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
            <XAxis dataKey="period" tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
            <YAxis
              yAxisId="left"
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(value) => formatCompactCurrency(value as number)}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(value) => formatNumber(value as number)}
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
            <Area
              yAxisId="left"
              type="monotone"
              dataKey="revenue"
              name="Revenue"
              stroke="#22d3ee"
              fill="url(#revenueTrendFill)"
              strokeWidth={3}
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="orders"
              name="Orders"
              stroke="#f97316"
              strokeWidth={3}
              dot={{ r: 4, fill: "#f97316", strokeWidth: 0 }}
              activeDot={{ r: 6 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}