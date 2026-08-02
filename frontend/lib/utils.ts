/**
 * Tiny dependency-free classNames helper.
 * Accepts strings, arrays and conditional objects, like a mini clsx.
 * (v2 intentionally avoids extra deps — see project memory.)
 */
type ClassInput = string | number | null | false | undefined | ClassInput[] | Record<string, boolean>;

export function cn(...inputs: ClassInput[]): string {
  const out: string[] = [];
  const walk = (val: ClassInput) => {
    if (!val) return;
    if (typeof val === "string" || typeof val === "number") {
      out.push(String(val));
    } else if (Array.isArray(val)) {
      val.forEach(walk);
    } else if (typeof val === "object") {
      for (const [k, v] of Object.entries(val)) if (v) out.push(k);
    }
  };
  inputs.forEach(walk);
  return out.join(" ");
}

export function humanize(key: string): string {
  return (key || "").replace(/[_-]+/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function formatDate(iso?: string | null): string {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

export function relativeTime(iso?: string | null): string {
  if (!iso) return "—";
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.round(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.round(hrs / 24);
  if (days < 30) return `${days}d ago`;
  return formatDate(iso);
}
