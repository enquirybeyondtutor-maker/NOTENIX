"use client";
import { useState } from "react";
import { Lock, Hourglass } from "lucide-react";
import PaymentBox from "./PaymentBox";
import { Button } from "./ui/Button";

export interface UnlockInfo {
  locked: true;
  count?: number;
  amount: number;
  currency: string;
  price_label: string;
  reference: string;
  payment_pending: boolean;
  message?: string;
}

// Shown instead of the test when it's locked until paid (the server sends no questions).
export default function LockedTest({ info }: { info: UnlockInfo }) {
  const [pending, setPending] = useState(info.payment_pending);
  const many = (info.count ?? 1) > 1;

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <div className="text-center">
        <span className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-amber-50 text-amber-600">
          {pending ? <Hourglass size={24} /> : <Lock size={24} />}
        </span>
        {pending ? (
          <>
            <h1 className="mt-4 text-xl font-semibold text-ink">We're checking your payment</h1>
            <p className="mx-auto mt-2 max-w-md text-sm text-ink-muted">
              Thanks for paying. As soon as we confirm it, {many ? "your tests unlock" : "this test unlocks"} and
              we'll email you, usually within 24 hours.
            </p>
          </>
        ) : (
          <>
            <h1 className="mt-4 text-xl font-semibold text-ink">Your payment isn't done yet</h1>
            <p className="mx-auto mt-2 max-w-md text-sm text-ink-muted">
              Please unlock {many ? `your ${info.count} tests` : "this test"} by making a payment of{" "}
              <b className="text-ink">{info.price_label}</b>.
              {many && " One payment unlocks all of them."}
            </p>
          </>
        )}
      </div>

      {!pending && (
        <div className="mt-8">
          <PaymentBox
            purpose="unlock"
            amount={info.amount}
            currency={info.currency}
            reference={info.reference}
            onClaimed={() => setPending(true)}
          />
        </div>
      )}

      <div className="mt-8 text-center">
        <Button href="/tests" variant="secondary">Back to my tests</Button>
      </div>
    </div>
  );
}
