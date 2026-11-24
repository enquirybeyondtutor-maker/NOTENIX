"use client";
import { Field, Input } from "@/components/ui/Input";

/** Date of birth of the person who paid (optional). Wise sometimes asks for it to confirm who sent
 *  a transfer, so it helps us match the payment faster. */
export default function PayerDobField({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  const today = new Date().toISOString().slice(0, 10);
  return (
    <Field label="Date of birth of the person who paid"
      hint="Optional, but it helps us process your payment faster: Wise sometimes asks for it to confirm a transfer.">
      <Input type="date" value={value} max={today} min="1900-01-01" onChange={(e) => onChange(e.target.value)} />
    </Field>
  );
}
