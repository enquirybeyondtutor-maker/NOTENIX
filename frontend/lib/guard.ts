"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getUser, authAPI } from "./api";

type Role = "student" | "teacher" | "admin";

/**
 * Client-side auth guard. Redirects to /login if no session.
 * If `requireRole` is set and the user's role doesn't match, redirects them
 * to their correct home. Returns { user, ready }.
 */
export function useAuthGuard(requireRole?: "student" | "teacher") {
  const router = useRouter();
  const [user, setUser] = useState<any | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("notenix_token") : null;
    if (!token) {
      router.replace("/login");
      return;
    }
    const cached = getUser();
    if (cached) setUser(cached);

    authAPI
      .me()
      .then(({ data }) => {
        try {
          localStorage.setItem("notenix_user", JSON.stringify(data));
        } catch {}
        setUser(data);
        const role: Role = data.role || "student";
        if (requireRole === "teacher" && role === "student") {
          router.replace("/dashboard");
          return;
        }
        if (requireRole === "student" && (role === "teacher" || role === "admin")) {
          router.replace("/teacher");
          return;
        }
        setReady(true);
      })
      .catch(() => {
        // Token invalid/expired — interceptor handles 401 redirect.
        setReady(true);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { user, ready };
}
