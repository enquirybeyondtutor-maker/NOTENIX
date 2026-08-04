import axios from "axios";

// All requests go to /api/* which Next.js rewrites to the Render backend (same-origin, no CORS).
export const api = axios.create({ baseURL: "/api", headers: { "Content-Type": "application/json" } });

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("notenix_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("notenix_token");
      localStorage.removeItem("notenix_user");
      if (!window.location.pathname.startsWith("/login")) window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export const authAPI = {
  // Returns { status: "otp_sent", email, dev_otp? } — a verification code is emailed, no token yet.
  register: (data: { email: string; password: string; full_name: string; role?: string }) =>
    api.post("/auth/register", data),
  verifyOtp: (email: string, code: string) => api.post("/auth/verify-otp", { email, code }),
  resendOtp: (email: string) => api.post("/auth/resend-otp", { email }),
  login: (email: string, password: string) =>
    api.post("/auth/login", new URLSearchParams({ username: email, password }), {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }),
  me: () => api.get("/auth/me"),
};

export const quizAPI = {
  subjects: () => api.get("/quiz/subjects"),
  create: (data: object) => api.post("/quiz/create", data),
  submit: (data: object) => api.post("/quiz/submit", data),
  history: () => api.get("/quiz/history"),
};

export const testsAPI = {
  mine: () => api.get("/tests"),
  get: (assignmentId: number | string) => api.get(`/tests/${assignmentId}`),
  submit: (assignmentId: number | string, data: { answers: any[]; time_taken_seconds?: number }) =>
    api.post(`/tests/${assignmentId}/submit`, data),
  result: (assignmentId: number | string) => api.get(`/tests/${assignmentId}/result`),
  join: (token: string) => api.post(`/tests/join/${token}`),
};

export const teacherAPI = {
  overview: () => api.get("/teacher/overview"),
  listTests: () => api.get("/teacher/tests"),
  createTest: (data: object) => api.post("/teacher/tests", data),
  createFromPdf: (formData: FormData) =>
    api.post("/teacher/tests/from-pdf", formData, { headers: { "Content-Type": "multipart/form-data" } }),
  testDetail: (id: number | string) => api.get(`/teacher/tests/${id}`),
  testFull: (id: number | string) => api.get(`/teacher/tests/${id}/full`),
  updateTest: (id: number | string, data: object) => api.put(`/teacher/tests/${id}`, data),
  deleteTest: (id: number | string) => api.delete(`/teacher/tests/${id}`),
  assign: (id: number | string, data: { student_emails: string[]; class_label?: string; due_at?: string | null }) =>
    api.post(`/teacher/tests/${id}/assign`, data),
  share: (id: number | string) => api.post(`/teacher/tests/${id}/share`),
  unshare: (id: number | string) => api.delete(`/teacher/tests/${id}/share`),
  students: () => api.get("/teacher/students"),
};

export const adminAPI = {
  overview: () => api.get("/admin/overview"),
  users: () => api.get("/admin/users"),
  ban: (id: number | string) => api.post(`/admin/users/${id}/ban`),
  unban: (id: number | string) => api.post(`/admin/users/${id}/unban`),
  setRole: (id: number | string, role: string) => api.post(`/admin/users/${id}/role`, { role }),
};

export const progressAPI = { dashboard: () => api.get("/progress/dashboard") };
export const leaderboardAPI = {
  global: () => api.get("/leaderboard/global"),
  weekly: () => api.get("/leaderboard/weekly"),
};
export const paymentsAPI = {
  plans: () => api.get("/payments/plans"),
  checkout: () => api.post("/payments/create-checkout"),
};

export function saveAuth(token: string, user: object) {
  localStorage.setItem("notenix_token", token);
  localStorage.setItem("notenix_user", JSON.stringify(user));
}
export function getUser(): any | null {
  if (typeof window === "undefined") return null;
  const u = localStorage.getItem("notenix_user");
  return u ? JSON.parse(u) : null;
}
export function logout() {
  localStorage.removeItem("notenix_token");
  localStorage.removeItem("notenix_user");
  window.location.href = "/";
}
