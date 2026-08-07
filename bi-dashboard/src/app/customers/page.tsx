"use client";

import { RouteGuard } from "@/components/route-guard";
import { AppLayout } from "@/components/app-layout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function CustomersPage() {
  return (
    <RouteGuard>
      <AppLayout
        title="Customers"
        subtitle="B2B share and order geography"
        active="customers"
      >
        <div className="grid gap-5 md:grid-cols-2">
          <Card className="bg-white/6">
            <CardHeader>
              <CardTitle>Geographic Distribution</CardTitle>
              <CardDescription>
                Shipping footprint across Indian states derived from the Amazon sales dataset.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-6 text-zinc-400">
                Most orders ship to Maharashtra, Karnataka, and Telangana. Use the Dashboard view
                for the full top-states breakdown.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white/6">
            <CardHeader>
              <CardTitle>B2B vs Consumer</CardTitle>
              <CardDescription>Business-to-business orders are rare in this dataset.</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-6 text-zinc-400">
                Only ~0.7% of rows are flagged B2B. Wholesale behaviour is minimal, so the market is
                almost entirely consumer (B2C) driven.
              </p>
            </CardContent>
          </Card>
        </div>
      </AppLayout>
    </RouteGuard>
  );
}

