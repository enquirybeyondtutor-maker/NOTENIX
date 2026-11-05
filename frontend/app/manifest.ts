import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Notenix: Practice Tests Marked by Tutors",
    short_name: "Notenix",
    description: "SAT, ESAT, TMUA, IGCSE, GCSE, A-Level, HSC, VCE, QCE, WACE and NCEA practice tests. By Beyond Groups.",
    start_url: "/",
    display: "standalone",
    background_color: "#FFFFFF",
    theme_color: "#5444DC",
    icons: [{ src: "/icon.svg", sizes: "any", type: "image/svg+xml" }],
  };
}
