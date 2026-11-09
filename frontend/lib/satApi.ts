import { api } from "@/lib/api";

// Notenix SAT (backend routers/sat.py, services/sat.py).

export type SatQuestion = {
  id: string; section: "rw" | "math"; domain: string; skill: string; difficulty: number;
  type: "mcq" | "spr"; passage?: string; question: string; options?: string[];
};
export type SatModule = { key: string; title: string; section: "rw" | "math"; minutes: number; questions: SatQuestion[] };
export type ReviewQuestion = SatQuestion & { answer: string | string[]; explanation: string; given: string | null; correct: boolean };
export type SkillRow = { section: "rw" | "math"; domain: string; skill: string; right: number; total: number };
export type Price = { currency: string; amount: number; label: string };

export const satAPI = {
  diagnostic: () => api.get<{ title: string; modules: SatModule[] }>("/sat/diagnostic"),
  scoreDiagnostic: (answers: Record<string, string>) => api.post("/sat/diagnostic/score", { answers }),
  price: (currency: string) => api.get<Price>("/sat/price", { params: { currency } }),
  trialStart: (data: { full_name: string; email: string; parent_email?: string; test_date?: string; target?: number; currency?: string; agree_terms: boolean }) =>
    api.post("/sat/trial/start", data),
  trialVerify: (email: string, code: string) => api.post("/sat/trial/verify", { email, code }),
  trialComplete: (data: { email: string; setup_token: string; password: string; diagnostic_answers?: Record<string, string> }) =>
    api.post("/sat/trial/complete", data),
  home: () => api.get("/sat/home"),
  setGoal: (data: { test_date?: string | null; target?: number | null }) => api.post("/sat/goal", data),
  start: (slug: string) => api.post(`/sat/forms/${slug}/start`),
  attempt: (id: number | string, openModule = false) => api.get(`/sat/attempts/${id}`, { params: openModule ? { open_module: true } : {} }),
  save: (id: number | string, data: { module: string; answers: Record<string, string>; marked: string[] }) => api.put(`/sat/attempts/${id}/save`, data),
  submit: (id: number | string, data: { module: string; answers: Record<string, string>; marked: string[] }) => api.post(`/sat/attempts/${id}/submit`, data),
  result: (id: number | string) => api.get(`/sat/attempts/${id}/result`),
  // Phase 2
  skills: () => api.get<SkillStatus[]>("/sat/skills"),
  plan: () => api.get<StudyPlan>("/sat/plan"),
  drill: (slug: string) => api.get(`/sat/drills/${slug}`),
  drillAnswer: (slug: string, question_id: string, answer: string) =>
    api.post<{ correct: boolean; answer: string | string[]; explanation: string }>(`/sat/drills/${slug}/answer`, { question_id, answer }),
};

export type SkillStatus = {
  slug: string; skill: string; domain: string; section: "rw" | "math"; about: string;
  right: number; total: number; accuracy: number | null; status: "strong" | "building" | "weak" | "untried";
};
export type PlanTask = { kind: "drill" | "mock"; title: string; detail: string; href: string; done: boolean; progress: string };
export type StudyPlan = {
  test_date: string | null; days_left: number | null; target: number | null;
  tasks: PlanTask[]; weeks: { week_of: string; items: string[]; current: boolean }[]; focus: SkillStatus[];
};

/** Billing currency for a visitor's country (SAT prices: services/pricing.SAT_PRICES). */
export function satCurrency(country: string): string {
  const map: Record<string, string> = { IN: "INR", AE: "AED", GB: "GBP", SG: "SGD", AU: "AUD", NZ: "NZD", CA: "CAD", US: "USD" };
  const eu = ["AT", "BE", "CY", "DE", "EE", "ES", "FI", "FR", "GR", "HR", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PT", "SI", "SK"];
  if (map[country]) return map[country];
  return eu.includes(country) ? "EUR" : "USD";
}

export const SAT_DOMAINS: Record<"rw" | "math", string[]> = {
  rw: ["Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"],
  math: ["Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"],
};
