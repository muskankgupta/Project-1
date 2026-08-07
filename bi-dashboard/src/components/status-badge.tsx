"use client";

import { cn } from "@/lib/utils";

import type { ServiceStatus } from "@/hooks/use-api-status";

interface StatusBadgeProps {
  status: ServiceStatus;
  label?: string;
  className?: string;
}

const CONFIG: Record<ServiceStatus, { dot: string; text: string; label: string }> = {
  online: {
    dot: "bg-emerald-400",
    text: "text-emerald-300",
    label: "Online",
  },
  offline: {
    dot: "bg-rose-400",
    text: "text-rose-300",
    label: "Offline",
  },
  checking: {
    dot: "bg-amber-400 animate-pulse",
    text: "text-amber-300",
    label: "Checking",
  },
};

export function StatusBadge({
  status,
  label,
  className,
}: StatusBadgeProps) {
  const config = CONFIG[status];

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-medium",
        config.text,
        className,
      )}
    >
      <span className={cn("h-2 w-2 rounded-full", config.dot)} />
      {label ?? config.label}
    </span>
  );
}

