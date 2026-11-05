"use client";
import { useEffect, useState } from "react";

// Payment accounts come from PAYMENT_ACCOUNTS on the backend. Optional fields:
//   countries: ["AU"]       show this account first to visitors from these countries
//                           ("EU" = every EU/EEA country plus Switzerland)
//   amount:    "A$290"      fixed local price for the £149 plan (else converted at today's rate)
export type Account = {
  label: string;
  currency?: string;
  details: Record<string, string>;
  note?: string;
  pay_link?: string;
  countries?: string[];
  amount?: string;
};

const COUNTRY_NAMES: Record<string, string> = {
  AU: "Australia", SG: "Singapore", GB: "the UK", NZ: "New Zealand", IN: "India",
  AE: "the UAE", US: "the US", IE: "Ireland", MY: "Malaysia", HK: "Hong Kong", CA: "Canada",
  DE: "Germany", FR: "France", NL: "the Netherlands", ES: "Spain", IT: "Italy", BE: "Belgium",
  AT: "Austria", PT: "Portugal", CH: "Switzerland", SE: "Sweden", DK: "Denmark", NO: "Norway",
  PL: "Poland", FI: "Finland", GR: "Greece",
};

const EU = ["AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IE","IT","LV","LT","LU","MT",
  "NL","PL","PT","RO","SK","SI","ES","SE","IS","LI","NO","CH"];
const expand = (codes: string[] = []) => codes.flatMap((c) => (c.toUpperCase() === "EU" ? EU : [c.toUpperCase()]));
export const countryName = (c: string) => COUNTRY_NAMES[c] || c;

// Fallback when the edge header is missing (local dev): guess from the browser time zone.
function countryFromTimeZone(): string {
  let tz = "";
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch {}
  if (tz.startsWith("Australia/")) return "AU";
  if (tz === "Asia/Singapore") return "SG";
  if (tz === "Pacific/Auckland" || tz === "Pacific/Chatham") return "NZ";
  if (tz === "Europe/London") return "GB";
  if (tz === "Asia/Kolkata" || tz === "Asia/Calcutta") return "IN";
  if (tz === "Asia/Dubai") return "AE";
  if (/^America\/(Toronto|Vancouver|Edmonton|Winnipeg|Halifax|Regina|St_Johns|Montreal)/.test(tz)) return "CA";
  if (/^America\/(New_York|Chicago|Denver|Los_Angeles|Phoenix|Anchorage|Detroit)/.test(tz) || tz.startsWith("US/")) return "US";
  if (/^Europe\/(Berlin|Paris|Amsterdam|Madrid|Rome|Brussels|Vienna|Lisbon|Zurich|Stockholm|Copenhagen|Oslo|Warsaw|Helsinki|Athens|Dublin)/.test(tz)) {
    const map: Record<string, string> = { Berlin: "DE", Paris: "FR", Amsterdam: "NL", Madrid: "ES", Rome: "IT", Brussels: "BE", Vienna: "AT",
      Lisbon: "PT", Zurich: "CH", Stockholm: "SE", Copenhagen: "DK", Oslo: "NO", Warsaw: "PL", Helsinki: "FI", Athens: "GR", Dublin: "IE" };
    return map[tz.split("/")[1]] || "";
  }
  return "";
}

/** Visitor's country code ("" until known or if unknown). `?country=AU` overrides, for testing. */
export function useCountry(): string {
  const [country, setCountry] = useState("");
  useEffect(() => {
    const forced = new URLSearchParams(window.location.search).get("country");
    if (forced) return setCountry(forced.toUpperCase());
    fetch("/geo")
      .then((r) => (r.ok ? r.json() : { country: "" }))
      .catch(() => ({ country: "" }))
      .then((d) => setCountry(d.country || countryFromTimeZone()));
  }, []);
  return country;
}

/** Only the accounts for the visitor's country. If we have none for that country,
 *  the GBP accounts instead. `local` says which case it is. */
