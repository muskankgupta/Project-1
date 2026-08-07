/**
 * export.ts
 *
 * Client-side export utilities for the MetricMind dashboard.
 *  - exportCsv: RFC-4180 compliant CSV download.
 *  - exportPdf: professional multi-section PDF report (KPIs, trends,
 *    rankings, top states, impact) built with jsPDF.
 */

import { jsPDF } from "jspdf";

import type { DashboardData } from "@/types/dashboard";
import { formatCompactCurrency, formatNumber, formatPercent } from "@/lib/dashboard-format";
import { formatIndianAmount } from "@/lib/format-indian";

function escapeCell(value: string): string {
  return `"${String(value).replaceAll('"', '""')}"`;
}

type CsvRow = string[];

/** Serialize the full dashboard into rows for CSV export. */
function buildCsvRows(data: DashboardData): CsvRow[] {
  const rows: CsvRow[] = [["Section", "Label", "Period/Group", "Value", "Share"]];

  for (const kpi of data.kpis ?? []) {
    rows.push(["KPI", kpi.label, "overall", formatCompactCurrency(kpi.value), ""]);
  }

  for (const point of data.revenueOrderTrend ?? []) {
    rows.push(["Trend", "Revenue", point.period, formatCompactCurrency(point.revenue), ""]);
    rows.push(["Trend", "Orders", point.period, formatNumber(point.orders), ""]);
  }

  for (const state of data.topStates ?? []) {
    rows.push([
      "Top States",
      state.state,
      "overall",
      formatCompactCurrency(state.sales),
      formatPercent(state.share),
    ]);
  }

  for (const item of data.topPerformers ?? []) {
    rows.push([
      "Top Performers",
      item.name,
      item.category,
      formatCompactCurrency(item.value),
      `${formatNumber(item.share)}%`,
    ]);
  }

  for (const item of data.worstPerformers ?? []) {
    rows.push([
      "Worst Performers",
      item.name,
      item.category,
      formatCompactCurrency(item.value),
      `${formatNumber(item.share)}%`,
    ]);
  }

  for (const point of data.aovTrend ?? []) {
    rows.push(["AOV Trend", "Average Order Value", point.period, formatCompactCurrency(point.aov), ""]);
  }

  for (const status of data.impactAnalysis?.statuses ?? []) {
    rows.push([
      "Impact",
      status.label,
      "overall",
      `${formatNumber(status.orders)} orders / ${formatCompactCurrency(status.revenue)}`,
      `${formatPercent(status.revenueShare)}`,
    ]);
  }

  return rows;
}

