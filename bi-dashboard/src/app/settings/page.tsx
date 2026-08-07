"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  BarChart3,
  Database,
  Info,
  Layers,
  LogOut,
  RefreshCw,
  Server,
  Sparkles,
  User,
  Check,
} from "lucide-react";

import { AppLayout } from "@/components/app-layout";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/status-badge";
import { useApiStatus, type ServiceStatus } from "@/hooks/use-api-status";
import { useTheme, type ThemeMode } from "@/lib/theme-provider";
import { useAuth } from "@/providers/auth-provider";
import { API_BASE_URL } from "@/lib/api-config";

const APP_VERSION = "2.0.0";

const THEME_OPTIONS: Array<{ value: ThemeMode; label: string; hint: string }> = [
  { value: "light", label: "Light", hint: "Bright, high-contrast interface" },
  { value: "dark", label: "Dark", hint: "Dimmed surfaces, ideal for low light" },
  { value: "system", label: "System", hint: "Follow your operating system" },
];

export default function SettingsPage() {
  const { status, refresh } = useApiStatus();
  const { theme, setTheme } = useTheme();
  const { user, logout } = useAuth();
  const router = useRouter();

  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    await refresh();
    setRefreshing(false);
  };

  const handleLogout = () => {
    logout();
    router.replace("/login");
  };

  const providerLabel = status.provider ? status.provider.toUpperCase() : "Fallback (no provider key)";

  return (
    <AppLayout
      title="Settings"
      subtitle="Manage your workspace, appearance, and integrations"
      active="settings"
    >
      <div className="grid gap-5 xl:grid-cols-2">
        {/* Appearance */}
        <Card className="bg-white/6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-cyan-400" />
              Appearance
            </CardTitle>
            <CardDescription>Choose how MetricMind looks on this device.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {THEME_OPTIONS.map((option) => {
              const active = option.value === theme;

              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setTheme(option.value)}
                  className={`flex w-full items-center justify-between rounded-2xl border px-4 py-3 text-left transition ${
                    active
                      ? "border-cyan-400/30 bg-cyan-400/10"
                      : "border-white/10 bg-white/5 hover:bg-white/10"
                  }`}
                >
                  <div>
                    <p className="text-sm font-medium text-white">{option.label}</p>
                    <p className="mt-0.5 text-xs text-zinc-500">{option.hint}</p>
                  </div>
                  {active && <Check className="h-4 w-4 text-cyan-400" />}
                </button>
              );
            })}
          </CardContent>
        </Card>

        {/* Profile */}
        <Card className="bg-white/6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-4 w-4 text-cyan-400" />
              Profile
            </CardTitle>
            <CardDescription>Your local session details.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4 rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-200">
                {user?.initials ?? "U"}
              </div>
              <div>
                <p className="font-medium text-white">{user?.name ?? "Signed out"}</p>
                <p className="text-sm text-zinc-400">{user?.email}</p>
                <p className="mt-0.5 text-xs text-zinc-500">{user?.role}</p>
              </div>
            </div>

            <Button
              variant="ghost"
              className="w-full border-rose-400/20 text-rose-300 hover:bg-rose-400/10"
              onClick={handleLogout}
            >
              <LogOut className="h-4 w-4" />
              Sign out
            </Button>
          </CardContent>
        </Card>

        {/* API Status */}
        <Card className="bg-white/6">
          <CardHeader>
            <div className="flex items-center justify-between gap-3">
              <CardTitle className="flex items-center gap-2">
                <Server className="h-4 w-4 text-cyan-400" />
                API Status
              </CardTitle>
              <Button
                variant="ghost"
                className="px-3"
                onClick={handleRefresh}
                disabled={refreshing}
              >
                <RefreshCw className={`h-4 w-4 ${refreshing ? "animate-spin" : ""}`} />
                Refresh
              </Button>
            </div>
            <CardDescription>Live connectivity from the MetricMind backend.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <StatusRow
                icon={<Server className="h-4 w-4" />}
                label="Backend"
                detail={`${API_BASE_URL}`}
                status={status.backend}
              />
              <StatusRow
                icon={<Layers className="h-4 w-4" />}
                label="Semantic Layer"
                detail={status.health?.semantic_layer ?? "—"}
                status={status.semanticLayer}
              />
              <StatusRow
                icon={<Database className="h-4 w-4" />}
                label="Databricks"
                detail={status.health?.databricks ?? "—"}
                status={status.databricks}
              />
              <StatusRow
                icon={<Sparkles className="h-4 w-4" />}
                label="LLM"
                detail={providerLabel}
                status={status.llm}
              />
            </div>

            {status.checkedAt && (
              <p className="mt-4 text-xs text-zinc-500">
                Last checked {status.checkedAt.toLocaleTimeString()}
              </p>
            )}
          </CardContent>
        </Card>

        {/* About */}
        <Card className="bg-white/6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Info className="h-4 w-4 text-cyan-400" />
              About
            </CardTitle>
            <CardDescription>MetricMind platform information.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4 rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-cyan-400/15 text-cyan-200">
                <BarChart3 className="h-5 w-5" />
              </div>
              <div>
                <p className="font-medium text-white">MetricMind BI</p>
                <p className="text-sm text-zinc-400">
                  Agentic Natural Language → SQL Business Intelligence
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
                <p className="text-xs uppercase tracking-wide text-zinc-500">Version</p>
                <p className="mt-1 font-semibold text-white">v{APP_VERSION}</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
                <p className="text-xs uppercase tracking-wide text-zinc-500">Peer</p>
                <Badge className="mt-1">Semantic + FastAPI</Badge>
              </div>
            </div>

            <p className="text-xs leading-5 text-zinc-500">
              MetricMind analyzes Amazon.in sales data across revenue, orders, fulfillment,
              states, categories, and order status — powered by a multi-agent pipeline and a
              shared semantic layer.
            </p>
          </CardContent>
        </Card>
      </div>
    </AppLayout>
  );
}

function StatusRow({
  icon,
  label,
  detail,
  status,
}: {
  icon: React.ReactNode;
  label: string;
  detail: string;
  status: ServiceStatus;
}) {
  return (
    <div className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
      <div className="flex items-center gap-3">
        <span className="text-zinc-400">{icon}</span>
        <div>
          <p className="text-sm font-medium text-white">{label}</p>
          <p className="max-w-[220px] truncate text-xs text-zinc-500">{detail}</p>
        </div>
      </div>
      <StatusBadge status={status} />
    </div>
  );
}

