import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Notenix — Smart GCSE & A-Level Quiz Platform",
    short_name: "Notenix",
    description: "Smart quizzes built on real GCSE & A-Level past papers. By Beyond Imagination.",
    start_url: "/",
    display: "standalone",
    background_color: "#F5F3FF",
    theme_color: "#7C3AED",
    icons: [{ src: "/icon.svg", sizes: "any", type: "image/svg+xml" }],
  };
}
