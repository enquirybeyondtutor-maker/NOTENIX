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

// ── Shared cache ─────────────────────────────────────────────────────────────
// The menu badges, the dashboard and the Homework page all read the same inbox. It is
// fetched once and reused for FRESH_MS (also across full page loads, via sessionStorage),
// so clicking between pages costs no extra requests. It refreshes when it goes stale, when
// the student comes back to the tab, and straight after they open, hand in or submit work.
const FRESH_MS = 2 * 60 * 1000;
const STORE = "notenix_inbox";
type Raw = { key: string; at: number; notes: any[]; tests: any[] };
let mem: Raw | null = null;
let inflight: { key: string; p: Promise<Inbox> } | null = null;
const listeners = new Set<(x: Inbox) => void>();

const userKey = () => {
  try { return (localStorage.getItem("notenix_token") || "").slice(-32); } catch { return ""; }
};

function cached(): Raw | null {
  const key = userKey();
  if (mem && mem.key === key) return mem;
  try {
    const r = JSON.parse(sessionStorage.getItem(STORE) || "null") as Raw | null;
    if (r && r.key === key) return (mem = r);
  } catch { /* storage blocked or bad JSON: just fetch */ }
  return null;
}

/** The cached inbox right now (possibly stale), or null: lets pages render without a flash. */
export function peekInbox(): Inbox | null {
  const r = cached();
  return r ? buildInbox(r.notes, r.tests) : null;
}

export async function loadInbox(opts: { fresh?: boolean } = {}): Promise<Inbox> {
  const key = userKey();
  const r = cached();
  if (!opts.fresh && r && Date.now() - r.at < FRESH_MS) return buildInbox(r.notes, r.tests);
  if (inflight && inflight.key === key) return inflight.p;  // one request, however many callers
  const p = (async () => {
    const [n, t] = await Promise.all([
      notesAPI.mine().then((x) => x.data).catch(() => null),
      testsAPI.mine().then((x) => x.data).catch(() => null),
    ]);
    const notes = Array.isArray(n) ? n : r?.notes ?? [];
    const tests = Array.isArray(t) ? t : r?.tests ?? [];
    if (Array.isArray(n) && Array.isArray(t)) {
      mem = { key, at: Date.now(), notes, tests };
      try { sessionStorage.setItem(STORE, JSON.stringify(mem)); } catch { /* storage full or blocked */ }
    }
    const box = buildInbox(notes, tests);
    listeners.forEach((fn) => fn(box));
    return box;
  })().finally(() => { inflight = null; });
  inflight = { key, p };
  return p;
}

/** Something changed (homework handed in, test submitted): refetch for everyone listening. */
export function invalidateInbox() {
  mem = null;
  try { sessionStorage.removeItem(STORE); } catch { /* ignore */ }
  if (typeof window !== "undefined") window.dispatchEvent(new Event("notenix:inbox"));
}

/** Inbox for a signed-in student, shared with every other component that uses it. */
export function useInbox(enabled: boolean, _refreshKey = ""): Inbox | null {
  const [inbox, setInbox] = useState<Inbox | null>(null);
  useEffect(() => {
    if (!enabled) return;
    let alive = true;
    const set = (x: Inbox) => { if (alive) setInbox(x); };
    const now = peekInbox();
    if (now) setInbox(now);
    listeners.add(set);
    loadInbox().then(set);                                   // cached unless stale
    const fresh = () => { loadInbox({ fresh: true }).then(set); };
    const onVisible = () => { if (document.visibilityState === "visible") loadInbox().then(set); };
    window.addEventListener("notenix:seen", fresh);
    window.addEventListener("notenix:inbox", fresh);
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      alive = false;
      listeners.delete(set);
      window.removeEventListener("notenix:seen", fresh);
      window.removeEventListener("notenix:inbox", fresh);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, [enabled, _refreshKey]);
  return inbox;
}
