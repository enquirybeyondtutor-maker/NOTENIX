import type { Metadata } from "next";
import { SITE } from "@/lib/site";
import LegalPage from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Cancellation & Refund Policy",
  description: "How Notenix Pro passes and tutor-marked tests can be cancelled and refunded.",
  alternates: { canonical: `${SITE}/refunds` },
};

export default function RefundsPage() {
  return (
    <LegalPage
      title="Cancellation and refunds"
      intro="Pro is a one-off 30-day pass, so there is nothing to cancel: it simply ends after 30 days unless you choose to pay again."
    >
      <section>
        <h2>Pro passes</h2>
        <ul>
          <li>If we have not switched Pro on yet, we will refund your payment in full on request.</li>
          <li>If you are not happy within 7 days of Pro starting, email us and we will refund it in full.</li>
          <li>After 7 days, Pro runs until the end of its 30 days and is not refunded.</li>
        </ul>
      </section>

      <section>
        <h2>Tutor-marked tests</h2>
        <ul>
          <li>Requests are free right now. If a price applies, it is shown on the request form before you send it.</li>
          <li>For a paid request, you get a full refund if you cancel before you start the test, or if we cannot assign or mark it.</li>
        </ul>
      </section>

      <section>
        <h2>How refunds are paid</h2>
        <p>
          Email <a href="mailto:hello@notenix.com" className="text-brand-600 hover:underline">hello@notenix.com</a> with your payment
          reference (it starts with NX-). We refund to the account you paid from, usually within 5 working days. We
          cannot refund fees your bank charged for the original transfer.
        </p>
      </section>
    </LegalPage>
  );
}
