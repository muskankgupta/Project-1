export interface KpiMetric {
  id: string;
  label: string;
  value: number;
  format: "currency" | "number" | "decimal" | "percent";
  delta: number;
  trend: "up" | "down" | "flat";
}

export interface ImpactStatusMetric {
  id: string;
  label: string;
  orders: number;
  revenue: number;
  orderShare: number;
  revenueShare: number;
  color: string;
}

export interface ImpactComparisonPoint {
  label: string;
  orders: number;
  revenue: number;
}

export interface ImpactAnalysisTotals {
  orders: number;
  revenue: number;
}

export interface ImpactAnalysisData {
  statuses: ImpactStatusMetric[];
  comparison: ImpactComparisonPoint[];
  totals?: ImpactAnalysisTotals;
}

export interface RevenueOrderTrendPoint {
  period: string;
  revenue: number;
  orders: number;
}

export interface RankingItem {
  id: string;
  name: string;
  category: string;
  value: number;
  change: number;
  share: number;
}

export interface TopStatePoint {
  id: string;
  state: string;
  sales: number;
  orders: number;
  share: number;
}

export interface AovTrendPoint {
  period: string;
  aov: number;
}

export interface DashboardInsightMeta {
  insights: string[];
  explanation: string | null;
  sql: string | string[] | null;
  source: "api" | "mock";
  generatedAt: string;
}

export interface DashboardData {
  kpis: KpiMetric[];
  impactAnalysis: ImpactAnalysisData;
  revenueOrderTrend: RevenueOrderTrendPoint[];
  topPerformers: RankingItem[];
  worstPerformers: RankingItem[];
  topStates: TopStatePoint[];
  aovTrend: AovTrendPoint[];
  meta?: DashboardInsightMeta;
}
