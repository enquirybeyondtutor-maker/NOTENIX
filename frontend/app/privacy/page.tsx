import type { Metadata } from "next";
import { SITE } from "@/lib/site";
import LegalPage from "@/components/LegalPage";
import { legalEntity, operatorLine } from "@/lib/legal";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "What data Notenix collects, why, who processes it and how long it is kept.",
  alternates: { canonical: `${SITE}/privacy` },
};

export default function PrivacyPage() {
  return (
    <LegalPage
      title="Privacy policy"
      intro="We collect only what we need to run your practice tests, mark them and look after your account. We do not sell your data."
    >
      <section>
        <h2>Who is responsible for your data</h2>
        <p>
          Notenix is operated by {operatorLine}. {legalEntity.operator} is the data controller (UK GDPR) and data
          fiduciary (India&apos;s Digital Personal Data Protection Act 2023) for personal data collected through Notenix.
        </p>
      </section>

      <section>
        <h2>What we collect</h2>
        <ul>
          <li><b className="text-ink">Account:</b> your name, email address, role (student or teacher) and a securely hashed password.</li>
          <li><b className="text-ink">Practice:</b> your answers, any photos of working you upload, scores, marks, feedback and timings.</li>
          <li><b className="text-ink">Requests:</b> the exam, subject, notes and preferred date you give when you request a test.</li>
          <li><b className="text-ink">Payments:</b> the amount, payment reference, and the payer name and note you give us. We never see or store card details.</li>
          <li><b className="text-ink">Analytics:</b> anonymous usage statistics through Google Analytics, only if you accept analytics cookies.</li>
        </ul>
      </section>

      <section>
        <h2>How long we keep it</h2>
        <p>
          Your typed answers and uploaded photos are deleted 28 days after you submit a test. Your marks, grades and
          feedback are kept so you can track your progress. Account details are kept until you ask us to delete your account.
        </p>
      </section>

      <section>
        <h2>Who processes it</h2>
        <ul>
          <li><b className="text-ink">Tutors:</b> tutors from Beyond Tutors see the answers you submit for a tutor-marked test so they can mark them. Teachers see the work you submit for tests they assigned.</li>
          <li><b className="text-ink">AI tools used by our team:</b> students&apos; questions and answers are written and marked by people, not by AI. Our tutors may use Anthropic&apos;s Claude AI to turn a paper they upload into a test and to draft the written summary on a progress report, which sends test results to Anthropic. They are not used to train Anthropic&apos;s models.</li>
          <li><b className="text-ink">Hosting and email:</b> the site and database are hosted by cloud providers (Vercel and Render), and verification and notification emails go through an email delivery provider.</li>
        </ul>
      </section>

      <section>
        <h2>Cookies</h2>
        <p>
          We use your browser&apos;s storage to keep you signed in and remember your cookie choice. Analytics cookies are
          only set if you click Accept on the cookie notice.
        </p>
      </section>

      <section>
        <h2>Your choices</h2>
        <p>
          You can ask for a copy of your data, ask us to correct it, or ask us to delete your account by emailing{" "}
          <a href="mailto:support@notenix.com" className="text-brand-600 hover:underline">support@notenix.com</a>. If you are under 13,
          a parent or guardian can make these requests for you. We respond within one month.
        </p>
        <p>
          In the UK you can also complain to the Information Commissioner&apos;s Office (ico.org.uk); in India, to the
          Data Protection Board.
        </p>
      </section>
    </LegalPage>
  );
}
