// Public KS3 topic pages (/ks3/year-7/maths/negative-numbers …), built from the KS3 notes.
// Data: lib/ks3-topics.json, exported by backend/ks3_content/export_web.py.
import data from "./ks3-topics.json";

export type Ks3Question = { question: string; options: string[]; answer: string; explanation: string; topic: string };
export type Ks3Topic = { key: string; year: number; subject: string; title: string; slug: string; body: string; questions: Ks3Question[] };

export const TOPICS = data as Ks3Topic[];
export const YEARS = [7, 8, 9] as const;
export const SUBJECTS = ["Maths", "Science", "English"] as const;

export const yearSlug = (y: number) => `year-${y}`;
export const subjectSlug = (s: string) => s.toLowerCase();
export const topicPath = (t: Ks3Topic) => `/ks3/${yearSlug(t.year)}/${subjectSlug(t.subject)}/${t.slug}`;

export function findTopic(year: string, subject: string, slug: string): Ks3Topic | undefined {
  return TOPICS.find((t) => yearSlug(t.year) === year && subjectSlug(t.subject) === subject && t.slug === slug);
}

export function topicsFor(year: number, subject?: string): Ks3Topic[] {
  return TOPICS.filter((t) => t.year === year && (!subject || t.subject === subject));
}

/** The notes are plain text: CAPS lines are headings, "• " lines are bullets, the rest paragraphs. */
export type Block = { kind: "h"; text: string } | { kind: "ul"; items: string[] } | { kind: "p"; text: string };

export function blocks(body: string): Block[] {
  const out: Block[] = [];
  for (const raw of body.split("\n")) {
    const line = raw.trim();
    if (!line) continue;
    const letters = line.replace(/[^A-Za-z]/g, "");
    if (letters.length > 2 && letters === letters.toUpperCase() && !line.includes("$") && line.length < 70) {
      out.push({ kind: "h", text: line.charAt(0) + line.slice(1).toLowerCase() });
    } else if (line.startsWith("• ")) {
      const last = out[out.length - 1];
      if (last && last.kind === "ul") last.items.push(line.slice(2));
      else out.push({ kind: "ul", items: [line.slice(2)] });
    } else {
      out.push({ kind: "p", text: line });
    }
  }
  return out;
}

/** First plain sentence of the notes, for meta descriptions. */
export function summary(t: Ks3Topic): string {
  const first = blocks(t.body).find((b) => b.kind === "p") as { text: string } | undefined;
  const clean = (first?.text || "").replace(/\$[^$]*\$/g, "").replace(/\s+/g, " ").trim();
  return clean.length > 40 ? clean.slice(0, 150) : `Clear Year ${t.year} ${t.subject} notes on ${t.title.toLowerCase()}, with worked examples.`;
}
