import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Analytics from "@/components/Analytics";
import Shell from "@/components/Shell";
import CookieConsent from "@/components/CookieConsent";
import { SITE } from "@/lib/site";

const inter = Inter({ subsets: ["latin"], display: "swap", variable: "--font-inter" });

const GA_ID = process.env.NEXT_PUBLIC_GA_ID || "G-6NVHXT86PC"; // GA4 Measurement ID (env var overrides)

export const metadata: Metadata = {
  metadataBase: new URL(SITE),
  title: {
    default: "Notenix: Free Practice Tests Marked by Tutors (SAT, ESAT, TMUA, IGCSE, GCSE, A-Level)",
    template: "%s | Notenix",
  },
  description:
    "Free practice tests for SAT, ESAT, TMUA, GCSE, IGCSE, A-Level, HSC, VCE, QCE, WACE and NCEA. Sit timed mocks online, get instant marking, or request a full mock marked by real tutors. Students anywhere can start free.",
  keywords: [
    "Notenix", "notenix", "SAT practice test", "digital SAT practice", "free SAT mock", "ESAT practice",
    "ESAT mock test", "TMUA practice", "TMUA mock", "IGCSE practice test", "HSC practice test", "VCE practice exam", "QCE practice exam", "WACE practice exam", "NCEA practice exam",
    "GCSE quiz", "A-Level quiz", "past papers", "GCSE revision",
    "A-Level revision", "exam practice", "AQA", "Edexcel", "OCR", "GCSE past papers",
    "A-Level past papers", "online quiz platform", "Beyond Groups", "Beyond Tutors",
  ],
  authors: [{ name: "Beyond Groups" }],
  creator: "Beyond Groups",
  publisher: "Beyond Groups",
  applicationName: "Notenix",
  openGraph: {
    type: "website",
    url: SITE,
    siteName: "Notenix",
    title: "Notenix — SAT, ESAT, TMUA, GCSE & A-Level Practice Tests",
    description:
      "Timed practice tests with instant marking, plus full mocks marked by real tutors. SAT, ESAT, TMUA, GCSE and A-Level. Start free.",
    locale: "en_GB",
  },
  twitter: {
    card: "summary_large_image",
    title: "Notenix — SAT, ESAT, TMUA, GCSE & A-Level Practice Tests",
    description: "Timed practice tests with instant marking, plus full mocks marked by real tutors. Start free.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large", "max-snippet": -1 },
  },
  category: "education",
};

const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": `${SITE}/#org`,
      name: "Notenix",
      url: SITE,
      description: "Online practice-test platform for SAT, ESAT, TMUA, GCSE, A-Level, IGCSE, HSC, VCE, QCE, WACE and NCEA, with mocks marked by tutors from Beyond Tutors.",
      logo: `${SITE}/icon.svg`,
      email: "support@notenix.com",
      contactPoint: { "@type": "ContactPoint", contactType: "customer support", email: "support@notenix.com" },
      parentOrganization: { "@type": "Organization", name: "Beyond Groups" },
      sameAs: [
        "https://www.thebeyondtutors.com",
        "https://www.youtube.com/@thebeyondtutors",
      ],
    },
    {
      "@type": "WebSite",
      "@id": `${SITE}/#website`,
      url: SITE,
      name: "Notenix",
      publisher: { "@id": `${SITE}/#org` },
      inLanguage: "en",
    },
    {
      "@type": "WebApplication",
      name: "Notenix",
      url: SITE,
      applicationCategory: "EducationalApplication",
      operatingSystem: "Web",
      offers: [
        { "@type": "Offer", price: "0", priceCurrency: "GBP", name: "Free practice" },
        { "@type": "Offer", price: "49", priceCurrency: "GBP", name: "Beyond Tutors students: 1 year", url: `${SITE}/pricing` },
        { "@type": "Offer", price: "149", priceCurrency: "GBP", name: "Revision access for all other students: 1 year", url: `${SITE}/revision/checkout` },
      ],
    },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-GB" className={inter.variable}>
      <head>
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      </head>
      <body className="min-h-screen bg-canvas text-ink antialiased">
        <Shell>{children}</Shell>

        {/* Google Analytics 4: the script only downloads after the visitor accepts cookies. */}
        {GA_ID && <Analytics gaId={GA_ID} />}
        <CookieConsent />
      </body>
    </html>
  );
}
