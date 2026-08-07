/**
 * query.ts
 *
 * Types mirroring the MetricMind backend `QueryResponse` model
 * (see backend `api_models.py`).
 */

export interface QueryPlanField {
  metrics: string[];
  metric: string | null;
  dimensions: string[];
  filters: Array<Record<string, unknown>>;
  group_by: string[];
  order_by: string | null;
  order: string;
  limit: number | null;
  raw_query: string;
  rewritten_query: string;
  notes: string[];
}

export interface QueryResponse {
  status: "ok" | "error";
  question: string;
  rewritten_question: string | null;
  sql: string | null;
  answer: string | null;
  insights: string[];
  chart: string | null;
  explanation: string | null;
  llm: {
    provider: string;
    model: string | null;
    text: string;
  } | null;
  data: {
    columns: string[];
    rows: Array<unknown[]>;
    sql: string;
    status: string;
    error?: string;
  } | null;
  plan: QueryPlanField | null;
  error: string | null;
}