export function pickAccounts(accounts: Account[], country: string): { shown: Account[]; local: boolean } {
  const local = country ? accounts.filter((a) => expand(a.countries).includes(country)) : [];
  if (local.length) return { shown: local, local: true };
  const gbp = accounts.filter((a) => !a.currency || a.currency.toUpperCase() === "GBP");
  // Prefer the GBP accounts not tied to a country (e.g. the international IBAN one).
  const intl = gbp.filter((a) => !a.countries?.length);
  return { shown: intl.length ? intl : gbp.length ? gbp : accounts, local: false };
}

// ── Local prices ─────────────────────────────────────────────────────────────
// Prices are set in GBP. A visitor from a country where we have a local account sees
// that account's currency (rounded, at today's rate); everyone else sees GBP.

const SYMBOL: Record<string, string> = {
  GBP: "£", AUD: "A$", NZD: "NZ$", SGD: "S$", CAD: "C$", USD: "US$", EUR: "€", AED: "AED ", INR: "₹",
};

/** Round up to a price ending in 9: A$286.60 → A$289, US$200.70 → US$209 (₹ to the next ...99). */
function tidy(amount: number, currency: string): number {
  const step = currency === "INR" ? 100 : 10;
  let v = Math.ceil(amount / step) * step - 1;
  if (v < amount) v += step;
  return v;
}

export function formatMoney(amount: number, currency: string): string {
  return `${SYMBOL[currency] ?? currency + " "}${amount.toLocaleString("en-GB")}`;
}

/** Converts a GBP price to `currency` with today's rate, e.g. 149 → "A$290". */
export function localAmount(gbp: number, currency: string, rates: Record<string, number> | null): string | null {
  if (currency === "GBP") return formatMoney(gbp, "GBP");
  const r = rates?.[currency];
  return r ? formatMoney(tidy(gbp * r, currency), currency) : null;
}

let ratesPromise: Promise<Record<string, number> | null> | null = null;
function loadRates() {
  ratesPromise ??= fetch("/api/payments/fx").then((r) => (r.ok ? r.json() : null)).then((d) => d?.rates ?? null).catch(() => null);
  return ratesPromise;
}

/** Today's GBP exchange rates (shared, fetched once per page). */
export function useRates(): Record<string, number> | null {
  const [rates, setRates] = useState<Record<string, number> | null>(null);
  useEffect(() => { loadRates().then(setRates); }, []);
  return rates;
}

let accountsPromise: Promise<Account[]> | null = null;
function loadAccounts() {
  accountsPromise ??= fetch("/api/payments/revision-checkout").then((r) => (r.ok ? r.json() : null))
    .then((d) => (d?.accounts ?? []) as Account[]).catch(() => []);
  return accountsPromise;
}

/** The plan price an account's fixed `amount` applies to. */
export const FULL_ACCESS_GBP = 149;

/** What a visitor pays for `gbp`, in their currency when we have an account for their
 *  country (its fixed `amount` wins for the £149 plan), else GBP. */
export function priceFor(gbp: number, account: Account | undefined, rates: Record<string, number> | null): string {
  const cur = account?.currency?.toUpperCase();
  if (!account || !cur || cur === "GBP") return formatMoney(gbp, "GBP");
  return (gbp === FULL_ACCESS_GBP && account.amount) || localAmount(gbp, cur, rates) || formatMoney(gbp, "GBP");
}

/** The visitor's local price for a GBP amount, or null when it's just GBP. */
export function useLocalPrice(gbp: number): string | null {
  const country = useCountry();
  const rates = useRates();
  const [accounts, setAccounts] = useState<Account[] | null>(null);
  useEffect(() => { loadAccounts().then(setAccounts); }, []);
  if (!accounts || !country) return null;
  const { shown, local } = pickAccounts(accounts, country);
  if (!local) return null;
  const p = priceFor(gbp, shown[0], rates);
  return p.startsWith("£") ? null : p;
}
