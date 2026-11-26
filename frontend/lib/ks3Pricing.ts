"use client";
import { useEffect, useState } from "react";
import { paymentsAPI } from "@/lib/api";
import type { Account } from "@/lib/country";

// Notenix KS3 is priced by year group (backend services/pricing.py, KS3_PRICES / KS3_LIST_PRICES).
// prices[currency] = [first, second, third year]: UK Years 7/8/9, or Grades 5/6/7 on the US / Ontario tracks.
// While the offer runs, each price carries `was_label` (the usual price, shown struck through).

export type Ks3Price = { currency: string; amount: number; label: string; was?: number; was_label?: string };
export type Ks3Track = "us" | "on";
export type Ks3Info = {
  accounts: Account[];
  prices: Record<string, Ks3Price[]>;
  gbp: Ks3Price[];
  offer?: boolean;
  offer_until?: string | null;
  pay_link?: string;
};

/** The year-group names for a track, in price order. */
export function ks3Years(track?: Ks3Track | null): { year: number; label: string }[] {
  return track
    ? [5, 6, 7].map((g) => ({ year: g, label: `Grade ${g}` }))
    : [7, 8, 9].map((y) => ({ year: y, label: `Year ${y}` }));
}

/** 0/1/2 for a year (7-9) or track grade (5-7). Year 6 children work on Year 7, so they pay Year 7. */
export function ks3Tier(year: number | null | undefined, track?: Ks3Track | null): number {
  const first = track ? 5 : 7;
  return year ? Math.min(2, Math.max(0, year - first)) : 0;
}

// Used only if the API can't be reached: the usual (list) prices, no offer.
const gbp = (a: number): Ks3Price => ({ currency: "GBP", amount: a, label: `£${a}` });
export const KS3_FALLBACK: Ks3Info = { accounts: [], prices: { GBP: [gbp(169), gbp(189), gbp(209)] }, gbp: [gbp(169), gbp(189), gbp(209)] };

let infoPromise: Promise<Ks3Info> | null = null;
export function loadKs3Info(): Promise<Ks3Info> {
  infoPromise ??= paymentsAPI.ks3Info().then((r) => r.data as Ks3Info).catch(() => KS3_FALLBACK);
  return infoPromise;
}

export function useKs3Info(): Ks3Info | null {
  const [info, setInfo] = useState<Ks3Info | null>(null);
  useEffect(() => { loadKs3Info().then(setInfo); }, []);
  return info;
}

/** "Offer ends in 5h 12m", ticking each minute; null when there's no running offer. */
export function useOfferCountdown(until?: string | null): string | null {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (!until) return;
    const t = setInterval(() => setNow(Date.now()), 30_000);
    return () => clearInterval(t);
  }, [until]);
  if (!until) return null;
  const left = new Date(until).getTime() - now;
  if (!(left > 0)) return null;
  const h = Math.floor(left / 3_600_000);
  const m = Math.floor((left % 3_600_000) / 60_000);
  return `Offer ends in ${h > 0 ? `${h}h ` : ""}${m}m`;
}
