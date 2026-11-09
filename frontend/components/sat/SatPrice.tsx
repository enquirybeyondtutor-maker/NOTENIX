"use client";
import { useEffect, useState } from "react";
import { satAPI, satCurrency } from "@/lib/satApi";
import { useCountry } from "@/lib/country";

/** The Notenix SAT price in the visitor's currency ($129 until their country is known). */
export default function SatPrice({ className = "" }: { className?: string }) {
  const country = useCountry();
  const [label, setLabel] = useState("$129");
  useEffect(() => {
    if (country) satAPI.price(satCurrency(country)).then((r) => setLabel(r.data.label)).catch(() => {});
  }, [country]);
  return <span className={className}>{label}</span>;
}
