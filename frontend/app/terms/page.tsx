import type { Metadata } from "next";
import Link from "next/link";
import { SITE } from "@/lib/site";
import LegalPage from "@/components/LegalPage";
import { legalEntity, operatorLine } from "@/lib/legal";

export const metadata: Metadata = {
  title: "Terms of Use",
  description: "The terms for using Notenix practice tests, Pro access and tutor-marked mock tests.",
  alternates: { canonical: `${SITE}/terms` },
};

export default function TermsPage() {
  return (
    <LegalPage
      title="Terms of use"
      intro="These terms explain what Notenix provides, what you can expect from us and what we expect from you. By creating an account you agree to them."
    >
      <section>
        <h2>Who runs Notenix</h2>
        <p>
          Notenix is operated by {operatorLine}. Tutor-marked tests are marked by tutors from Beyond Tutors, which
          is also run by {legalEntity.operator}. Contact us at <a href="mailto:hello@notenix.com" className="text-brand-600 hover:underline">hello@notenix.com</a>.
        </p>
        <p>GSTIN {legalEntity.gstin} · Udyam {legalEntity.udyam}</p>
        <p>Notenix is an independent practice service. It is not affiliated with or endorsed by any exam board or test provider.</p>
      </section>

      <section>
        <h2>What you get</h2>
        <ul>
          <li><b className="text-ink">Free account:</b> free sample questions, a limited number of AI-generated quizzes, tests a teacher or tutor assigns to you, and your results and progress.</li>
          <li><b className="text-ink">Pro:</b> a 30-day pass with unlimited AI-generated quizzes and written-answer practice that is marked automatically by AI. Pro does not include marking by a human tutor.</li>
          <li><b className="text-ink">Tutor-marked tests:</b> you request a mock, our team assigns one to your account, you sit it online, and a tutor marks your written answers and adds feedback. The price, or the fact that it is currently free, is shown on the request form before you send it.</li>
        </ul>
      </section>

      <section>
        <h2>Payment and access</h2>
        <ul>
          <li>Pro is paid by bank transfer. It is a one-off 30-day pass, not a subscription, and it never renews automatically.</li>
          <li>Pro starts once we have confirmed your payment has arrived. Paying again while Pro is active adds another 30 days.</li>
          <li>Prices are shown on the <Link href="/pricing" className="text-brand-600 hover:underline">pricing page</Link> and on the payment screen before you pay. Your bank may charge transfer or currency-conversion fees.</li>
          <li>Cancellations and refunds are covered in our <Link href="/refunds" className="text-brand-600 hover:underline">refund policy</Link>.</li>
        </ul>
      </section>

      <section>
        <h2>Marks, grades and feedback</h2>
        <p>
          Automatic marks, AI marking and grade estimates are a guide to help you practise. They are not official
          results and do not predict the grade you will receive. Grade boundaries change from year to year.
        </p>
      </section>

      <section>
        <h2>Your account</h2>
        <ul>
          <li>Keep your password private. You are responsible for activity on your account.</li>
          <li>Students under 13 need a parent or guardian to create the account or agree to these terms.</li>
          <li>Do your own work in tests, and do not share, copy or resell Notenix questions.</li>
          <li>We may suspend accounts that misuse the service or try to break it.</li>
        </ul>
      </section>

      <section>
        <h2>Our content</h2>
        <p>Questions, explanations and reports on Notenix are our original work. You may use them for your own study.</p>
      </section>

      <section>
        <h2>Liability and law</h2>
        <p>
          Nothing in these terms limits rights you have under consumer law where you live. Otherwise our total
          liability is limited to the fees you paid for the service concerned. These terms are governed by the laws of India.
        </p>
      </section>

      <section>
        <h2>Changes</h2>
        <p>
          If we change these terms in a way that affects you, we will say so on the site or by email before the change
          applies. Anything you have already paid for keeps the terms it was sold with.
        </p>
      </section>
    </LegalPage>
  );
}
