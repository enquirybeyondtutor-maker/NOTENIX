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
    copy_attempts?: number; fullscreen_exits?: number; burst_flags?: number;
  }) => api.post(`/tests/${assignmentId}/submit`, data),
  start: (assignmentId: number | string) => api.post(`/tests/${assignmentId}/start`),
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
  resetTimer: (assignmentId: number | string) => api.post(`/teacher/assignments/${assignmentId}/reset-timer`),
  setExcluded: (attemptId: number | string, excluded: boolean) =>
    api.post(`/teacher/attempts/${attemptId}/exclude`, { excluded }),
};

export const reportsAPI = {
  candidates: () => api.get("/reports/candidates"),
  // Building runs as a background job (topic tagging + commentary take longer than the proxy allows).
  startBuild: (data: { student_id: number; exam: string; attempt_ids?: number[]; target?: string; pronouns?: string; commentary?: boolean }) =>
    api.post("/reports/jobs", data),
  job: (jobId: string) => api.get(`/reports/jobs/${jobId}`),
};

export const adminAPI = {
  overview: () => api.get("/admin/overview"),
  users: () => api.get("/admin/users"),
  ban: (id: number | string) => api.post(`/admin/users/${id}/ban`),
  unban: (id: number | string) => api.post(`/admin/users/${id}/unban`),
  setRole: (id: number | string, role: string) => api.post(`/admin/users/${id}/role`, { role }),
  setWriteAccess: (id: number | string, enabled: boolean) =>
    api.post(`/admin/users/${id}/write-access`, { enabled }),
  // Beyond Tutors-issued accounts: the password comes back once, in the response.
  suggestId: (name: string) => api.get("/admin/suggest-id", { params: { name } }),
  createUser: (data: { full_name: string; email?: string; role: "student" | "teacher"; access: "trial" | "year" | "none" }) =>
    api.post("/admin/users", data),
  resetPassword: (id: number | string) => api.post(`/admin/users/${id}/reset-password`),
  setAccess: (id: number | string, access: "trial" | "year" | "none") =>
    api.post(`/admin/users/${id}/access`, { access }),
};

// Class notes: teachers share text and/or a PDF/image with students.
export const notesAPI = {
  mine: () => api.get("/notes"),
  get: (id: number | string) => api.get(`/notes/${id}`),
  teacherList: () => api.get("/teacher/notes"),
  create: (data: { title: string; subject?: string; body?: string; file_name?: string; file_data?: string; student_emails: string[] }) =>
    api.post("/teacher/notes", data),
  share: (id: number, student_emails: string[]) => api.post(`/teacher/notes/${id}/share`, { student_emails }),
  unshare: (id: number, studentId: number) => api.delete(`/teacher/notes/${id}/share/${studentId}`),
  remove: (id: number) => api.delete(`/teacher/notes/${id}`),
};

// Revision papers: page 1 public, full paper needs live access (app/papers/[slug]).
export const papersAPI = {
  info: (slug: string) => api.get(`/papers/${slug}`),
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
// Manual bank-transfer payments (Wise etc.): the student pays, then an admin confirms.
export const paymentsAPI = {
  plans: () => api.get("/payments/plans"),
  accounts: () => api.get("/payments/accounts"),
  claim: (data: { purpose: "pro" | "test_request"; request_id?: number; paid_via?: string; payer_name?: string; payer_note?: string }) =>
    api.post("/payments/claim", data),
  mine: () => api.get("/payments/mine"),
  revisionInfo: () => api.get("/payments/revision-checkout"),
  revisionCheckout: (data: { full_name: string; email: string; password: string; paid_via?: string; payer_name?: string; payer_note?: string }) =>
    api.post("/payments/revision-checkout", data),
  adminList: (status?: string) => api.get("/payments/admin", { params: status ? { status } : {} }),
  review: (id: number, approve: boolean) => api.post(`/payments/admin/${id}/review`, { approve }),
};

// Request-a-test service: student requests → team assigns a test → team marks it.
export const requestsAPI = {
  config: () => api.get("/requests/config"),
  create: (data: { exam: string; subject?: string; details?: string; preferred_date?: string | null }) =>
    api.post("/requests", data),
  guest: (data: { full_name: string; email: string; whatsapp: string; password: string; exam: string;
                  subject?: string; details?: string; preferred_date?: string | null }) =>
    api.post("/requests/guest", data),
  mine: () => api.get("/requests/mine"),
  cancel: (id: number) => api.post(`/requests/${id}/cancel`),
  adminList: () => api.get("/requests/admin"),
  adminTests: () => api.get("/requests/admin/tests"),
  assign: (id: number, data: { test_id: number; due_at?: string | null; note?: string }) =>
    api.post(`/requests/admin/${id}/assign`, data),
  update: (id: number, data: { status?: "open" | "cancelled"; note?: string }) =>
    api.post(`/requests/admin/${id}`, data),
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
