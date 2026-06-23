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
  register: (data: { email: string; password: string; full_name: string }) => api.post("/auth/register", data),
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
