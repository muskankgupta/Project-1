"use client";

import { AppLayout } from "@/components/app-layout";
import { RouteGuard } from "@/components/route-guard";
import { DashboardSection } from "@/components/dashboard-section";

export default function Home() {
  return (
    <RouteGuard>
      <AppLayout
        title="BI Dashboard Overview"
        subtitle="Enterprise Command Center"
        active="dashboard"
      >
        <DashboardSection />
      </AppLayout>
    </RouteGuard>
  );
}