/** Trigger a CSV file download. */
export function exportDashboardCsv(data: DashboardData): void {
  const rows = buildCsvRows(data);
  const csv = rows.map((row) => row.map(escapeCell).join(",")).join("\n");

  const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `MetricMind-Report-${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/* ----------------------------------------------------------------
 * PDF report generation
 * ---------------------------------------------------------------- */

const PAGE_WIDTH = 210; // A4 mm
const MARGIN = 14;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2;

const DARK_BG: [number, number, number] = [5, 8, 22];
const ACCENT: [number, number, number] = [34, 211, 238];
const MUTED: [number, number, number] = [100, 116, 139];
const ROW_HEADER: [number, number, number] = [22, 27, 49];

interface PdfDoc {
  doc: jsPDF;
  y: number;
}

function ensureSpace(page: PdfDoc, needed = 18): void {
  const pageHeight = 297;
  if (page.y + needed > pageHeight - MARGIN) {
    page.doc.addPage();
    page.y = MARGIN;
  }
}

function header(page: PdfDoc, text: string): void {
  ensureSpace(page, 22);
  page.doc.setFillColor(...ACCENT);
  page.doc.rect(MARGIN, page.y, 2.2, 6, "F");
  page.doc.setTextColor(255, 255, 255);
  page.doc.setFont("helvetica", "bold");
  page.doc.setFontSize(13);
  page.doc.text(text, MARGIN + 4, page.y + 5);
  page.y += 10;
}

function kvRow(page: PdfDoc, label: string, value: string): void {
  ensureSpace(page, 8);
  page.doc.setFont("helvetica", "normal");
  page.doc.setFontSize(10);
  page.doc.setTextColor(...MUTED);
  page.doc.text(label, MARGIN, page.y);
  page.doc.setTextColor(240, 240, 240);
  page.doc.text(value, MARGIN + 60, page.y);
  page.y += 7;
}

function tableRows(
  page: PdfDoc,
  headers: string[],
  rows: string[][],
  widths: number[],
): void {
  ensureSpace(page, 24);

  page.doc.setFillColor(...ROW_HEADER);
  page.doc.rect(MARGIN, page.y, CONTENT_WIDTH, 8, "F");
  page.doc.setFont("helvetica", "bold");
  page.doc.setFontSize(9);
  page.doc.setTextColor(255, 255, 255);

  let x = MARGIN;
  headers.forEach((headerText, index) => {
    page.doc.text(headerText, x + 2, page.y + 5.5);
    x += widths[index];
  });
  page.y += 9;

  page.doc.setFont("helvetica", "normal");
  page.doc.setTextColor(220, 220, 230);

  rows.forEach((row) => {
    ensureSpace(page, 8);
    page.doc.setFontSize(8.5);

    let currentX = MARGIN;
    row.forEach((cell, index) => {
      const text = String(cell ?? "");
      const segmentWidth = widths[index];
      page.doc.text(text, currentX + 2, page.y + 4, { maxWidth: segmentWidth - 4 });
      currentX += segmentWidth;
    });
    page.y += 7;
  });
}

/** Build and download a professional PDF report of the dashboard. */
export function exportDashboardPdf(data: DashboardData): void {
  const doc = new jsPDF({ unit: "mm", format: "a4" });
  const page: PdfDoc = { doc, y: MARGIN };

  // --- Cover / header band ---
  doc.setFillColor(...DARK_BG);
  doc.rect(0, 0, PAGE_WIDTH, 34, "F");
  doc.setFillColor(...ACCENT);
  doc.rect(MARGIN, 20, 3, 8, "F");
  doc.setTextColor(255, 255, 255);
  doc.setFont("helvetica", "bold");
  doc.setFontSize(20);
  doc.text("MetricMind BI Report", MARGIN + 6, 26);
  doc.setFontSize(11);
  doc.setFont("helvetica", "normal");
  doc.setTextColor(160, 200, 235);
  doc.text("Amazon.in Sales — Executive Summary", MARGIN + 6, 32);
  page.y = 42;

  kvRow(page, "Generated", new Date().toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }));
  kvRow(page, "Data source", data.meta?.source === "api" ? "Live MetricMind backend" : "Bundled sample data");

  // --- KPIs ---
  header(page, "Key Performance Indicators");
  for (const kpi of data.kpis ?? []) {
    kvRow(page, kpi.label, formatCompactCurrency(kpi.value));
  }

  // --- Revenue / Order trend ---
  const trendRows = (data.revenueOrderTrend ?? []).map((point) => [
    point.period,
    formatCompactCurrency(point.revenue),
    formatNumber(point.orders),
    formatIndianAmount(point.revenue).text,
  ]);
  if (trendRows.length > 0) {
    header(page, "Revenue vs Order Trend");
    tableRows(page, ["Period", "Revenue", "Orders", "Executive"], trendRows, [40, 45, 40, 55]);
  }

  // --- Top states ---
  const stateRows = (data.topStates ?? []).map((state) => [
    state.state,
    formatCompactCurrency(state.sales),
    formatNumber(state.orders),
    formatPercent(state.share),
  ]);
  if (stateRows.length > 0) {
    header(page, "Top States");
    tableRows(page, ["State", "Sales", "Orders", "Share"], stateRows, [60, 45, 40, 35]);
  }

  // --- Rankings (best performers) ---
  const rankRows = (data.topPerformers ?? []).map((item) => [
    item.name,
    item.category,
    formatCompactCurrency(item.value),
    `${formatNumber(item.share)}%`,
  ]);
  if (rankRows.length > 0) {
    header(page, "Top Performing Categories");
    tableRows(page, ["Product/Category", "Type", "Value", "Share"], rankRows, [55, 45, 45, 35]);
  }

  const worstRows = (data.worstPerformers ?? []).map((item) => [
    item.name,
    item.category,
    formatCompactCurrency(item.value),
    `${formatNumber(item.share)}%`,
  ]);
  if (worstRows.length > 0) {
    header(page, "Underperforming Categories");
    tableRows(page, ["Product/Category", "Type", "Value", "Share"], worstRows, [55, 45, 45, 35]);
  }

  // --- Impact analysis ---
  const impactRows = (data.impactAnalysis?.statuses ?? []).map((status) => [
    status.label,
    formatNumber(status.orders),
    formatCompactCurrency(status.revenue),
    formatPercent(status.revenueShare),
  ]);
  if (impactRows.length > 0) {
    header(page, "Order Status Impact");
    tableRows(page, ["Status", "Orders", "Revenue", "Revenue Share"], impactRows, [60, 35, 45, 40]);
  }

  // --- Footer ---
  doc.setFontSize(8);
  doc.setTextColor(...MUTED);
  doc.text("MetricMind — Agentic NL → SQL Business Intelligence", MARGIN, 290);

  doc.save(`MetricMind-Report-${new Date().toISOString().slice(0, 10)}.pdf`);
}

