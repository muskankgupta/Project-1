"use client";

import { Area, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { SectionEmptyState, SectionLoadingState } from "@/components/dashboard/section-state";
import { formatCurrency } from "@/lib/dashboard-format";

import type { AovTrendPoint } from "@/types/dashboard";

interface AovTrendSectionProps {
  data: AovTrendPoint[];
  isLoading: boolean;
}

export function AovTrendSection({ data, isLoading }: AovTrendSectionProps) {
  if (isLoading) {
    return <SectionLoadingState title="AOV Trend" description="Loading average order value data." />;
  }

  if (data.length === 0) {
    return (
      <SectionEmptyState
        title="No AOV trend data available"
        description="Average order value will render here once the backend data is connected."
      />
    );
  }

  return (
    <Card className="bg-white/6">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle>AOV Trend</CardTitle>
            <CardDescription>Average order value movement over time.</CardDescription>
          </div>
          <Badge>Order quality</Badge>
        </div>
      </CardHeader>
      <CardContent className="h-[320px] pb-8">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <defs>
              <linearGradient id="aovFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity={0.35} />
                <stop offset="100%" stopColor="#38bdf8" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
            <XAxis dataKey="period" tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
            <YAxis
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(value) => formatCurrency(value as number)}
            />
            <Tooltip
              contentStyle={{
                background: "rgba(5, 8, 22, 0.92)",
                border: "1px solid rgba(255,255,255,0.12)",
                borderRadius: 20,
                color: "#fff",
              }}
              formatter={(value) => [formatCurrency(Number(value ?? 0)), "AOV"]}
            />
            <Area type="monotone" dataKey="aov" stroke="transparent" fill="url(#aovFill)" />
            <Line
              type="monotone"
              dataKey="aov"
              stroke="#38bdf8"
              strokeWidth={3}
              dot={{ r: 4, fill: "#38bdf8", strokeWidth: 0 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}