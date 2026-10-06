"use client";
/* Beyond Tutors performance report — A4, print-to-PDF. All numbers come from the
   /reports/build payload; charts are hand-rolled SVG (no chart dependency). */
import { Instagram, Youtube, Facebook, AtSign, MessageCircle, Globe } from "lucide-react";

// ── Brand + chart palette (validated: categorical sections pass all CVD checks;
//    correct/wrong is 7.3 ΔE deutan, so status always ships with labels/legend + gaps) ──
const C = {
  navy: "#0E0B24", ink: "#14112E", muted: "#5B5875", subtle: "#8E8BA6", line: "#E7E5F0", wash: "#F6F5FB",
  violet: "#7C3AED", indigo: "#4338CA", amber: "#F59E0B",
  correct: "#0F9D74", wrong: "#E5484D", skipped: "#A1A1AA",
};
const SERIES = ["#4338CA", "#D97706", "#0D9488", "#7C3AED", "#DB2777"]; // fixed order, never cycled

export const SOCIALS = [
  { icon: Instagram, label: "@beyondtutors_", href: "https://instagram.com/beyondtutors_" },
  { icon: Youtube, label: "@thebeyondtutors", href: "https://youtube.com/@thebeyondtutors" },
  { icon: Facebook, label: "Beyond Tutors", href: "https://www.facebook.com/profile.php?id=61594833854440" },
  { icon: AtSign, label: "@beyondtutors_", href: "https://www.threads.net/@beyondtutors_" },
  { icon: MessageCircle, label: "WhatsApp Channel", href: "https://whatsapp.com/channel/0029VaG7hGW6GcGKrQlvOB0I" },
  { icon: Globe, label: "thebeyondtutors.com", href: "https://thebeyondtutors.com" },
];

const fmtDate = (iso?: string | null) =>
  iso ? new Date(iso).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }) : "—";
const shortDate = (iso?: string | null) =>
  iso ? new Date(iso).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : "";
const mmss = (s?: number | null) => {
  if (s == null) return "—";
  const m = Math.floor(s / 60), r = Math.round(s % 60);
  return m ? `${m}m ${String(r).padStart(2, "0")}s` : `${r}s`;
};
const pct = (v?: number | null) => (v == null ? "—" : `${Math.round(v)}%`);
const first = (name: string) => (name || "Student").split(" ")[0];
const shortTitle = (t: string) => t.replace(/^(ESAT|TMUA)\s+Practice Paper\s*/i, "Paper ").replace(/:.*$/, "").trim();

// ── Building blocks ──────────────────────────────────────────────────────────

function SectionTitle({ n, title, sub }: { n: number; title: string; sub?: string }) {
  return (
    <div className="mb-3 mt-7 flex items-end gap-3 break-after-avoid">
      <span className="grid h-7 w-7 shrink-0 place-items-center rounded-lg text-[12px] font-bold text-white"
        style={{ background: `linear-gradient(135deg, ${C.violet}, ${C.indigo})` }}>{n}</span>
      <div>
        <h2 className="text-[17px] font-bold leading-tight" style={{ color: C.ink }}>{title}</h2>
        {sub && <p className="text-[11px]" style={{ color: C.muted }}>{sub}</p>}
      </div>
    </div>
  );
}

function Tile({ label, value, note, accent }: { label: string; value: string; note?: string; accent?: string }) {
  return (
    <div className="avoid-break rounded-xl border px-3 py-2.5" style={{ borderColor: C.line, background: "#fff" }}>
      <div className="text-[10px] font-semibold uppercase tracking-wide" style={{ color: C.subtle }}>{label}</div>
      <div className="mt-0.5 text-[20px] font-bold leading-tight" style={{ color: accent || C.ink }}>{value}</div>
      {note && <div className="text-[10px] leading-snug" style={{ color: C.muted }}>{note}</div>}
    </div>
  );
}

function Prose({ children }: { children?: React.ReactNode }) {
  if (!children) return null;
  return <p className="text-[12.5px] leading-relaxed" style={{ color: C.ink }}>{children}</p>;
}

function Callout({ title, children }: { title: string; children?: React.ReactNode }) {
  if (!children) return null;
  return (
    <div className="avoid-break mt-3 rounded-xl border-l-4 px-4 py-3" style={{ borderColor: C.violet, background: C.wash }}>
      <div className="mb-1 text-[10px] font-bold uppercase tracking-wider" style={{ color: C.violet }}>{title}</div>
      <div className="text-[12.5px] leading-relaxed" style={{ color: C.ink }}>{children}</div>
    </div>
  );
}

