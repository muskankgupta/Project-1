"use client";

import {
  Bell,
  ChevronDown,
  Download,
  LayoutDashboard,
  type LucideIcon,
  Menu,
  MessageSquareText,
  RefreshCw,
  Search,
  Settings,
  TrendingUp,
  Users,
  Wallet,
  LineChart,
  FileText,
  BarChart3,
} from "lucide-react";
import { ChatPanel } from "@/components/chat-panel";
import { useState } from "react";

import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { AovTrendSection } from "@/components/dashboard/aov-trend-section";
import { ImpactAnalysisSection } from "@/components/dashboard/impact-analysis-section";
import { KpiSection } from "@/components/dashboard/kpi-section";
import { RankingSection } from "@/components/dashboard/ranking-section";
import { RevenueOrderTrendSection } from "@/components/dashboard/revenue-order-trend-section";
import { TopStatesSection } from "@/components/dashboard/top-states-section";
import { useDashboardData } from "@/hooks/use-dashboard-data";

type NavItem = {
  label: string;
  icon: LucideIcon;
};

const navItems: NavItem[] = [
  { label: "Dashboard", icon: LayoutDashboard },
  { label: "Revenue", icon: Wallet },
  { label: "Sales", icon: TrendingUp },
  { label: "Customers", icon: Users },
  { label: "Forecast", icon: LineChart },
  { label: "Reports", icon: FileText },
  { label: "Settings", icon: Settings },
];

