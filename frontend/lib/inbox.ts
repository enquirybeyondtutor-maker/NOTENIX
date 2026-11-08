"use client";
import { useEffect, useState } from "react";
import { notesAPI, testsAPI } from "@/lib/api";

// What a student has waiting from their tutor, worked out from their notes and assigned tests.
// Used by the dashboard's "From your tutor" panel, the Homework page and the menu badges.

export type InboxItem = {
  key: string;
  kind: "homework" | "notes" | "test";
  title: string;
  subject?: string | null;
  due_at?: string | null;
  isNew: boolean;
  href: string;
  action: string;
};

export type Inbox = {
  notes: any[];         // every shared note/homework file (with seen + submission)
  tests: any[];         // every assigned test (homework-kind included)
  todo: InboxItem[];    // homework to hand in, tests to sit, new class notes; most urgent first
  counts: { homework: number; notes: number; tests: number };
};

const time = (d?: string | null) => (d ? new Date(d).getTime() : Infinity);

/** Marked past papers are stored as untimed homework-kind tests, but students think of them as tests. */
export const boardKind = (t: { kind?: string; class_label?: string | null }): "test" | "homework" =>
  t.kind === "homework" && t.class_label !== "Marked past paper" ? "homework" : "test";

export function buildInbox(notes: any[], tests: any[]): Inbox {
  const todo: InboxItem[] = [];
  for (const n of notes) {
    if (n.kind === "homework" && !n.submission) {
      todo.push({ key: `n${n.id}`, kind: "homework", title: n.title, subject: n.subject, due_at: n.due_at,
        isNew: n.seen === false, href: `/homework#note-${n.id}`, action: "Open homework" });
    } else if (n.kind !== "homework" && n.seen === false) {
      todo.push({ key: `n${n.id}`, kind: "notes", title: n.title, subject: n.subject, due_at: null,
        isNew: true, href: `/notes#note-${n.id}`, action: "Read notes" });
    }
  }
  for (const t of tests) {
    if (t.status === "completed") continue;
    const hw = boardKind(t) === "homework";
    todo.push({ key: `t${t.assignment_id}`, kind: hw ? "homework" : "test", title: t.title, subject: t.subject,
      due_at: t.due_at, isNew: !t.started, href: `/tests/${t.assignment_id}`,
      action: hw ? "Start homework" : t.mode === "written" ? "Write answers" : "Start test" });
  }
  // New things first, then whatever is due soonest.
  todo.sort((a, b) => Number(b.isNew) - Number(a.isNew) || time(a.due_at) - time(b.due_at));
  return {
    notes, tests, todo,
    counts: {
      homework: todo.filter((i) => i.kind === "homework").length,
      notes: todo.filter((i) => i.kind === "notes").length,
      tests: todo.filter((i) => i.kind === "test").length,
    },
  };
}

export async function loadInbox(): Promise<Inbox> {
  const [n, t] = await Promise.all([
    notesAPI.mine().then((r) => r.data).catch(() => []),
    testsAPI.mine().then((r) => r.data).catch(() => []),
  ]);
  return buildInbox(Array.isArray(n) ? n : [], Array.isArray(t) ? t : []);
}

/** Inbox for a signed-in student; reloads when a note is opened, or when refreshKey (e.g. the path) changes. */
export function useInbox(enabled: boolean, refreshKey = ""): Inbox | null {
  const [inbox, setInbox] = useState<Inbox | null>(null);
  useEffect(() => {
    if (!enabled) return;
    let alive = true;
    const refresh = () => loadInbox().then((x) => alive && setInbox(x));
    refresh();
    window.addEventListener("notenix:seen", refresh);
    return () => { alive = false; window.removeEventListener("notenix:seen", refresh); };
  }, [enabled, refreshKey]);
  return inbox;
}
