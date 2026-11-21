import type { Metadata } from "next";
import { SITE } from "@/lib/site";

const title = "TMUA Mock Series for January 2027: 10 Full Computer-Based Mocks";
const description =
  "10 full TMUA mocks before the 4–8 January 2027 test, on screen and timed like the real thing, plus a Baseline Mock, " +
  "rankings, worked solutions and topic sets on request. £99 if you enrol by 24 November, then £109.";

export const metadata: Metadata = {
  title,
  description,
  alternates: { canonical: `${SITE}/tmua-mocks` },
  openGraph: { type: "website", url: `${SITE}/tmua-mocks`, siteName: "Notenix", title, description },
  twitter: { card: "summary_large_image", title, description },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
