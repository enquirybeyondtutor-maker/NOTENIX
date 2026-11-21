"use client";
import { useEffect, useState } from "react";
import { SERIES, currentPrice } from "@/lib/tmuaSeries";

// Price shown to the visitor: early bird until Tue 24 Nov (UK), then full price.
// Rendered after mount so a cached page never shows a stale price.
//   amount: "£99"     line: "£99 if you enrol by Tue 24 Nov, then £109"     card: big price + note
export default function TmuaSeriesPrice({ variant = "line" }: { variant?: "amount" | "line" | "card" }) {
  const [p, setP] = useState<{ amount: number; early: boolean } | null>(null);
  useEffect(() => setP(currentPrice()), []);
  if (!p) return variant === "amount" ? null : <span className="inline-block h-5 w-48 animate-pulse rounded bg-brand-100 align-middle" />;
  if (variant === "amount") return <>£{p.amount}</>;
  if (variant === "card") {
    return (
      <div>
        <p className="flex items-baseline gap-2">
          <span className="text-4xl font-bold tracking-tight text-ink">£{p.amount}</span>
          {p.early && <span className="text-lg text-ink-subtle line-through">£{SERIES.price}</span>}
        </p>
        <p className="mt-1 text-sm text-ink-muted">
          {p.early ? <>Early-bird price until {SERIES.earlyLabel}. One payment for the whole series.</> : <>One payment for the whole series.</>}
        </p>
      </div>
    );
  }
  return p.early
    ? <><b className="font-semibold text-ink">£{p.amount}</b> if you enrol by {SERIES.earlyLabel}, then £{SERIES.price}</>
    : <><b className="font-semibold text-ink">£{p.amount}</b> for the full series</>;
}