function StatusLegend() {
  const items = [["Correct", C.correct, "✓"], ["Wrong", C.wrong, "✗"], ["Skipped", C.skipped, "–"]];
  return (
    <div className="flex flex-wrap gap-4 text-[10.5px]" style={{ color: C.muted }}>
      {items.map(([l, c, g]) => (
        <span key={l} className="inline-flex items-center gap-1.5">
          <span className="grid h-3.5 w-3.5 place-items-center rounded-[4px] text-[9px] font-bold text-white" style={{ background: c }}>{g}</span>{l}
        </span>
      ))}
    </div>
  );
}

const HATCH = (
  <defs>
    <pattern id="bt-hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="5" height="5" fill="#E4E4E7" />
      <line x1="0" y1="0" x2="0" y2="5" stroke={C.skipped} strokeWidth="2" />
    </pattern>
  </defs>
);

// ── Charts ───────────────────────────────────────────────────────────────────

/** Where the student sits on the official 1.0–9.0 scale, with the estimate range and benchmarks. */
function BandScale({ rows, benchmarks }: { rows: { label: string; est: number; low: number; high: number; pctl?: number | null }[]; benchmarks: { label: string; score: number }[] }) {
  const W = 680, L = 104, R = 24, top = 46, rowH = 46;
  const H = top + rows.length * rowH + 22;
  const x = (v: number) => L + ((v - 1) / 8) * (W - L - R);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Estimated band on the 1 to 9 scale">
      <defs>
        <linearGradient id="bt-scale" x1="0" x2="1">
          <stop offset="0" stopColor="#EDE9FE" /><stop offset="1" stopColor="#E0E7FF" />
        </linearGradient>
      </defs>
      {benchmarks.map((b, i) => (
        <g key={b.label}>
          <line x1={x(b.score)} x2={x(b.score)} y1={top - 6} y2={H - 22} stroke={C.subtle} strokeDasharray="3 3" strokeWidth="1" />
          <text x={x(b.score)} y={10 + (i % 3) * 12} textAnchor="middle" fontSize="9.5" fill={C.muted}>
            {b.label} <tspan fontWeight="700" fill={C.ink}>{b.score.toFixed(1)}</tspan>
          </text>
        </g>
      ))}
      {rows.map((r, i) => {
        const y = top + i * rowH + 14;
        return (
          <g key={r.label}>
            <text x={0} y={y + 4} fontSize="11.5" fontWeight="700" fill={C.ink}>{r.label}</text>
            {r.pctl != null && <text x={0} y={y + 18} fontSize="9.5" fill={C.muted}>≈ top {Math.max(1, 100 - r.pctl)}%</text>}
            <rect x={x(1)} y={y - 5} width={x(9) - x(1)} height={10} rx={5} fill="url(#bt-scale)" />
            <rect x={x(r.low)} y={y - 9} width={Math.max(4, x(r.high) - x(r.low))} height={18} rx={9} fill={C.indigo} opacity={0.18} />
            <circle cx={x(r.est)} cy={y} r={8} fill={C.indigo} stroke="#fff" strokeWidth={2} />
            <text x={x(r.est)} y={y + 24} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.indigo}>
              {r.est.toFixed(1)} <tspan fontWeight="500" fill={C.muted} fontSize="9.5">({r.low.toFixed(1)}–{r.high.toFixed(1)})</tspan>
            </text>
          </g>
        );
      })}
      {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((v) => (
        <text key={v} x={x(v)} y={H - 6} textAnchor="middle" fontSize="9.5" fill={C.subtle}>{v}.0</text>
      ))}
    </svg>
  );
}

/** Correct / wrong / skipped split per section (stacked bar, 2px surface gaps). */
function SectionBars({ sections }: { sections: any[] }) {
  const W = 680, L = 104, R = 54, rowH = 30;
  const H = sections.length * rowH + 4;
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Results by section">
      {HATCH}
      {sections.map((s, i) => {
        const y = i * rowH + 4, w = W - L - R;
        const parts = [
          { k: "correct", v: s.correct, fill: C.correct },
          { k: "wrong", v: s.n - s.correct - s.skipped, fill: C.wrong },
          { k: "skipped", v: s.skipped, fill: "url(#bt-hatch)" },
        ];
        let acc = L;
        return (
          <g key={s.section}>
            <text x={0} y={y + 14} fontSize="11.5" fontWeight="700" fill={C.ink}>{s.section}</text>
            {parts.map((p) => {
              const pw = (p.v / s.n) * w;
              const x0 = acc; acc += pw;
              if (pw <= 0) return null;
              return (
                <g key={p.k}>
                  <rect x={x0 + 1} y={y} width={Math.max(0, pw - 2)} height={20} rx={4} fill={p.fill} />
                  {pw > 26 && <text x={x0 + pw / 2} y={y + 14} textAnchor="middle" fontSize="10" fontWeight="700" fill={p.k === "skipped" ? C.ink : "#fff"}>{p.v}</text>}
                </g>
              );
            })}
            <text x={W} y={y + 14} textAnchor="end" fontSize="11.5" fontWeight="800" fill={C.ink}>{pct(s.accuracy)}</text>
          </g>
        );
      })}
    </svg>
  );
}

