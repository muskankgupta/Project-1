"use client";

import { RouteGuard } from "@/components/route-guard";
import { AppLayout } from "@/components/app-layout";
import { DashboardSection } from "@/components/dashboard-section";

export default function RevenuePage() {
  return (
    <RouteGuard>
      <AppLayout
        title="Revenue Analytics"
        subtitle="Revenue, orders, and average order value trends"
        active="revenue"
      >
        <DashboardSection />
      </AppLayout>
    </RouteGuard>
  );
}

