"use client";
import { useLocalPrice } from "@/lib/country";

// Shows the price in the visitor's currency (e.g. "A$290") with the GBP price beside it.
// UK and unknown visitors see the GBP price only. Server render shows GBP.
export default function LocalPrice({ gbp, className, subClassName }: { gbp: number; className?: string; subClassName?: string }) {
  const local = useLocalPrice(gbp);
  return (
    <>
      <span className={className}>{local ?? `£${gbp}`}</span>
      {local && <span className={subClassName}> (£{gbp})</span>}
    </>
  );
}
