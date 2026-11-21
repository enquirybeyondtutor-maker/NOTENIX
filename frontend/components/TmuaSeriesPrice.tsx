"use client";
import { useEffect, useState } from "react";
import { SERIES, currentPrice } from "@/lib/tmuaSeries";

// Price shown to the visitor: early bird until Tue 24 Nov (UK), then full price.
// Rendered after mount so a cached page never shows a stale price.
export default function TmuaSeriesPrice({ compact = false }: { compact?: boolean }) {
  const [p, setP] = useState<{ amount: number; early: boolean } | null>(null);
  useEffect(() => setP(currentPrice()), []);
  if (!p) return <span className="inline-block h-6 w-40 animate-pulse rounded bg-brand-100" />;
  if (compact) return <>£{p.amount}</>;
  return p.early ? (
    <span>
      <b className="text-2xl font-bold text-ink">£{SERIES.earlyPrice}</b>{" "}
      <span className="text-ink-muted">if you enrol by {SERIES.earlyLabel}, then <s>£{SERIES.price}</s></span>
    </span>
  ) : (
    <span><b className="text-2xl font-bold text-ink">£{SERIES.price}</b> <span className="text-ink-muted">for the full series</span></span>
  );
}
