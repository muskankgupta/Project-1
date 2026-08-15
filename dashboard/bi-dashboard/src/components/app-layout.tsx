"use client";

import { useState, type ReactNode } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  BarChart3,
  Bell,
  FileText,
  LayoutDashboard,
  LineChart,
  LogOut,
  Menu,
  MessageSquareText,
  Settings,
  TrendingUp,
  Users,
  Wallet,
  type LucideIcon,
} from "lucide-react";

import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { StatusBadge } from "@/components/status-badge";
import { ThemeToggle } from "@/components/theme-toggle";
import { ChatPanel } from "@/components/chat-panel";
import { useApiStatus } from "@/hooks/use-api-status";
import { useAuth } from "@/providers/auth-provider";
import { cn } from "@/lib/utils";

type NavKey =
  | "dashboard"
  | "revenue"
  | "sales"
  | "customers"
  | "forecast"
  | "reports"
  | "settings";

interface NavItem {
  key: NavKey;
  label: string;
  href: string;
  icon: LucideIcon;
}

interface AppLayoutProps {
  title: string;
  subtitle?: string;
  active?: NavKey;
  children: ReactNode;
}

const NAV_ITEMS: NavItem[] = [
  { key: "dashboard", label: "Dashboard", href: "/", icon: LayoutDashboard },
  { key: "revenue", label: "Revenue", href: "/revenue", icon: Wallet },
  { key: "sales", label: "Sales", href: "/sales", icon: TrendingUp },
  { key: "customers", label: "Customers", href: "/customers", icon: Users },
  { key: "forecast", label: "Forecast", href: "/forecast", icon: LineChart },
  { key: "reports", label: "Reports", href: "/reports", icon: FileText },
  { key: "settings", label: "Settings", href: "/settings", icon: Settings },
];

export function AppLayout({ title, subtitle, active, children }: AppLayoutProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();
  const { status } = useApiStatus();

  const [chatOpen, setChatOpen] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  const resolvedActive =
    active ??
    (NAV_ITEMS.find((item) => item.href === pathname)?.key ?? "dashboard");

  const handleLogout = () => {
    logout();
    router.replace("/login");
  };

  return (
    <div className="min-h-screen">
      <div className="mx-auto flex min-h-screen max-w-[1800px] gap-5 p-4 lg:p-6">
        {/* Sidebar */}
        <aside
          className={cn(
            "shrink-0 lg:flex",
            mobileNavOpen ? "flex" : "hidden",
          )}
        >
          <Card className="fixed bottom-4 left-4 top-4 z-40 flex w-64 flex-col justify-between overflow-hidden bg-white/6 p-5 lg:sticky lg:top-4 lg:h-[calc(100vh-2rem)]">
            <div>
              <div className="flex items-center gap-3 rounded-3xl border border-white/10 bg-white/5 p-4">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-100">
                  <BarChart3 className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm font-medium text-zinc-400">Axlero Solutions</p>
                  <p className="text-lg font-semibold text-white">MetricMind</p>
                </div>
              </div>

              <nav className="mt-6 space-y-2">
                {NAV_ITEMS.map((item) => {
                  const Icon = item.icon;
                  const isActive = resolvedActive === item.key;

                  return (
                    <Link
                      key={item.key}
                      href={item.href}
                      onClick={() => setMobileNavOpen(false)}
                      className={cn(
                        "flex w-full items-center gap-3 rounded-2xl border px-4 py-3 text-sm font-medium transition",
                        isActive
                          ? "border-cyan-400/25 bg-cyan-400/10 text-white"
                          : "border-white/5 bg-white/0 text-zinc-400 hover:border-white/10 hover:bg-white/5 hover:text-white",
                      )}
                    >
                      <Icon className="h-4 w-4" />
                      {item.label}
                    </Link>
                  );
                })}
              </nav>
            </div>

            <div className="mt-6 space-y-4">
              <Card className="border-cyan-400/20 bg-cyan-400/10">
                <CardContent className="p-4">
                  <Badge className="mb-3">Quarterly Spotlight</Badge>
                  <p className="text-sm leading-6 text-cyan-50/90">
                    Revenue growth is tracking ahead of target with pipeline expansion in
                    enterprise accounts.
                  </p>
                </CardContent>
              </Card>

              <div className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/[-4px] px-4 py-3">
                <div>
                  <p className="text-xs uppercase tracking-wide text-zinc-500">Backend</p>
                  <p className="text-sm font-medium text-white">{user?.name ?? "Guest"}</p>
                </div>
                <StatusBadge status={status.backend} />
              </div>
            </div>
          </Card>
        </aside>

        {/* Main */}
        <main className="flex min-w-0 flex-1 flex-col gap-5">
          {/* Header */}
          <Card className="sticky top-4 z-30 bg-white/6 px-4 py-4 lg:px-5">
            <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
              <div className="flex items-center gap-3">
                <Button
                  variant="ghost"
                  className="px-3 lg:hidden"
                  onClick={() => setMobileNavOpen((value) => !value)}
                >
                  <Menu className="h-4 w-4" />
                </Button>
                <div>
                  <p className="text-sm text-zinc-400">Enterprise Command Center</p>
                  <h1 className="text-2xl font-semibold tracking-tight text-white md:text-3xl">
                    {title}
                  </h1>
                  {subtitle && <p className="mt-1 text-sm text-zinc-400">{subtitle}</p>}
                </div>
              </div>

              <div className="flex flex-col gap-3 md:flex-row md:items-center">
                <div className="relative w-full md:w-[280px]">
                  <Input className="pl-4" placeholder="Quick search…" />
                </div>

                <div className="flex items-center gap-3">
                  <Button variant="ghost" className="px-3">
                    <Bell className="h-4 w-4" />
                  </Button>
                  <ThemeToggle />
                  <Button
                    variant="ghost"
                    className="px-3 lg:hidden"
                    onClick={() => setMobileNavOpen(false)}
                  />
                  <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-3 py-2">
                    <Avatar>{user?.initials ?? "U"}</Avatar>
                    <div className="hidden min-[420px]:block">
                      <p className="text-sm font-medium text-white">{user?.name ?? "User"}</p>
                      <p className="text-xs text-zinc-500">{user?.role ?? "Analyst"}</p>
                    </div>
                  </div>
                  <Button variant="ghost" className="px-2" onClick={handleLogout} aria-label="Sign out">
                    <LogOut className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </Card>

          {children}
        </main>
      </div>

      {/* Chat FAB */}
      <Button
        type="button"
        onClick={() => setChatOpen((value) => !value)}
        className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full p-0 shadow-lg shadow-cyan-500/20"
        aria-label={chatOpen ? "Close AI assistant" : "Open AI assistant"}
      >
        <MessageSquareText className="h-6 w-6" />
      </Button>

      <ChatPanel open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}

