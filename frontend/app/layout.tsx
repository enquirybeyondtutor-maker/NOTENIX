import "./globals.css";
import type { Metadata } from "next";
import Script from "next/script";
import Shell from "@/components/Shell";

const SITE = "https://notenix.com";
const GA_ID = process.env.NEXT_PUBLIC_GA_ID; // GA4 Measurement ID, e.g. G-XXXXXXXXXX

export const metadata: Metadata = {
  metadataBase: new URL(SITE),
  title: {
    default: "Notenix — Smart GCSE & A-Level Quiz & Past Paper Practice",
    template: "%s | Notenix",
  },
  description:
    "Notenix helps UK students ace GCSE & A-Level exams with smart quizzes built on real past papers, instant marking, progress tracking and leaderboards. Start free.",
  keywords: [
    "Notenix", "notenix", "GCSE quiz", "A-Level quiz", "past papers", "GCSE revision",
    "A-Level revision", "exam practice", "AQA", "Edexcel", "OCR", "GCSE past papers",
    "A-Level past papers", "online quiz platform", "Beyond Imagination", "Beyond Tutors",
  ],
  authors: [{ name: "Beyond Imagination" }],
  creator: "Beyond Imagination",
  publisher: "Beyond Imagination",
  applicationName: "Notenix",
  alternates: { canonical: SITE },
  openGraph: {
    type: "website",
    url: SITE,
    siteName: "Notenix",
    title: "Notenix — Smart GCSE & A-Level Quiz & Past Paper Practice",
    description:
      "Ace GCSE & A-Level exams with smart quizzes built on real past papers, instant marking and progress tracking. Start free.",
    locale: "en_GB",
  },
  twitter: {
    card: "summary_large_image",
    title: "Notenix — Smart GCSE & A-Level Quiz & Past Paper Practice",
    description: "Ace GCSE & A-Level exams with smart quizzes built on real past papers. Start free.",
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
      description: "Smart GCSE & A-Level quiz and past-paper practice platform by Beyond Imagination.",
      parentOrganization: { "@type": "Organization", name: "Beyond Imagination" },
    },
    {
      "@type": "WebSite",
      "@id": `${SITE}/#website`,
      url: SITE,
      name: "Notenix",
      publisher: { "@id": `${SITE}/#org` },
      inLanguage: "en-GB",
    },
    {
      "@type": "WebApplication",
      name: "Notenix",
      url: SITE,
      applicationCategory: "EducationalApplication",
      operatingSystem: "Web",
      offers: [
        { "@type": "Offer", price: "0", priceCurrency: "GBP", name: "Free" },
        { "@type": "Offer", price: "9.99", priceCurrency: "GBP", name: "Pro" },
      ],
    },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-GB">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet" />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      </head>
      <body className="min-h-screen bg-canvas text-ink antialiased">
        <Shell>{children}</Shell>

        {/* Google Analytics 4 — loads only when NEXT_PUBLIC_GA_ID is set */}
        {GA_ID && (
          <>
            <Script
              src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
              strategy="afterInteractive"
            />
            <Script
              id="ga4-init"
              strategy="afterInteractive"
              dangerouslySetInnerHTML={{
                __html: `
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());
                  gtag('config', '${GA_ID}', { anonymize_ip: true });
                `,
              }}
            />
          </>
        )}
      </body>
    </html>
  );
}
