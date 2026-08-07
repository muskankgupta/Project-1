"use client";

import { RouteGuard } from "@/components/route-guard";
import { AppLayout } from "@/components/app-layout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ReportsPage() {
  return (
    <RouteGuard>
      <AppLayout title="Reports" subtitle="Scheduled and on-demand reporting" active="reports">
        <Card className="bg-white/6">
          <CardHeader>
            <CardTitle>Available Reports</CardTitle>
            <CardDescription>
              Summary of the metrics powering the dashboard.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-6 text-zinc-400">
              KPIs include total revenue, order count, units sold, and average order value —
              alongside trend, ranking, state, and impact analysis breakdowns.
            </p>
          </CardContent>
        </Card>
      </AppLayout>
    </RouteGuard>
  );
}

