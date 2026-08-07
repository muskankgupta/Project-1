import * as React from "react";

import { cn } from "@/lib/utils";

export function Input({ className, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "h-11 w-full rounded-2xl border border-white/10 bg-white/5 px-4 text-sm text-white placeholder:text-zinc-500 shadow-sm outline-none transition focus:border-cyan-400/40 focus:ring-2 focus:ring-cyan-400/20",
        className,
      )}
      {...props}
    />
  );
}