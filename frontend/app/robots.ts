import type { MetadataRoute } from "next";
import { SITE } from "@/lib/site";

// Signed-in areas: nothing useful for search engines, and every page needs a session.
const PRIVATE = [
  "/dashboard", "/quiz", "/progress", "/tests", "/homework", "/practice", "/marking",
  "/settings", "/teacher", "/admin", "/join", "/requests", "/pay", "/verify-email", "/reset-password",
];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/", disallow: PRIVATE },
    sitemap: `${SITE}/sitemap.xml`,
    host: SITE,
  };
}
