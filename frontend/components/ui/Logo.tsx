import Link from "next/link";
import { cn } from "@/lib/utils";

// "Marked N": an N whose right stroke rises like a tutor's mark. Same path as
// app/icon.svg and public/brand/notenix-*.svg; keep them in sync.
export const MARK_PATH = "M0 100V8H27L63 64V40L84 4H100L86 34V100H60L23 44V100Z";
export const BRAND_VIOLET = "#5444DC";

export function Mark({ className, color = "currentColor" }: { className?: string; color?: string }) {
  return (
    <svg viewBox="0 4 100 96" className={className} aria-hidden>
      <path d={MARK_PATH} fill={color} />
    </svg>
  );
}

/** Notenix logo: Marked N in a violet tile + wordmark.
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
    <span className={cn("flex items-center gap-2.5", className)} aria-label="Notenix">
      <span
        className="grid h-8 w-8 place-items-center rounded-lg shadow-xs"
        style={{ background: light ? "#fff" : BRAND_VIOLET }}
      >
        <Mark className="h-[18px] w-[19px]" color={light ? BRAND_VIOLET : "#fff"} />
      </span>
      <span className={cn("text-[17px] font-bold tracking-tight", light ? "text-white" : "text-[#151829]")}>Notenix</span>
    </span>
  );
  if (href) return <Link href={href}>{content}</Link>;
  return content;
}
