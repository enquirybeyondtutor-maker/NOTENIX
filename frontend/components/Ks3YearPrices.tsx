"use client";
import { Clock } from "lucide-react";
import { useCountry, pickAccounts } from "@/lib/country";
import { useKs3Info, useOfferCountdown, ks3Years, KS3_FALLBACK, type Ks3Track } from "@/lib/ks3Pricing";

// The yearly price for each year group on the KS3 / Middle School / Ontario landing pages,
// with the usual price struck through and a countdown while the offer runs.
// UK KS3 shows the visitor's local currency when we have an account for their country, else GBP.
export default function Ks3YearPrices({ track }: { track?: Ks3Track }) {
  const info = useKs3Info() ?? KS3_FALLBACK;
  const country = useCountry();
  const countdown = useOfferCountdown(info.offer ? info.offer_until : null);
  let cur = track === "us" ? "USD" : track === "on" ? "CAD" : "GBP";
  if (!track) {
    const { shown, local } = pickAccounts(info.accounts, country);
    const c = shown[0]?.currency?.toUpperCase();
    if (local && c && info.prices[c]) cur = c;
  }
  const row = info.prices[cur] || info.gbp;
  const offerOn = !!countdown || (info.offer && !info.offer_until);

  return (
    <div className="mt-3">
      {offerOn && (
        <p className="mb-3 inline-flex items-center gap-1.5 rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-800">
          <Clock size={13} /> Launch offer{countdown ? `: ${countdown.replace("Offer ends", "ends")}` : ""}
        </p>
      )}
      <ul className="divide-y divide-line rounded-lg border border-line">
        {ks3Years(track).map((y, i) => {
          const p = row[i] || row[0];
          return (
            <li key={y.year} className="flex items-baseline justify-between gap-3 px-4 py-2.5">
              <span className="text-sm font-medium text-ink">{y.label}</span>
              <span className="flex items-baseline gap-2">
                {offerOn && p.was_label && <s className="text-sm text-ink-subtle">{p.was_label}</s>}
                <span className="text-2xl font-bold text-ink">{p.label}</span>
                <span className="text-xs text-ink-subtle">/ year</span>
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