/** Accuracy per section across mocks (one line per section, direct-labelled). */
function TrendChart({ attempts }: { attempts: any[] }) {
  const names: string[] = [];
  attempts.forEach((a) => a.sections.forEach((s: any) => { if (!names.includes(s.section)) names.push(s.section); }));
  const W = 680, H = 210, L = 34, R = 86, T = 14, B = 40;
  const n = attempts.length;
  const x = (i: number) => (n === 1 ? (L + W - R) / 2 : L + (i / (n - 1)) * (W - L - R));
  const y = (v: number) => T + (1 - v / 100) * (H - T - B);
  // End-of-line labels: start at each series' last point, then push apart so they never collide.
  const ends = names.map((name, si) => {
    const last = [...attempts].reverse().find((a) => a.sections.some((z: any) => z.section === name));
    const v = last?.sections.find((z: any) => z.section === name)?.accuracy ?? 0;
    return { name, si, y: y(v) + 4 };
  }).sort((a, b) => a.y - b.y);
  ends.forEach((e, i) => { if (i > 0 && e.y - ends[i - 1].y < 13) e.y = ends[i - 1].y + 13; });
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Accuracy by section across mocks">
      {[0, 25, 50, 75, 100].map((g) => (
        <g key={g}>
          <line x1={L} x2={W - R} y1={y(g)} y2={y(g)} stroke={C.line} strokeWidth="1" />
          <text x={L - 6} y={y(g) + 3} textAnchor="end" fontSize="9.5" fill={C.subtle}>{g}%</text>
        </g>
      ))}
      {attempts.map((a, i) => (
        <g key={a.attempt_id}>
          <text x={x(i)} y={H - 22} textAnchor="middle" fontSize="9.5" fontWeight="600" fill={C.muted}>{`Mock ${i + 1}`}</text>
          <text x={x(i)} y={H - 10} textAnchor="middle" fontSize="9" fill={C.subtle}>{shortDate(a.date)}</text>
        </g>
      ))}
      {names.map((name, si) => {
        const pts = attempts.map((a, i) => {
          const s = a.sections.find((z: any) => z.section === name);
          return s ? { i, v: s.accuracy as number } : null;
        }).filter(Boolean) as { i: number; v: number }[];
        const color = SERIES[si];
        const labelY = ends.find((e) => e.si === si)!.y;
        return (
          <g key={name}>
            {pts.length > 1 && <polyline fill="none" stroke={color} strokeWidth="2" strokeLinejoin="round" points={pts.map((p) => `${x(p.i)},${y(p.v)}`).join(" ")} />}
            {pts.map((p) => (
              <g key={p.i}>
                <circle cx={x(p.i)} cy={y(p.v)} r={4.5} fill={color} stroke="#fff" strokeWidth={2} />
                <text x={x(p.i)} y={si % 2 ? y(p.v) + 16 : y(p.v) - 9} textAnchor="middle" fontSize="9.5" fontWeight="700" fill={C.ink}>{Math.round(p.v)}%</text>
              </g>
            ))}
            {pts.length > 0 && <text x={W - R + 10} y={labelY} fontSize="10.5" fontWeight="700" fill={C.ink}>
              <tspan fill={color}>●</tspan> {name}</text>}
          </g>
        );
      })}
    </svg>
  );
}

