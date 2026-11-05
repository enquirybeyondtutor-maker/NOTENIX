"use client";
import { QRCodeSVG } from "qrcode.react";
import { ExternalLink } from "lucide-react";

// One-click payment link (e.g. Wise) shown as a big button plus a QR code,
// so a parent on a laptop can scan and pay from their phone.
export default function PayLink({ href, label, hint }: { href: string; label: string; hint?: string }) {
  return (
    <div className="flex flex-col items-center gap-5 rounded-xl border border-brand-200 bg-brand-50 p-5 sm:flex-row">
      <div className="flex-1 text-center sm:text-left">
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 px-5 py-3 font-semibold text-white hover:bg-brand-700 sm:w-auto"
        >
          {label} <ExternalLink size={15} />
        </a>
        <p className="mt-2 text-xs text-ink-muted">
          {hint ?? "Secure payment through Wise: card, Apple Pay, Google Pay or bank, in your own currency."}
        </p>
      </div>
      <div className="shrink-0 text-center">
        <div className="rounded-lg bg-white p-2"><QRCodeSVG value={href} size={112} /></div>
        <p className="mt-1 text-[11px] text-ink-subtle">Scan to pay on your phone</p>
      </div>
    </div>
  );
}
