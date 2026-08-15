import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { SectionEmptyState, SectionLoadingState } from "@/components/dashboard/section-state";
import { formatCompactCurrency, formatNumber, formatSignedPercent } from "@/lib/dashboard-format";

import type { KpiMetric } from "@/types/dashboard";

interface KpiSectionProps {
  data: KpiMetric[];
  isLoading: boolean;
}

function KpiCard({ metric }: { metric: KpiMetric }) {
  const TrendIcon = metric.trend === "up" ? ArrowUpRight : metric.trend === "down" ? ArrowDownRight : Minus;
  const badgeClassName =
    metric.trend === "down"
      ? "border-rose-400/20 bg-rose-400/10 text-rose-100"
      : metric.trend === "flat"
        ? "border-white/10 bg-white/5 text-zinc-200"
        : "border-emerald-400/20 bg-emerald-400/10 text-emerald-100";

  const value =
    metric.format === "currency"
      ? formatCompactCurrency(metric.value)
      : metric.format === "number"
        ? formatNumber(metric.value)
        : metric.format === "decimal"
          ? metric.value.toFixed(1)
          : formatSignedPercent(metric.value);

  return (
    <Card className="bg-white/6">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm text-zinc-400">{metric.label}</p>
            <div className="mt-3 text-3xl font-semibold tracking-tight text-white">{value}</div>
          </div>
          <Badge className={badgeClassName}>
            <TrendIcon className="h-3.5 w-3.5" />
            {formatSignedPercent(metric.delta)}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}

export function KpiSection({ data, isLoading }: KpiSectionProps) {
  if (isLoading) {
    return <SectionLoadingState title="KPI Section" description="Loading core metrics." />;
  }

  if (data.length === 0) {
    return (
      <SectionEmptyState
        title="No KPI data available"
        description="The KPI cards will render here once the backend or mock source provides metrics."
      />
    );
  }

  return (
    <section className="grid gap-4 md:grid-cols-2 2xl:grid-cols-4">
      {data.map((metric) => (
        <KpiCard key={metric.id} metric={metric} />
      ))}
    </section>
  );
}