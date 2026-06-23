import axios from "axios";

const API_BASE = typeof window !== "undefined" && window.location.hostname !== "localhost"
  ? "/api"
  : "http://localhost:8000";

export const api = axios.create({ baseURL: API_BASE, headers: { "Content-Type": "application/json" } });

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
      window.location.href = "/login";
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
  create: (data: object) => api.post("/quiz/create", data),
  submit: (data: object) => api.post("/quiz/submit", data),
  history: () => api.get("/quiz/history"),
  result: (id: string) => api.get(`/quiz/result/${id}`),
};

export const progressAPI = {
  dashboard: () => api.get("/progress/dashboard"),
  srsdue: () => api.get("/progress/srs-due"),
};

export const paymentsAPI = {
  plans: () => api.get("/payments/plans"),
  createCheckout: (plan: string) => api.post("/payments/create-checkout", { plan }),
};
