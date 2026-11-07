// Doubt Help / Ask a Tutor (backend routers/doubt.py). Kept apart from lib/api.ts on purpose.
import { api } from "@/lib/api";

export type DoubtPlan = { plan: "annual" | "doubt" | "plus"; name: string; label: string; currency: string; amount: number; cap: number; calls: number };

export const doubtAPI = {
  plans: (currency = "SGD") => api.get("/doubt/plans", { params: { currency } }),
  startTrial: (data: { child_name: string; level: string; parent_email: string; agree_terms: boolean }) => api.post("/doubt/trial/start", data),
  verifyTrial: (data: { parent_email: string; code: string }) => api.post("/doubt/trial/verify", data),
  completeTrial: (data: { parent_email: string; setup_token: string; password: string }) => api.post("/doubt/trial/complete", data),
  checkoutInfo: () => api.get("/doubt/checkout"),
  checkout: (data: { login_id: string; password: string; plan: string; currency: string; paid_via?: string; payer_name?: string; payer_note?: string }) =>
    api.post("/doubt/checkout", data),
  adminSet: (id: number | string, data: { plan: string | null; level?: string | null; days?: number }) => api.post(`/doubt/admin/users/${id}`, data),
};

export const SG_LEVELS = ["Sec 1", "Sec 2", "Sec 3", "Sec 4", "Sec 5", "JC 1", "JC 2"];