/** Seconds spent on every question of one sitting, coloured by outcome, against even pace. */
function TimeStrip({ attempt }: { attempt: any }) {
  const qs: any[] = attempt.questions;
  const pace: number | null = attempt.timing.pace_seconds;
  const W = 680, H = 190, L = 34, R = 6, T = 16, B = 34;
  const cap = Math.max(pace ? pace * 3 : 0, ...qs.map((q) => q.seconds), 10);
  const maxV = pace ? Math.min(cap, Math.max(pace * 2.2, ...qs.map((q) => q.seconds))) : cap;
  const bw = (W - L - R) / qs.length;
  const y = (v: number) => T + (1 - Math.min(v, maxV) / maxV) * (H - T - B);
  const ticks = [0, Math.round(maxV / 2), Math.round(maxV)];
  // section boundaries
  const bounds: { at: number; name: string }[] = [];
  qs.forEach((q, i) => { if (i === 0 || q.section !== qs[i - 1].section) bounds.push({ at: i, name: q.section }); });
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Time spent per question">
      {HATCH}
      {ticks.map((t) => (
        <g key={t}>
          <line x1={L} x2={W - R} y1={y(t)} y2={y(t)} stroke={C.line} />
          <text x={L - 5} y={y(t) + 3} textAnchor="end" fontSize="9" fill={C.subtle}>{mmss(t)}</text>
        </g>
      ))}
      {qs.map((q, i) => {
        const h = Math.max(2, y(0) - y(q.seconds));
        const fill = q.status === "correct" ? C.correct : q.status === "wrong" ? C.wrong : "url(#bt-hatch)";
        return (
          <g key={q.n}>
            <rect x={L + i * bw + 1} y={y(0) - h} width={Math.max(1, bw - 2)} height={h} rx={Math.min(3, bw / 3)} fill={fill}>
              <title>{`Q${q.n} · ${q.topic} · ${mmss(q.seconds)} · ${q.status}`}</title>
            </rect>
            {q.seconds > maxV && <text x={L + i * bw + bw / 2} y={T - 3} textAnchor="middle" fontSize="8" fill={C.ink}>▲</text>}
            {(q.n === 1 || q.n % 5 === 0) && <text x={L + i * bw + bw / 2} y={H - 20} textAnchor="middle" fontSize="8.5" fill={C.subtle}>{q.n}</text>}
          </g>
        );
      })}
      {pace && (
        <g>
          <line x1={L} x2={W - R} y1={y(pace)} y2={y(pace)} stroke={C.ink} strokeDasharray="5 4" strokeWidth="1.2" />
          <rect x={W - R - 108} y={y(pace) - 17} width={106} height={14} rx={4} fill="#fff" opacity={0.9} />
          <text x={W - R - 4} y={y(pace) - 6} textAnchor="end" fontSize="9.5" fontWeight="700" fill={C.ink}>Even pace · {mmss(pace)}</text>
        </g>
      )}
      {bounds.length > 1 && bounds.map((b) => (
        <g key={b.at}>
          {b.at > 0 && <line x1={L + b.at * bw} x2={L + b.at * bw} y1={T} y2={y(0) + 4} stroke={C.ink} strokeWidth="1" opacity={0.5} />}
          <text x={L + b.at * bw + 4} y={H - 6} fontSize="9.5" fontWeight="700" fill={C.muted}>{b.name} →</text>
        </g>
      ))}
      {bounds.length <= 1 && <text x={L} y={H - 6} fontSize="9.5" fill={C.muted}>Question number</text>}
    </svg>
  );
}

/** Simple single-series horizontal bars (accuracy by difficulty). */
function MiniBars({ rows }: { rows: { label: string; value: number | null; note?: string }[] }) {
  return (
    <div className="space-y-2">
      {rows.map((r) => (
        <div key={r.label} className="flex items-center gap-3 text-[11.5px]">
          <div className="w-24 shrink-0 font-semibold" style={{ color: C.ink }}>{r.label}</div>
          <div className="h-3.5 flex-1 overflow-hidden rounded-full" style={{ background: C.wash }}>
            <div className="h-full rounded-full" style={{ width: `${r.value ?? 0}%`, background: C.indigo }} />
          </div>
          <div className="w-24 shrink-0 text-right" style={{ color: C.ink }}><b>{pct(r.value)}</b> <span style={{ color: C.subtle }}>{r.note}</span></div>
        </div>
      ))}
    </div>
  );
}

const RATING: Record<string, { label: string; bg: string; fg: string }> = {
  strong: { label: "Strong", bg: "#DCFCE7", fg: "#166534" },
  developing: { label: "Developing", bg: "#FEF3C7", fg: "#92400E" },
  weak: { label: "Focus", bg: "#FEE2E2", fg: "#991B1B" },
  "limited data": { label: "Few Qs", bg: "#F1F5F9", fg: "#475569" },
};

// ── Report ───────────────────────────────────────────────────────────────────

