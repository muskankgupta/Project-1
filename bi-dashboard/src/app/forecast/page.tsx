"use client";

import { RouteGuard } from "@/components/route-guard";
import { AppLayout } from "@/components/app-layout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ForecastPage() {
  return (
    <RouteGuard>
      <AppLayout
        title="Forecast"
        subtitle="Trend projection and future outlook"
        active="forecast"
      >
        <Card className="bg-white/6">
          <CardHeader>
            <CardTitle>Outlook</CardTitle>
            <CardDescription>
              The dataset covers 2022-03-31 to 2022-06-29; projections are illustrative.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-6 text-zinc-400">
              Current momentum across the revenue and order trends suggests continued growth,
              with average order value holding steady. Extrapolation beyond the dataset window is
              not supported by the available data.
            </p>
          </CardContent>
        </Card>
      </AppLayout>
    </RouteGuard>
  );
}

