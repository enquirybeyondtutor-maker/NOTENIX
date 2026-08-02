import Link from "next/link";
import { cn } from "@/lib/utils";

/** Notenix wordmark — `N` glyph in a rounded tile + wordmark.
 *  `light` renders white-on-dark for use over the brand panel. */
export function Logo({
  className,
  href = "/",
  light = false,
}: {
  className?: string;
  href?: string | null;
  light?: boolean;
}) {
  const content = (
    <span className={cn("flex items-center gap-2.5", className)}>
      <span
        className={cn(
          "grid h-8 w-8 place-items-center rounded-lg shadow-xs",
          light ? "bg-white text-brand-600" : "bg-brand-600 text-white"
        )}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden>
          <path d="M5 19V5l14 14V5" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </span>
      <span className={cn("text-[17px] font-bold tracking-tight", light ? "text-white" : "text-ink")}>Notenix</span>
    </span>
  );
  if (href) return <Link href={href}>{content}</Link>;
  return content;
}
