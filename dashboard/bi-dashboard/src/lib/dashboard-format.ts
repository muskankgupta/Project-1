/**
 * dashboard-format.ts
 *
 * Number/currency formatting helpers.
 *
 * The MetricMind platform analyzes Amazon.in sales data (INR), so currency
 * helpers default to Indian Rupees with the `en-IN` locale.
 */

const INR_LOCALE = "en-IN";
const INR_CURRENCY = "INR";

export function formatCurrency(value: number) {
  return new Intl.NumberFormat(INR_LOCALE, {
    style: "currency",
    currency: INR_CURRENCY,
    notation: value >= 1000000 ? "compact" : "standard",
    maximumFractionDigits: value >= 1000000 ? 2 : 0,
  }).format(value);
}

export function formatCompactCurrency(value: number) {
  return new Intl.NumberFormat(INR_LOCALE, {
    style: "currency",
    currency: INR_CURRENCY,
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

export function formatNumber(value: number) {
  return new Intl.NumberFormat(INR_LOCALE, {
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatPercent(value: number) {
  return `${new Intl.NumberFormat(INR_LOCALE, {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(value)}%`;
}

export function formatSignedPercent(value: number) {
  const prefix = value > 0 ? "+" : "";
  return `${prefix}${formatPercent(value)}`;
}