export function DashboardShell() {
  const { data, isLoading, refresh } = useDashboardData();
  const [chatOpen, setChatOpen] = useState(false);

  const meta = data?.meta;
  const isApiSource = meta?.source === "api";

  const handleExportCsv = () => {
    if (!data) {
      return;
    }

    const rows: string[][] = [
      ["Metric", "Period", "Value", "Share", "Category"],
    ];

    for (const kpi of data.kpis ?? []) {
      rows.push([kpi.label, "overall", String(kpi.value), "", ""]);
    }

    for (const point of data.revenueOrderTrend ?? []) {
      rows.push(["Revenue", point.period, String(point.revenue), "", ""]);
      rows.push(["Orders", point.period, String(point.orders), "", ""]);
    }

    for (const state of data.topStates ?? []) {
      rows.push(["Revenue by State", state.state, String(state.sales), String(state.share), ""]);
    }

    for (const item of data.topPerformers ?? []) {
      rows.push(["Top Performer", "", String(item.value), String(item.share), item.category]);
    }

    for (const item of data.worstPerformers ?? []) {
      rows.push(["Worst Performer", "", String(item.value), String(item.share), item.category]);
    }

    const csv = rows
      .map((row) =>
        row
          .map((cell) => `"${String(cell).replaceAll('"', '""')}"`)
          .join(","),
      )
      .join("\n");

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `axlero-bi-dashboard-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-transparent text-zinc-100">
      <div className="mx-auto flex min-h-screen max-w-[1800px] gap-5 p-4 lg:p-6">
        <aside className="hidden w-72 shrink-0 lg:flex">
          <Card className="flex w-full flex-col justify-between overflow-hidden bg-white/6 p-5">
            <div>
              <div className="flex items-center gap-3 rounded-3xl border border-white/10 bg-white/5 p-4">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-100">
                  <BarChart3 className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm font-medium text-zinc-400">Axlero Solutions</p>
                  <p className="text-lg font-semibold text-white">Business Intelligence</p>
                </div>
              </div>

              <nav className="mt-6 space-y-2">
                {navItems.map((item, index) => {
                  const Icon = item.icon;

                  return (
                    <button
                      key={item.label}
                      className={`flex w-full items-center gap-3 rounded-2xl border px-4 py-3 text-sm font-medium transition ${
                        index === 0
                          ? "border-cyan-400/25 bg-cyan-400/10 text-white"
                          : "border-white/5 bg-white/0 text-zinc-400 hover:border-white/10 hover:bg-white/5 hover:text-white"
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                      {item.label}
                    </button>
                  );
                })}
              </nav>
            </div>

            <Card className="mt-6 border-cyan-400/20 bg-cyan-400/10">
              <CardContent className="p-4">
                <Badge className="mb-3">Quarterly Spotlight</Badge>
                <p className="text-sm leading-6 text-cyan-50/90">
                  Revenue growth is tracking ahead of target with pipeline expansion in
                  enterprise accounts.
                </p>
              </CardContent>
            </Card>
          </Card>
        </aside>

        <main className="flex min-w-0 flex-1 flex-col gap-5">
          <Card className="sticky top-4 z-10 bg-white/6 px-4 py-4 lg:px-5">
            <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
              <div className="flex items-center gap-3">
                <Button variant="ghost" className="px-3 xl:hidden">
                  <Menu className="h-4 w-4" />
                </Button>
                <div>
                  <p className="text-sm text-zinc-400">Enterprise Command Center</p>
                  <h1 className="text-2xl font-semibold tracking-tight text-white md:text-3xl">
                    BI Dashboard Overview
                  </h1>
                </div>
              </div>

              <div className="flex flex-col gap-3 md:flex-row md:items-center">
                <div className="relative w-full md:w-[320px]">
                  <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-500" />
                  <Input className="pl-11" placeholder="Search revenue, accounts, reports" />
                </div>

                <div className="flex items-center gap-3">
                  <Badge
                    className={
                      isApiSource
                        ? "border-emerald-400/20 bg-emerald-400/10 text-emerald-100"
                        : "border-white/10 bg-white/5 text-zinc-300"
                    }
                    title={
                      isApiSource
                        ? "Live MetricMind backend"
                        : "Backend unreachable - showing bundled sample data"
                    }
                  >
                    {isApiSource ? "Live data" : "Sample data"}
                  </Badge>
                  <Button
                    variant="ghost"
                    className="px-3"
                    onClick={refresh}
                    disabled={isLoading}
                    title="Refresh dashboard data"
                    aria-label="Refresh dashboard data"
                  >
                    <RefreshCw
                      className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`}
                    />
                  </Button>
                  <Button
                    variant="ghost"
                    className="px-3"
                    onClick={handleExportCsv}
                    disabled={!data}
                    title="Export dashboard as CSV"
                    aria-label="Export dashboard as CSV"
                  >
                    <Download className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" className="px-3">
                    <Bell className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" className="px-4">
                    Dark Mode
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                  <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-3 py-2">
                    <Avatar>AM</Avatar>
                    <div className="hidden min-[420px]:block">
                      <p className="text-sm font-medium text-white">Amara Malik</p>
                      <p className="text-xs text-zinc-500">Finance Director</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          <KpiSection data={data?.kpis ?? []} isLoading={isLoading} />

          {/* Insights & explanation strip (visible only when the live API provides them) */}
          {meta && (meta.insights.length > 0 || meta.explanation) && (
            <Card className="border-cyan-400/10 bg-white/[0.03]">
              <CardContent className="p-5">
                <div className="mb-3 flex items-center gap-3">
                  <Badge className="text-cyan-200">
                    AI Insights
                  </Badge>
                  {meta.source === "api" && (
                    <span className="text-xs text-zinc-500">
                      Generated {new Date(meta.generatedAt).toLocaleString()}
                    </span>
                  )}
                </div>

                {meta.insights.length > 0 && (
                  <ul className="mb-4 space-y-2">
                    {meta.insights.map((insight, i) => (
                      <li
                        key={i}
                        className="flex items-start gap-3 text-sm leading-6 text-zinc-300"
                      >
                        <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-400" />
                        {insight}
                      </li>
                    ))}
                  </ul>
                )}

                {meta.explanation && (
                  <p className="text-sm leading-7 text-zinc-400">
                    {meta.explanation}
                  </p>
                )}
              </CardContent>
            </Card>
          )}

          <ImpactAnalysisSection
            data={data?.impactAnalysis ?? { statuses: [], comparison: [] }}
            isLoading={isLoading}
          />

          <section className="grid gap-5 xl:grid-cols-[minmax(0,1.35fr)_minmax(0,0.95fr)]">
            <RevenueOrderTrendSection data={data?.revenueOrderTrend ?? []} isLoading={isLoading} />
            <TopStatesSection data={data?.topStates ?? []} isLoading={isLoading} />
          </section>

          <section className="grid gap-5 xl:grid-cols-2">
            <RankingSection
              title="Top Performing Products/Categories"
              description="Reusable ranking block for any high-performing product or category data."
              badgeLabel="Top performers"
              data={data?.topPerformers ?? []}
              isLoading={isLoading}
            />
            <RankingSection
              title="Worst Performing Products/Categories"
              description="Reusable ranking block for underperforming product or category data."
              badgeLabel="Worst performers"
              data={data?.worstPerformers ?? []}
              isLoading={isLoading}
            />
          </section>

          <AovTrendSection data={data?.aovTrend ?? []} isLoading={isLoading} />
        </main>
      </div>

      {/* Chat launcher FAB */}
      <Button
        type="button"
        onClick={() => setChatOpen((open) => !open)}
        className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full p-0 shadow-lg shadow-cyan-500/20"
        aria-label={chatOpen ? "Close AI assistant" : "Open AI assistant"}
      >
        <MessageSquareText className="h-6 w-6" />
      </Button>

      <ChatPanel open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}
