import type { Metadata } from "next";
import Link from "next/link";
import { SITE } from "@/lib/site";
import { Button } from "@/components/ui/Button";
import { MathText } from "@/components/MathText";
import skills from "@/lib/sat-skills.json";

export const metadata: Metadata = {
  title: "Every Digital SAT Skill, with Free Practice Questions | Notenix SAT",
  description: "All 30 skills tested on the Digital SAT, Reading and Writing and Math, explained simply with free practice questions and worked explanations.",
  alternates: { canonical: `${SITE}/sat/skills` },
};

const DOMAINS: [string, "rw" | "math"][] = [
  ["Information and Ideas", "rw"], ["Craft and Structure", "rw"], ["Expression of Ideas", "rw"], ["Standard English Conventions", "rw"],
  ["Algebra", "math"], ["Advanced Math", "math"], ["Problem-Solving and Data Analysis", "math"], ["Geometry and Trigonometry", "math"],
];

export default function SatSkills() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
      <span className="eyebrow">Notenix SAT</span>
      <h1 className="mt-2 text-3xl font-bold tracking-tight text-ink sm:text-4xl">Every Digital SAT skill</h1>
      <p className="mt-3 max-w-3xl text-lg text-ink-muted">
        The SAT reports your results across eight areas and thirty skills. Pick any skill to see what it tests and try free practice questions.
      </p>
      <Button href="/sat/diagnostic" className="mt-6">Find your weakest skills: free diagnostic</Button>
      {(["rw", "math"] as const).map((sec) => (
        <section key={sec} className="mt-12">
          <h2 className="text-xl font-bold text-ink">{sec === "rw" ? "Reading and Writing" : "Math"}</h2>
          <div className="mt-5 grid gap-5 md:grid-cols-2">
            {DOMAINS.filter(([, s]) => s === sec).map(([d]) => (
              <div key={d} className="card p-5">
                <h3 className="font-semibold text-ink">{d}</h3>
                <ul className="mt-3 space-y-2.5">
                  {skills.filter((s) => s.domain === d).map((s) => (
                    <li key={s.slug}>
                      <Link href={`/sat/skills/${s.slug}`} className="font-medium text-brand-700 hover:underline">{s.skill}</Link>
                      <p className="text-sm text-ink-muted"><MathText text={s.about} /></p>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
