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
  forgotPassword: (email: string) => api.post("/auth/forgot-password", { email }),
  resetPassword: (email: string, code: string, new_password: string) =>
    api.post("/auth/reset-password", { email, code, new_password }),
  login: (email: string, password: string) =>
    api.post("/auth/login", new URLSearchParams({ username: email, password }), {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }),
  me: () => api.get("/auth/me"),
  updateProfile: (full_name: string) => api.patch("/auth/profile", { full_name }),
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
  submit: (assignmentId: number | string, data: {
    answers: any[]; answer_images?: string[][]; time_taken_seconds?: number; question_times?: number[];
    focus_lost_count?: number; time_away_seconds?: number; paste_attempts?: number;
  }) => api.post(`/tests/${assignmentId}/submit`, data),
  saveDraft: (assignmentId: number | string, answers: any[]) =>
    api.post(`/tests/${assignmentId}/draft`, { answers }),
  result: (assignmentId: number | string) => api.get(`/tests/${assignmentId}/result`),
  join: (token: string) => api.post(`/tests/join/${token}`),
};

export const teacherAPI = {
  overview: () => api.get("/teacher/overview"),
  listTests: () => api.get("/teacher/tests"),
  createTest: (data: object) => api.post("/teacher/tests", data),
  createFromPdf: (formData: FormData) =>
    api.post("/teacher/tests/from-pdf", formData, { headers: { "Content-Type": "multipart/form-data" } }),
  createPhotoQuestions: (data: {
    title?: string; subject: string; topic?: string; level: string; exam_board?: string;
    marks_per_question: number; images: string[]; kind?: string; is_library?: boolean;
  }) => api.post("/teacher/tests/photo-questions", data),
  testDetail: (id: number | string) => api.get(`/teacher/tests/${id}`),
  testFull: (id: number | string) => api.get(`/teacher/tests/${id}/full`),
  updateTest: (id: number | string, data: object) => api.put(`/teacher/tests/${id}`, data),
  deleteTest: (id: number | string) => api.delete(`/teacher/tests/${id}`),
  assign: (id: number | string, data: { student_emails: string[]; class_label?: string; due_at?: string | null }) =>
    api.post(`/teacher/tests/${id}/assign`, data),
  share: (id: number | string) => api.post(`/teacher/tests/${id}/share`),
  unshare: (id: number | string) => api.delete(`/teacher/tests/${id}/share`),
  students: () => api.get("/teacher/students"),
  aiCheck: (attemptId: number | string) => api.post(`/teacher/attempts/${attemptId}/ai-check`),
};

export const adminAPI = {
  overview: () => api.get("/admin/overview"),
  users: () => api.get("/admin/users"),
  ban: (id: number | string) => api.post(`/admin/users/${id}/ban`),
  unban: (id: number | string) => api.post(`/admin/users/${id}/unban`),
  setRole: (id: number | string, role: string) => api.post(`/admin/users/${id}/role`, { role }),
  setWriteAccess: (id: number | string, enabled: boolean) =>
    api.post(`/admin/users/${id}/write-access`, { enabled }),
};

// Student written-answer practice (library + upload your own past paper).
export const practiceAPI = {
  library: () => api.get("/practice/library"),
  startLibrary: (testId: number | string) => api.post(`/practice/library/${testId}/start`),
  uploadPaper: (formData: FormData) =>
    api.post("/practice/upload", formData, { headers: { "Content-Type": "multipart/form-data" } }),
};

// Teacher/admin manual marking of written answers.
export const markingAPI = {
  queue: () => api.get("/marking/queue"),
  get: (attemptId: number | string) => api.get(`/marking/${attemptId}`),
  submit: (attemptId: number | string, marks: { marks_awarded: number; feedback?: string; model_answer?: string }[]) =>
    api.post(`/marking/${attemptId}`, { marks }),
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
