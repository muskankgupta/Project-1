import { AlertCircle } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";

interface SectionStateProps {
  title: string;
  description: string;
}

export function SectionLoadingState({ title, description }: SectionStateProps) {
  return (
    <Card className="bg-white/6">
      <CardContent className="space-y-4 p-6">
        <div>
          <div className="h-4 w-36 rounded-full bg-white/10" />
          <div className="mt-3 h-3 w-56 rounded-full bg-white/5" />
        </div>
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <div className="h-28 rounded-3xl bg-white/5" />
          <div className="h-28 rounded-3xl bg-white/5" />
          <div className="h-28 rounded-3xl bg-white/5" />
          <div className="h-28 rounded-3xl bg-white/5" />
        </div>
        <p className="sr-only">
          {title} loading state: {description}
        </p>
      </CardContent>
    </Card>
  );
}

export function SectionEmptyState({ title, description }: SectionStateProps) {
  return (
    <Card className="bg-white/6">
      <CardContent className="flex min-h-[220px] items-center justify-center p-6 text-center">
        <div className="max-w-sm">
          <AlertCircle className="mx-auto h-6 w-6 text-zinc-400" />
          <p className="mt-4 text-base font-semibold text-white">{title}</p>
          <p className="mt-2 text-sm leading-6 text-zinc-400">{description}</p>
        </div>
      </CardContent>
    </Card>
  );
}