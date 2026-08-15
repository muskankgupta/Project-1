/**
 * format-indian.ts
 *
 * Executive-friendly Indian number formatting.
 * Converts raw INR values into ₹ Lakhs / ₹ Crores phrases used in
 * executive summaries and exported reports.
 */

const NUM_VALUE = {
  thousand: 1_000,
  lakh: 100_000,
  crore: 10_000_000,
} as const;

export interface IndianAmountParts {
  value: number;
  unit: "lakh" | "crore" | null;
  text: string;
}

/**
 * Convert a raw INR amount into a compact Indian representation.
 * Returns a plain object so callers can render in the UI or embed into prose.
 */
export function formatIndianAmount(amount: number): IndianAmountParts {
  const absolute = Math.abs(amount);

  if (absolute >= NUM_VALUE.crore) {
    const value = amount / NUM_VALUE.crore;
    return { value, unit: "crore", text: `₹${value.toFixed(2)} Cr` };
  }

  if (absolute >= NUM_VALUE.lakh) {
    const value = amount / NUM_VALUE.lakh;
    return { value, unit: "lakh", text: `₹${value.toFixed(2)} L` };
  }

  if (absolute >= NUM_VALUE.thousand) {
    const value = amount / NUM_VALUE.thousand;
    return { value, unit: null, text: `₹${value.toFixed(1)}K` };
  }

  return { value: amount, unit: null, text: `₹${amount.toFixed(0)}` };
}

/** Short one-line currency using the Indian numbering system (en-IN). */
export function formatINR(value: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

