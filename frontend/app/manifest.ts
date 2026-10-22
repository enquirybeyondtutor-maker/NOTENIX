import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Notenix: Practice Tests Marked by Tutors",
    short_name: "Notenix",
    description: "SAT, ESAT, TMUA, IGCSE, GCSE, A-Level, CBSE, ICSE, JEE and NEET practice tests. By Beyond Imagination.",
    start_url: "/",
    display: "standalone",
    background_color: "#F5F3FF",
    theme_color: "#7C3AED",
    icons: [{ src: "/icon.svg", sizes: "any", type: "image/svg+xml" }],
  };
}
