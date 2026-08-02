"use client";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export const Input = forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "w-full bg-white border border-line rounded-lg px-3.5 py-2.5 text-sm text-ink",
        "placeholder:text-ink-subtle transition-all outline-none",
        "focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10",
        className
      )}
      {...props}
    />
  )
);
Input.displayName = "Input";

export const Select = forwardRef<HTMLSelectElement, React.SelectHTMLAttributes<HTMLSelectElement>>(
  ({ className, children, ...props }, ref) => (
    <select
      ref={ref}
      className={cn(
        "w-full bg-white border border-line rounded-lg px-3.5 py-2.5 text-sm text-ink",
        "transition-all outline-none appearance-none cursor-pointer",
        "focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10",
        className
      )}
      {...props}
    >
      {children}
    </select>
  )
);
Select.displayName = "Select";

export function Field({
  label,
  hint,
  error,
  children,
}: {
  label?: string;
  hint?: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-1.5">
      {label && <label className="block text-sm font-medium text-ink">{label}</label>}
      {children}
      {error ? (
        <p className="text-xs text-red-600">{error}</p>
      ) : hint ? (
        <p className="text-xs text-ink-subtle">{hint}</p>
      ) : null}
    </div>
  );
}
