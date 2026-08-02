"use client";
import { forwardRef } from "react";
import Link from "next/link";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

type Variant = "primary" | "secondary" | "ghost" | "danger" | "inverse" | "outline-inverse";
type Size = "sm" | "md" | "lg";

const variants: Record<Variant, string> = {
  primary: "bg-brand-600 text-white shadow-xs hover:bg-brand-700 active:bg-brand-800",
  secondary: "bg-white text-ink border border-line shadow-xs hover:bg-slate-50",
  ghost: "bg-transparent text-ink-muted hover:bg-slate-100 hover:text-ink",
  danger: "bg-red-600 text-white hover:bg-red-700",
  inverse: "bg-white text-brand-700 hover:bg-brand-50 shadow-xs",
  "outline-inverse": "bg-transparent text-white border border-white/30 hover:bg-white/10",
};

const sizes: Record<Size, string> = {
  sm: "text-xs px-3 py-2 rounded-lg gap-1.5",
  md: "text-sm px-4 py-2.5 rounded-lg gap-2",
  lg: "text-base px-5 py-3 rounded-xl gap-2",
};

const base =
  "inline-flex items-center justify-center font-medium transition-all duration-150 " +
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/40 " +
  "disabled:opacity-50 disabled:pointer-events-none whitespace-nowrap";

interface CommonProps {
  variant?: Variant;
  size?: Size;
  loading?: boolean;
  className?: string;
  children: React.ReactNode;
}
type ButtonProps = CommonProps & Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, keyof CommonProps> & { href?: undefined };
type LinkProps = CommonProps & { href: string; target?: string; rel?: string };

export const Button = forwardRef<HTMLButtonElement, ButtonProps | LinkProps>(
  ({ variant = "primary", size = "md", loading, className, children, ...props }, ref) => {
    const classes = cn(base, sizes[size], variants[variant], className);
    if ("href" in props && props.href) {
      const { href, target, rel } = props as LinkProps;
      return (
        <Link href={href} target={target} rel={rel} className={classes}>
          {loading && <Loader2 className="animate-spin" size={16} />}
          {children}
        </Link>
      );
    }
    const btn = props as ButtonProps;
    return (
      <button ref={ref} className={classes} disabled={loading || btn.disabled} {...btn}>
        {loading && <Loader2 className="animate-spin" size={16} />}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