export default function ReportView({ report, adminCopy }: { report: any; adminCopy?: boolean }) {
  const r = report;
  const c = r.commentary || {};
  const s = r.summary;
  const name = r.student.name;
  const fname = first(name);
  const attempts: any[] = r.attempts;
  const latest = attempts[attempts.length - 1];
  const timedLatest = [...attempts].reverse().find((a) => a.timing.has_data);

  const bandRows =
    r.band?.unit === "module"
      ? Object.entries(r.band.modules).map(([k, v]: any) => ({ label: k, est: v.estimate, low: v.low, high: v.high, pctl: v.percentile }))
      : r.band?.unit === "total"
        ? [{ label: `${r.exam} total`, est: r.band.estimate, low: r.band.low, high: r.band.high, pctl: r.band.percentile }]
        : [];
  const bandHeadline =
    r.band?.unit === "total" ? `${r.band.estimate.toFixed(1)}` :
      bandRows.length ? bandRows.map((b) => b.est.toFixed(1)).join(" · ") : "—";

  const diffRows = (() => {
    const agg: Record<string, { n: number; c: number }> = {};
    attempts.forEach((a) => a.questions.forEach((q: any) => {
      if (!q.difficulty) return;
      const k = String(q.difficulty);
      agg[k] = agg[k] || { n: 0, c: 0 };
      agg[k].n += 1; agg[k].c += q.status === "correct" ? 1 : 0;
    }));
    return [["1", "Routine"], ["2", "Multi-step"], ["3", "Challenging"]]
      .filter(([k]) => agg[k])
      .map(([k, label]) => ({ label, value: Math.round((100 * agg[k].c) / agg[k].n), note: `${agg[k].c}/${agg[k].n}` }));
  })();

  const totalSkips = attempts.reduce((t, a) => t + a.skips.count, 0);
  const guessValue = attempts.reduce((t, a) => t + a.skips.guess_value, 0);
  const easySkips = attempts.flatMap((a, i) => a.skips.easy.map((e: any) => ({ ...e, mock: i + 1 })));
  const careless = attempts.flatMap((a, i) => a.careless.map((e: any) => ({ ...e, mock: i + 1 })));
  const lateSkips = attempts.reduce((t, a) => t + (a.timing.quarters?.[3]?.skipped || 0), 0);

  return (
    <article className="report-sheet mx-auto bg-white text-left" style={{ color: C.ink }}>
      <table className="w-full border-collapse">
        <tbody><tr><td className="p-0 align-top">

          {/* ── Cover band ── */}
          <header className="avoid-break overflow-hidden rounded-2xl px-7 pb-6 pt-6 text-white"
            style={{ background: `radial-gradient(120% 140% at 100% 0%, ${C.violet}55 0%, transparent 55%), linear-gradient(135deg, ${C.navy} 0%, #1E1A4D 100%)` }}>
            <div className="flex items-start justify-between gap-4">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/brand/bt-horizontal-white.svg" alt="Beyond Tutors" className="h-9 w-auto" />
              <div className="text-right text-[10.5px] leading-snug opacity-80">
                Generated {fmtDate(r.generated_at)}<br />Confidential · for {fname}&rsquo;s family
              </div>
            </div>
            <div className="mt-6 text-[11px] font-semibold uppercase tracking-[0.18em]" style={{ color: C.amber }}>
              {r.exam} Performance Analysis
            </div>
            <h1 className="mt-1 text-[30px] font-extrabold leading-tight">{name}</h1>
            <div className="mt-1 text-[12px] opacity-80">
              {s.mocks} timed mock{s.mocks === 1 ? "" : "s"} · {fmtDate(attempts[0]?.date)} – {fmtDate(latest?.date)}
              {r.target ? <> · Target: <b className="opacity-100">{r.target}</b></> : null}
            </div>
            {c.headline && (
              <p className="mt-4 max-w-[150mm] border-l-2 pl-3 text-[14px] font-medium leading-snug" style={{ borderColor: C.amber }}>{c.headline}</p>
            )}
          </header>

          {/* ── At a glance ── */}
          <div className="mt-4 grid grid-cols-5 gap-2">
            <Tile label={r.band?.unit === "module" ? "Est. band (per module)" : "Estimated band"} value={bandHeadline}
              note={r.band?.unit === "total" ? `range ${r.band.low.toFixed(1)}–${r.band.high.toFixed(1)}` : bandRows.map((b) => b.label).join(" · ")} accent={C.indigo} />
            <Tile label="Overall accuracy" value={pct(s.accuracy)} note={`${s.correct} of ${s.questions} questions`} />
            <Tile label="When attempted" value={pct(s.accuracy_attempted)} note="accuracy excl. skips" />
            <Tile label="Latest mock" value={pct(s.latest_score)} note={s.mocks > 1 ? `first mock ${pct(s.first_score)}` : shortTitle(latest?.title || "")} />
            <Tile label="Skipped" value={s.skip_data ? String(s.skipped) : "n/a"} note={s.skip_data ? `${pct((100 * s.skipped) / Math.max(1, s.questions))} of questions` : "older answers purged"} />
          </div>

          {c.overview && <div className="mt-4"><Prose>{c.overview}</Prose></div>}

          {/* ── 1. Where they stand ── */}
          {bandRows.length > 0 && (
            <>
              <SectionTitle n={1} title={`Where ${fname} stands on the ${r.exam} scale`}
                sub={r.band?.unit === "total" ? `Combined estimate from the latest Paper 1 + Paper 2 (${r.band.combined_marks}); official scale 1.0–9.0` : "Recency-weighted estimate per module; official scale 1.0–9.0"} />
              <div className="avoid-break rounded-xl border p-4" style={{ borderColor: C.line }}>
                <BandScale rows={bandRows} benchmarks={r.benchmarks} />
              </div>
              <Callout title="What this means">{c.band_commentary}</Callout>
            </>
          )}

          {/* ── 2. Results by section ── */}
          <SectionTitle n={2} title="Results by section & subject" sub={`All ${s.mocks} mock${s.mocks === 1 ? "" : "s"} combined, then mock by mock`} />
          <div className="avoid-break rounded-xl border p-4" style={{ borderColor: C.line }}>
            <div className="mb-2 flex items-center justify-between"><StatusLegend /><span className="text-[10px]" style={{ color: C.subtle }}>accuracy</span></div>
            <SectionBars sections={r.sections} />
          </div>
          {attempts.length > 1 && (
            <div className="avoid-break mt-3 rounded-xl border p-4" style={{ borderColor: C.line }}>
              <div className="mb-1 text-[11px] font-bold" style={{ color: C.ink }}>Accuracy trend by section</div>
              <TrendChart attempts={attempts} />
            </div>
          )}
          <div className="avoid-break mt-3 overflow-hidden rounded-xl border" style={{ borderColor: C.line }}>
            <table className="w-full text-[11px]">
              <thead style={{ background: C.wash, color: C.muted }}>
                <tr className="text-left">
                  <th className="px-3 py-2 font-semibold">Mock</th>
                  <th className="px-2 py-2 font-semibold">Date</th>
                  <th className="px-2 py-2 text-right font-semibold">Score</th>
                  <th className="px-2 py-2 text-right font-semibold">✓ / ✗ / –</th>
                  <th className="px-2 py-2 text-right font-semibold">Acc. when attempted</th>
                  <th className="px-2 py-2 text-right font-semibold">Time used</th>
                  <th className="px-3 py-2 text-right font-semibold">{r.exam === "TMUA" ? "Paper-equiv. band*" : "Module bands"}</th>
                </tr>
              </thead>
              <tbody>
                {attempts.map((a, i) => (
                  <tr key={a.attempt_id} className="border-t" style={{ borderColor: C.line }}>
                    <td className="px-3 py-1.5"><b>Mock {i + 1}</b> <span style={{ color: C.muted }}>{shortTitle(a.title)}</span></td>
                    <td className="px-2 py-1.5" style={{ color: C.muted }}>{shortDate(a.date)}</td>
                    <td className="px-2 py-1.5 text-right font-bold">{pct(a.score)}</td>
                    <td className="px-2 py-1.5 text-right">{a.correct} / {a.wrong} / {a.skipped}</td>
                    <td className="px-2 py-1.5 text-right">{pct(a.accuracy_attempted)}</td>
                    <td className="px-2 py-1.5 text-right">{mmss(a.timing.used_seconds)}{a.timing.allowed_seconds ? <span style={{ color: C.subtle }}> / {Math.round(a.timing.allowed_seconds / 60)}m</span> : null}</td>
                    <td className="px-3 py-1.5 text-right font-semibold" style={{ color: C.indigo }}>
                      {a.band != null ? a.band.toFixed(1) : a.sections.filter((x: any) => x.band != null).map((x: any) => `${x.section.replace("Maths", "M")} ${x.band.toFixed(1)}`).join(" · ") || "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* ── 3. Topics ── */}
          <SectionTitle n={3} title="Topic analysis — strengths & gaps" sub="Every question is tagged to a syllabus topic; ratings need at least 3 questions" />
          <div className="overflow-hidden rounded-xl border" style={{ borderColor: C.line }}>
            <table className="w-full text-[11px]">
              <thead style={{ background: C.wash, color: C.muted }}>
                <tr className="text-left">
                  <th className="px-3 py-2 font-semibold">Section</th>
                  <th className="px-2 py-2 font-semibold">Topic</th>
                  <th className="px-2 py-2 text-right font-semibold">Qs</th>
                  <th className="w-[34%] px-2 py-2 font-semibold">Accuracy</th>
                  <th className="px-2 py-2 text-right font-semibold">Skipped</th>
                  <th className="px-2 py-2 text-right font-semibold">Avg time</th>
                  <th className="px-3 py-2 text-right font-semibold">Rating</th>
                </tr>
              </thead>
              <tbody>
                {r.topics.map((t: any) => {
                  const rt = RATING[t.rating];
                  return (
                    <tr key={t.section + t.topic} className="avoid-break border-t" style={{ borderColor: C.line }}>
                      <td className="px-3 py-1.5" style={{ color: C.muted }}>{t.section}</td>
                      <td className="px-2 py-1.5 font-semibold">{t.topic}</td>
                      <td className="px-2 py-1.5 text-right">{t.n}</td>
                      <td className="px-2 py-1.5">
                        <div className="flex items-center gap-2">
                          <div className="h-2.5 flex-1 overflow-hidden rounded-full" style={{ background: C.wash }}>
                            <div className="h-full rounded-full" style={{ width: `${t.accuracy ?? 0}%`, background: C.indigo }} />
                          </div>
                          <b className="w-9 text-right">{pct(t.accuracy)}</b>
                        </div>
                      </td>
                      <td className="px-2 py-1.5 text-right">{t.skipped || "—"}</td>
                      <td className="whitespace-nowrap px-2 py-1.5 text-right">{mmss(t.avg_seconds)}</td>
                      <td className="px-3 py-1.5 text-right">
                        <span className="rounded-full px-2 py-0.5 text-[9.5px] font-bold" style={{ background: rt.bg, color: rt.fg }}>{rt.label}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          {(c.strengths?.length > 0) && (
            <div className="avoid-break mt-3 rounded-xl border px-4 py-3" style={{ borderColor: C.line }}>
              <div className="mb-1.5 text-[10px] font-bold uppercase tracking-wider" style={{ color: C.correct }}>Strengths to protect</div>
              <ul className="list-disc space-y-1 pl-4 text-[12px] leading-relaxed">
                {c.strengths.map((x: string, i: number) => <li key={i}>{x}</li>)}
              </ul>
            </div>
          )}

          {/* ── 4. Time ── */}
          <SectionTitle n={4} title="Time management" sub={timedLatest ? `Question-by-question timing from Mock ${attempts.indexOf(timedLatest) + 1} (${shortTitle(timedLatest.title)})` : "No per-question timing recorded"} />
          {timedLatest && (
            <>
              <div className="grid grid-cols-4 gap-2">
                <Tile label="Time used" value={mmss(timedLatest.timing.used_seconds)} note={timedLatest.timing.allowed_seconds ? `of ${Math.round(timedLatest.timing.allowed_seconds / 60)} min${timedLatest.timing.auto_submitted ? " · ran out of time" : ""}` : undefined} />
                <Tile label="Even pace" value={mmss(timedLatest.timing.pace_seconds)} note="per question" />
                <Tile label="Avg on correct" value={mmss(timedLatest.timing.avg_correct)} note={`wrong: ${mmss(timedLatest.timing.avg_wrong)}`} />
                <Tile label="Time on unscored Qs" value={mmss(timedLatest.timing.time_on_unscored)} note="wrong or skipped" accent={C.wrong} />
              </div>
              <div className="avoid-break mt-3 rounded-xl border p-4" style={{ borderColor: C.line }}>
                <div className="mb-2 flex items-center justify-between"><StatusLegend /><span className="text-[10px]" style={{ color: C.subtle }}>▲ = beyond the chart</span></div>
                <TimeStrip attempt={timedLatest} />
                {timedLatest.timing.quarters?.length === 4 && (
                  <div className="mt-2 grid grid-cols-4 gap-2">
                    {timedLatest.timing.quarters.map((q: any, i: number) => (
                      <div key={i} className="rounded-lg px-2.5 py-1.5 text-[10.5px]" style={{ background: C.wash }}>
                        <div className="font-bold" style={{ color: C.ink }}>{["1st", "2nd", "3rd", "Final"][i]} quarter <span className="font-normal" style={{ color: C.subtle }}>{q.label}</span></div>
                        <div style={{ color: C.muted }}><b style={{ color: C.ink }}>{pct(q.accuracy)}</b> correct · {q.skipped} skip · {q.avg_seconds}s/Q</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              {timedLatest.timing.sinks?.length > 0 && (
                <p className="mt-2 text-[11px]" style={{ color: C.muted }}>
                  <b style={{ color: C.ink }}>Time sinks</b> (≥1.75× pace, no mark):{" "}
                  {timedLatest.timing.sinks.map((q: any) => `Q${q.n} ${q.topic} (${mmss(q.seconds)})`).join(" · ")}
                </p>
              )}
            </>
          )}
          <Callout title="Timing insight">{c.timing}</Callout>

          {/* ── 5. Skips & accuracy ── */}
          <SectionTitle n={5} title="Skipping & accuracy" sub="No negative marking in this exam, so a blank never scores more than a guess" />
          <div className="grid grid-cols-4 gap-2">
            <Tile label="Questions skipped" value={s.skip_data ? String(totalSkips) : "n/a"} note={`across ${s.mocks} mock${s.mocks === 1 ? "" : "s"}`} />
            <Tile label="Skipped in final quarter" value={String(lateSkips)} note="last quarter of each paper" />
            <Tile label="Marks from guessing" value={`≈ ${guessValue.toFixed(1)}`} note="expected, had blanks been guessed" accent={C.indigo} />
            <Tile label="Slips on easier Qs" value={String(careless.length)} note="wrong where most get it right" accent={careless.length ? C.wrong : undefined} />
          </div>
          <div className="mt-3 grid grid-cols-2 gap-3">
            <div className="avoid-break rounded-xl border p-4" style={{ borderColor: C.line }}>
              <div className="mb-2.5 text-[11px] font-bold">Accuracy by question difficulty</div>
              {diffRows.length ? <MiniBars rows={diffRows} /> : <p className="text-[11px]" style={{ color: C.muted }}>Difficulty tags unavailable.</p>}
            </div>
            <div className="avoid-break rounded-xl border p-4 text-[11px] leading-relaxed" style={{ borderColor: C.line }}>
              <div className="mb-1.5 text-[11px] font-bold">Marks left on the table</div>
              {easySkips.length > 0 && <p><b>Skipped but accessible:</b> {easySkips.slice(0, 8).map((e) => `Mock ${e.mock} Q${e.n} (${e.topic})`).join(", ")}</p>}
              {careless.length > 0 && <p className="mt-1"><b>Likely slips:</b> {careless.slice(0, 8).map((e) => `Mock ${e.mock} Q${e.n} (${e.topic})`).join(", ")}</p>}
              {!easySkips.length && !careless.length && <p style={{ color: C.muted }}>No accessible skips or obvious slips detected.</p>}
            </div>
          </div>
          <Callout title="Skipping strategy">{c.skipping}</Callout>
          <Callout title="Accuracy">{c.accuracy}</Callout>

          {/* ── 6. Focus ── */}
          {(c.focus_areas?.length > 0) && (
            <>
              <SectionTitle n={6} title="Where the next marks will come from" sub="Ranked by marks recoverable — the highest-value fixes first" />
              <div className="space-y-2">
                {c.focus_areas.map((f: any, i: number) => (
                  <div key={i} className="avoid-break flex gap-3 rounded-xl border px-4 py-3" style={{ borderColor: C.line }}>
                    <span className="grid h-6 w-6 shrink-0 place-items-center rounded-full text-[11px] font-bold text-white" style={{ background: i === 0 ? C.amber : C.indigo }}>{i + 1}</span>
                    <div className="text-[12px] leading-relaxed">
                      <div className="font-bold" style={{ color: C.ink }}>{f.area}</div>
                      <div style={{ color: C.muted }}>{f.evidence}</div>
                      <div className="mt-0.5"><b style={{ color: C.indigo }}>What to change: </b>{f.action}</div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}

          {c.closing && (
            <div className="avoid-break mt-5 rounded-2xl px-5 py-4 text-white" style={{ background: `linear-gradient(135deg, ${C.indigo}, ${C.violet})` }}>
              <div className="text-[10px] font-bold uppercase tracking-wider" style={{ color: "#FDE68A" }}>Our expectation</div>
              <p className="mt-1 text-[13px] leading-relaxed">{c.closing}</p>
            </div>
          )}

          {adminCopy && (
            <div className="avoid-break mt-5 rounded-xl border border-dashed p-4 text-[11px]" style={{ borderColor: C.wrong }}>
              <div className="mb-1.5 font-bold" style={{ color: C.wrong }}>Admin copy only — exam integrity signals (do not share)</div>
              {attempts.map((a, i) => (
                <div key={a.attempt_id}>Mock {i + 1}: {a.integrity.focus_lost} tab switches · {mmss(a.integrity.time_away_seconds)} away · {a.integrity.paste_attempts} paste attempts · {a.integrity.fullscreen_exits} fullscreen exits{a.timing.auto_submitted ? " · auto-submitted" : ""}</div>
              ))}
            </div>
          )}

          <p className="avoid-break mt-5 text-[9.5px] leading-snug" style={{ color: C.subtle }}>
            <b>How to read this report.</b> Mocks are original Beyond Tutors papers written to the {r.exam} specification, not past papers,
            so bands are indicative estimates shown as a ±0.5 range. Raw marks are mapped to the official 1.0–9.0 scale using published
            conversion data and public score distributions{r.exam === "TMUA" ? " (TMUA: 2023 conversion + Oct 2025 percentiles; *paper-equivalent = one paper scored as if it were the whole test)" : r.exam === "ESAT" ? " (ESAT: 2024–25 module distributions; typical candidate ≈ 4.5)" : ""}.
            Universities do not publish cut-offs. Topic tags and difficulty are assigned per question; group comparisons use every student who sat the same paper.
          </p>

        </td></tr></tbody>
        <tfoot className="report-foot-spacer"><tr><td><div /></td></tr></tfoot>
      </table>

      {/* Fixed on every printed page; at the end of the sheet on screen. */}
      <footer className="report-footer">
        <div className="flex items-center gap-2">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/brand/bt-icon-color.svg" alt="" className="h-5 w-5" />
          <div className="leading-tight">
            <div className="text-[9.5px] font-bold" style={{ color: C.ink }}>Beyond Tutors</div>
            <div className="whitespace-nowrap text-[8.5px]" style={{ color: C.subtle }}>{name} · {r.exam} analysis</div>
          </div>
        </div>
        <div className="flex flex-wrap items-center justify-end gap-x-3 gap-y-0.5">
          <span className="text-[8.5px] font-semibold uppercase tracking-wider" style={{ color: C.violet }}>Follow us</span>
          {SOCIALS.map(({ icon: Icon, label, href }) => (
            <a key={href} href={href} className="inline-flex items-center gap-1 text-[8.5px] no-underline" style={{ color: C.muted }}>
              <Icon size={10} strokeWidth={2.2} color={C.indigo} />{label}
            </a>
          ))}
        </div>
      </footer>
    </article>
  );
}
