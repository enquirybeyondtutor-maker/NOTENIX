// Type-in (numeric) answers: accept "0.5", ".5", "1/2", "50%"-free forms the same way the
// backend grader does (services/grading.py::_numeric_equal).
function parseNumber(raw: string): number | null {
  const s = raw.trim().replace(/[,\s£$€]/g, "").replace(/\$/g, "");
  if (!s) return null;
  const frac = s.match(/^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/);
  if (frac) {
    const d = parseFloat(frac[2]);
    return d === 0 ? null : parseFloat(frac[1]) / d;
  }
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

export function numericEqual(given: string, expected: string): boolean {
  const a = parseNumber(given);
  const b = parseNumber(expected);
  if (a === null || b === null) return given.trim().toLowerCase() === expected.trim().toLowerCase();
  return Math.abs(a - b) <= 1e-6 * Math.max(1, Math.abs(b)) || Math.abs(a - b) < 5e-4;
}
