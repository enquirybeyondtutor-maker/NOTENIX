import { api } from "@/lib/api";
import type { SatModule, ReviewQuestion, PlanTask } from "@/lib/satApi";

// Notenix exam engine (backend routers/exam.py, services/exams.py): TMUA now, more exams later.
// SAT keeps its own adaptive engine (lib/satApi.ts).

/** Exams that have the engine: practice tests, diagnostic, skill map, plan and drills. */
export const ENGINE_EXAMS = ["tmua"] as const;
export const hasEngine = (slug: string) => (ENGINE_EXAMS as readonly string[]).includes(slug);

export type ExamInfo = {
  exam: string; name: string; full_name: string; sections: Record<string, string>;
  domains: Record<string, string[]>; scale: { min: number; max: number; decimals: number };
  calculator: boolean; mock_detail: string; about_score: string; has_diagnostic: boolean; mocks: number;
};
export type ExamSkillRow = { domain: string; skill: string; right: number; total: number };
export type ExamSection = { right: number; total: number; score: number; band?: [number, number] };
export type ExamReport = {
  sections: Record<string, ExamSection>; right: number; total: number; score: number; band?: [number, number];
  skills: ExamSkillRow[]; weakest: ExamSkillRow[];
  modules: { key: string; title: string; section: string; questions: ReviewQuestion[] }[];
};
export type ExamSkill = {
  slug: string; skill: string; domain: string; about: string; has_drill: boolean;
  right: number; total: number; accuracy: number | null; status: "strong" | "building" | "weak" | "untried";
};
export type ExamPlan = {
  test_date: string | null; days_left: number | null; target: number | null;
  tasks: PlanTask[]; weeks: { week_of: string; items: string[]; current: boolean }[]; focus: ExamSkill[];
};
export type Answers = { module: string; answers: Record<string, string>; marked: string[] };

export const examAPI = {
  info: (exam: string) => api.get<ExamInfo>(`/exam/${exam}/info`),
  diagnostic: (exam: string) => api.get<{ title: string; modules: SatModule[] }>(`/exam/${exam}/diagnostic`),
  scoreDiagnostic: (exam: string, answers: Record<string, string>) => api.post<ExamReport>(`/exam/${exam}/diagnostic/score`, { answers }),
  saveDiagnostic: (exam: string, answers: Record<string, string>) => api.post(`/exam/${exam}/diagnostic/save`, { answers }),
  home: (exam: string) => api.get(`/exam/${exam}/home`),
  setGoal: (exam: string, data: { test_date?: string | null; target?: number | null }) => api.post(`/exam/${exam}/goal`, data),
  start: (exam: string, slug: string) => api.post(`/exam/${exam}/forms/${slug}/start`),
  attempt: (id: number | string, openModule = false) => api.get(`/exam/attempts/${id}`, { params: openModule ? { open_module: true } : {} }),
  save: (id: number | string, data: Answers) => api.put(`/exam/attempts/${id}/save`, data),
  submit: (id: number | string, data: Answers) => api.post(`/exam/attempts/${id}/submit`, data),
  result: (id: number | string) => api.get(`/exam/attempts/${id}/result`),
  skills: (exam: string) => api.get<ExamSkill[]>(`/exam/${exam}/skills`),
  plan: (exam: string) => api.get<ExamPlan>(`/exam/${exam}/plan`),
  drill: (exam: string, slug: string) => api.get(`/exam/${exam}/drills/${slug}`),
  drillAnswer: (exam: string, slug: string, question_id: string, answer: string) =>
    api.post<{ correct: boolean; answer: string | string[]; explanation: string }>(`/exam/${exam}/drills/${slug}/answer`, { question_id, answer }),
};

/** A score on the exam's scale, e.g. 6.4 for TMUA. */
export const fmt = (n: number | null | undefined, info?: { scale: { decimals: number } } | null) =>
  n === null || n === undefined ? "–" : n.toFixed(info?.scale.decimals ?? 1);

/** Where a diagnostic taken before signing in waits to be saved to the account. */
export const diagKey = (exam: string) => `notenix_${exam}_diag`;
