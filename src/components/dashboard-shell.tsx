"use client";

import { Bell, ChevronDown, LayoutDashboard, LucideIcon, Menu, Search, Settings, ShieldAlert, Sparkles, TrendingUp, Users, Wallet, LineChart, FileText, BarChart3 } from "lucide-react";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Avatar } from "@/components/ui/avatar";

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

const revenueData = [
  { month: "Jan", value: 32 },
  { month: "Feb", value: 38 },
  { month: "Mar", value: 42 },
  { month: "Apr", value: 48 },
  { month: "May", value: 54 },
  { month: "Jun", value: 60 },
  { month: "Jul", value: 68 },
];

const pipelineData = [
  { name: "Enterprise", value: 84 },
  { name: "Mid-Market", value: 66 },
  { name: "SMB", value: 41 },
  { name: "Partners", value: 58 },
];

const metrics = [
  { label: "Monthly Revenue", value: "$2.84M", delta: "+14.8%" },
  { label: "Active Accounts", value: "1,248", delta: "+8.2%" },
  { label: "Conversion Rate", value: "17.4%", delta: "+2.1%" },
  { label: "Forecast Accuracy", value: "96.1%", delta: "+1.4%" },
];

const updates = [
  "Revenue concentration improved in EMEA and North America.",
  "Enterprise pipeline closed 3 large accounts ahead of schedule.",
  "Churn risk down 12% after product usage nudges launched.",
];

function MetricCard({
  label,
  value,
  delta,
}: {
  label: string;
  value: string;
  delta: string;
}) {
  return (
    <Card className="p-0 bg-white/6">
      <CardContent className="p-5">
        <p className="text-sm text-zinc-400">{label}</p>
        <div className="mt-3 flex items-end justify-between gap-4">
          <div className="text-3xl font-semibold tracking-tight text-white">{value}</div>
          <Badge className="border-emerald-400/20 bg-emerald-400/10 text-emerald-100">
            {delta}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}

export function DashboardShell() {
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
                <Button variant="ghost" className="xl:hidden px-3">
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

          <section className="grid gap-4 md:grid-cols-2 2xl:grid-cols-4">
            {metrics.map((metric) => (
              <MetricCard key={metric.label} {...metric} />
            ))}
          </section>

          <section className="grid gap-5 xl:grid-cols-[minmax(0,1.6fr)_minmax(320px,0.8fr)]">
            <Card className="overflow-hidden bg-white/6">
              <CardHeader className="flex items-start justify-between gap-4">
                <div>
                  <CardTitle>Revenue Momentum</CardTitle>
                  <CardDescription>Rolling 7-month trend across active portfolios</CardDescription>
                </div>
                <Badge>+18.6% YoY</Badge>
              </CardHeader>
              <CardContent className="h-[340px] pb-8">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={revenueData}>
                    <defs>
                      <linearGradient id="revenueFill" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.45} />
                        <stop offset="100%" stopColor="#22d3ee" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
                    <XAxis dataKey="month" tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
                    <Tooltip
                      contentStyle={{
                        background: "rgba(5, 8, 22, 0.92)",
                        border: "1px solid rgba(255,255,255,0.12)",
                        borderRadius: 20,
                        color: "#fff",
                      }}
                    />
                    <Area type="monotone" dataKey="value" stroke="#22d3ee" fill="url(#revenueFill)" strokeWidth={3} />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card className="bg-white/6">
              <CardHeader>
                <CardTitle>AI Insights Reserve</CardTitle>
                <CardDescription>Reserved for future model-driven recommendations</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="rounded-3xl border border-dashed border-cyan-400/20 bg-cyan-400/5 p-5">
                  <div className="flex items-center gap-3">
                    <Sparkles className="h-5 w-5 text-cyan-300" />
                    <p className="font-medium text-white">Insight workspace</p>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-zinc-400">
                    A dedicated panel for recommendations, anomaly detection, and narrative
                    summaries can live here without changing the core layout.
                  </p>
                </div>

                <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
                  <p className="text-sm font-medium text-zinc-300">Current indicators</p>
                  <div className="mt-4 space-y-3">
                    {updates.map((item) => (
                      <div key={item} className="flex gap-3 text-sm text-zinc-400">
                        <ShieldAlert className="mt-0.5 h-4 w-4 shrink-0 text-amber-300" />
                        <span>{item}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </section>

          <section className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_minmax(360px,0.85fr)]">
            <Card className="bg-white/6">
              <CardHeader>
                <CardTitle>Sales Channel Mix</CardTitle>
                <CardDescription>Performance by revenue source over the last quarter</CardDescription>
              </CardHeader>
              <CardContent className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={pipelineData}>
                    <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
                    <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false} />
                    <Tooltip
                      contentStyle={{
                        background: "rgba(5, 8, 22, 0.92)",
                        border: "1px solid rgba(255,255,255,0.12)",
                        borderRadius: 20,
                        color: "#fff",
                      }}
                    />
                    <Bar dataKey="value" radius={[16, 16, 4, 4]} fill="#38bdf8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <div className="grid gap-5">
              <Card className="bg-white/6">
                <CardHeader>
                  <CardTitle>Operational Summary</CardTitle>
                  <CardDescription>Reusable KPI blocks for executive review</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    ["Pipeline coverage", "3.8x target"],
                    ["Avg. deal velocity", "27 days"],
                    ["Renewal rate", "91.2%"],
                  ].map(([label, value]) => (
                    <div key={label} className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
                      <span className="text-sm text-zinc-400">{label}</span>
                      <span className="text-sm font-semibold text-white">{value}</span>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-cyan-400/10 to-blue-400/5">
                <CardHeader>
                  <CardTitle>Enterprise Ready</CardTitle>
                  <CardDescription>Glassmorphism, dark theme, and responsive composition</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm leading-6 text-zinc-300">
                    The layout is split into reusable sections so the navigation, charts, and AI
                    panel can be extended independently without restructuring the page.
                  </p>
                </CardContent>
              </Card>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}