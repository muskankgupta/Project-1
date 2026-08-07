"use client";

import { RouteGuard } from "@/components/route-guard";
import { AppLayout } from "@/components/app-layout";
import { DashboardSection } from "@/components/dashboard-section";

export default function SalesPage() {
  return (
    <RouteGuard>
      <AppLayout
        title="Sales Overview"
        subtitle="Top states, categories, and fulfillment performance"
        active="sales"
      >
        <DashboardSection />
      </AppLayout>
    </RouteGuard>
  );
}

