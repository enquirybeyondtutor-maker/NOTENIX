import type { Metadata } from "next";

// For signed-in pages: keep them out of search results.
export const privatePage = (title: string): Metadata => ({ title, robots: { index: false, follow: false } });
