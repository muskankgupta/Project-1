"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { formatCompactCurrency, formatNumber } from "@/lib/dashboard-format";

interface ChatChartProps {
  chart: string | null;
  columns: string[];
  rows: Array<unknown[]>;
}

const PALETTE = [
  "#22d3ee",
  "#f97316",
  "#a78bfa",
  "#34d399",
  "#f472b6",
  "#60a5fa",
  "#facc15",
  "#fb7185",
];

function isCurrencyColumn(column: string): boolean {
  const lower = column.toLowerCase();
  return /revenue|amount|sales|value|aov|gross|price|total/.test(lower);
}

function formatValue(column: string, raw: unknown): string {
  const value = Number(raw ?? 0);

  if (isCurrencyColumn(column)) {
    return formatCompactCurrency(value);
  }

  return formatNumber(value);
}

function TooltipStyles() {
  return {
    background: "rgba(5, 8, 22, 0.92)",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: 16,
    color: "#fff",
    fontSize: 12,
  } as const;
}

function toRows(columns: string[], rows: Array<unknown[]>): Array<Record<string, unknown>> {
  return rows.map((row) => {
    const record: Record<string, unknown> = {};
    columns.forEach((column, index) => {
      record[column] = row[index];
    });
    return record;
  });
}

function KpiCard({ columns, rows }: { columns: string[]; rows: Array<unknown[]> }) {
  const value = rows[0]?.[0];
  const column = columns[0] ?? "value";

  return (
    <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/10 px-4 py-6 text-center">
      <p className="text-[11px] uppercase tracking-[0.2em] text-cyan-200/80">{column}</p>
      <p className="mt-2 text-2xl font-semibold text-white">{formatValue(column, value)}</p>
    </div>
  );
}

function LineChartView({ columns, rows }: { columns: string[]; rows: Array<unknown[]> }) {
  const data = toRows(columns, rows);
  const dimensionKey = columns[0];
  const metricKey = columns[1] ?? columns[columns.length - 1];

  return (
    <div className="h-56 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 8, right: 12, left: 4, bottom: 4 }}>
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
          <XAxis
            dataKey={dimensionKey}
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value) => formatCompactCurrency(Number(value ?? 0))}
          />
          <Tooltip
            contentStyle={TooltipStyles()}
            formatter={(value, name) => [
              formatValue(String(name ?? ""), value),
              String(name ?? ""),
            ]}
          />
          <Line
            type="monotone"
            dataKey={metricKey}
            stroke="#22d3ee"
            strokeWidth={3}
            dot={{ r: 4, fill: "#22d3ee", strokeWidth: 0 }}
            activeDot={{ r: 6 }}
            isAnimationActive
            animationDuration={700}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function BarChartView({ columns, rows }: { columns: string[]; rows: Array<unknown[]> }) {
  const data = toRows(columns, rows);
  const dimensionKey = columns[0];
  const metricKey = columns[1] ?? columns[columns.length - 1];

  return (
    <div className="h-56 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 8, right: 12, left: 4, bottom: 4 }}
        >
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
          <XAxis
            type="number"
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value) => formatCompactCurrency(Number(value ?? 0))}
          />
          <YAxis
            type="category"
            dataKey={dimensionKey}
            width={110}
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            contentStyle={TooltipStyles()}
            formatter={(value, name) => [
              formatValue(String(name ?? ""), value),
              String(name ?? ""),
            ]}
          />
          <Bar dataKey={metricKey} radius={[0, 12, 12, 0]} isAnimationActive animationDuration={700}>
            {data.map((_, index) => (
              <Cell key={index} fill={PALETTE[index % PALETTE.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function PieChartView({ columns, rows }: { columns: string[]; rows: Array<unknown[]> }) {
  const data = toRows(columns, rows);
  const nameKey = columns[0];
  const valueKey = columns[1] ?? columns[columns.length - 1];

  return (
    <div className="h-56 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            dataKey={valueKey}
            nameKey={nameKey}
            innerRadius={45}
            outerRadius={80}
            paddingAngle={3}
            isAnimationActive
            animationDuration={700}
          >
            {data.map((_, index) => (
              <Cell key={index} fill={PALETTE[index % PALETTE.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={TooltipStyles()}
            formatter={(value, name) => [
              formatValue(String(name ?? ""), value),
              String(name ?? ""),
            ]}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

function TableView({ columns, rows }: { columns: string[]; rows: Array<unknown[]> }) {
  return (
    <div className="max-h-56 overflow-auto rounded-2xl border border-white/10">
      <table className="w-full text-left text-xs text-zinc-300">
        <thead className="sticky top-0 bg-[#0a0f1e]">
          <tr>
            {columns.map((column) => (
              <th key={column} className="px-3 py-2 font-medium text-zinc-400">
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex} className="border-t border-white/5">
              {row.map((cell, cellIndex) => {
                const column = columns[cellIndex];
                return (
                  <td key={cellIndex} className="px-3 py-2">
                    {formatValue(column, cell)}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function ChatChart({ chart, columns, rows }: ChatChartProps) {
  if (!chart || chart === "No chart recommended." || columns.length === 0 || rows.length === 0) {
    return null;
  }

  const normalized = chart.toLowerCase();

  if (normalized.includes("kpi")) {
    return <KpiCard columns={columns} rows={rows} />;
  }

  if (normalized.includes("line")) {
    return <LineChartView columns={columns} rows={rows} />;
  }

  if (normalized.includes("bar") || normalized.includes("column")) {
    return <BarChartView columns={columns} rows={rows} />;
  }

  if (normalized.includes("pie") || normalized.includes("donut")) {
    return <PieChartView columns={columns} rows={rows} />;
  }

  return <TableView columns={columns} rows={rows} />;
}
