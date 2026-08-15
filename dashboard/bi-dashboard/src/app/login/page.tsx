"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { BarChart3, KeyRound, Loader2, Lock, Mail } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ThemeToggle } from "@/components/theme-toggle";
import { useAuth, getRememberedEmail } from "@/providers/auth-provider";

const DEMO_EMAIL = "demo@axlero.com";
const DEMO_PASSWORD = "demo1234";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState(() =>
    typeof window === "undefined" ? "" : (getRememberedEmail() ?? DEMO_EMAIL),
  );
  const [password, setPassword] = useState(DEMO_PASSWORD);
  const [remember, setRemember] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await login(email, password, remember);
      router.replace("/");
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Unable to sign in.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-10">
      {/* ambient glows */}
      <div className="pointer-events-none absolute -left-32 -top-32 h-96 w-96 rounded-full bg-cyan-500/15 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-32 -right-32 h-96 w-96 rounded-full bg-blue-600/15 blur-3xl" />

      <div className="absolute right-6 top-6">
        <ThemeToggle />
      </div>

      <div className="w-full max-w-md">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-200">
            <BarChart3 className="h-7 w-7" />
          </div>
          <h1 className="mt-5 text-2xl font-semibold tracking-tight text-white md:text-3xl">
            MetricMind
          </h1>
          <p className="mt-2 text-sm text-zinc-400">
            Sign in to your business intelligence console
          </p>
        </div>

        <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
          <CardContent className="p-6 md:p-8">
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium text-zinc-300">
                  Email
                </label>
                <div className="relative">
                  <Mail className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-500" />
                  <Input
                    id="email"
                    type="email"
                    autoComplete="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    className="pl-10"
                    placeholder="you@company.com"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium text-zinc-300">
                  Password
                </label>
                <div className="relative">
                  <Lock className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-500" />
                  <Input
                    id="password"
                    type="password"
                    autoComplete="current-password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    className="pl-10"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </div>

              <label className="flex items-center gap-2 text-sm text-zinc-400">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(event) => setRemember(event.target.checked)}
                  className="h-4 w-4 rounded border-white/20 bg-white/5 accent-cyan-500"
                />
                Remember me
              </label>

              {error && (
                <div className="rounded-2xl border border-rose-400/20 bg-rose-400/10 px-4 py-3 text-sm text-rose-200">
                  {error}
                </div>
              )}

              <Button
                type="submit"
                className="w-full py-3"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <KeyRound className="h-4 w-4" />
                )}
                {isSubmitting ? "Signing in…" : "Sign in"}
              </Button>
            </form>

            <div className="mt-6 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-center">
              <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">
                Demo credentials
              </p>
              <p className="mt-1 text-sm text-zinc-300">
                {DEMO_EMAIL} · {DEMO_PASSWORD}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

