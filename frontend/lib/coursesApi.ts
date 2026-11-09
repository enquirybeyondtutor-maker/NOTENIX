import { api } from "@/lib/api";

// Per-course access (backend services/courses.py). A course is a whole admissions test
// ("tmua") or a curriculum + subject ("igcse-chemistry").

export type Course = { key: string; name: string; group: string };
export type Enrolment = { course: string; name: string; kind: "trial" | "paid"; until: string | null; live: boolean };
export type Price = { currency: string; amount: number; label: string };

export const coursesAPI = {
  catalogue: () => api.get<Course[]>("/courses/catalogue"),
  mine: () => api.get<{ restricted: boolean; courses: Enrolment[]; pending: string[]; price: Price }>("/courses/mine"),
  buy: (data: { course: string; paid_via?: string; payer_name?: string; payer_note?: string }) => api.post("/courses/buy", data),
  // admin
  add: (userId: number, course: string, access: "trial" | "year" | "none") =>
    api.post(`/admin/users/${userId}/courses`, { course, access }),
  remove: (userId: number, course: string) => api.delete(`/admin/users/${userId}/courses/${course}`),
  suggestions: () => api.get("/admin/courses/suggestions"),
  apply: (items: { user_id: number; courses: string[] }[]) => api.post("/admin/courses/apply", { items }),
  createUser: (data: { full_name: string; email?: string; role: "student" | "teacher"; access: "trial" | "year" | "none"; currency?: string; courses: string[] }) =>
    api.post("/admin/users", data),
};

/** Group a catalogue for <optgroup>s, keeping the server's order. */
export function grouped(list: Course[]): [string, Course[]][] {
  const m = new Map<string, Course[]>();
  for (const c of list) m.set(c.group, [...(m.get(c.group) ?? []), c]);
  return [...m.entries()];
}
