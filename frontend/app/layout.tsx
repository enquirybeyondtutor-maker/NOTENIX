import "katex/dist/katex.min.css";
import "./globals.css";
import type { Metadata } from "next";
import Script from "next/script";
import Shell from "@/components/Shell";
import CookieConsent from "@/components/CookieConsent";
import { SITE } from "@/lib/site";

const GA_ID = process.env.NEXT_PUBLIC_GA_ID || "G-6NVHXT86PC"; // GA4 Measurement ID (env var overrides)

export const metadata: Metadata = {
  metadataBase: new URL(SITE),
  title: {
    default: "Notenix: Free Practice Tests Marked by Tutors (SAT, ESAT, TMUA, IGCSE, JEE, NEET)",
    template: "%s | Notenix",
  },
  description:
    "Free practice tests for SAT, ESAT, TMUA, GCSE, IGCSE, A-Level, CBSE, ICSE, JEE and NEET. Sit timed mocks online, get instant marking, or request a full mock marked by real tutors. Students anywhere can start free.",
  keywords: [
    "Notenix", "notenix", "SAT practice test", "digital SAT practice", "free SAT mock", "ESAT practice",
    "ESAT mock test", "TMUA practice", "TMUA mock", "IGCSE practice test", "JEE Main mock test",
    "NEET mock test", "CBSE practice test", "ICSE practice test", "GCSE quiz", "A-Level quiz", "past papers", "GCSE revision",
    "A-Level revision", "exam practice", "AQA", "Edexcel", "OCR", "GCSE past papers",
    "A-Level past papers", "online quiz platform", "Beyond Imagination", "Beyond Tutors",
  ],
  authors: [{ name: "Beyond Imagination" }],
  creator: "Beyond Imagination",
  publisher: "Beyond Imagination",
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
      description: "Online practice-test platform for SAT, ESAT, TMUA, GCSE and A-Level, with mocks marked by tutors from Beyond Tutors.",
      parentOrganization: { "@type": "Organization", name: "Beyond Imagination" },
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

        {/* Google Analytics 4 with Consent Mode — analytics cookies stay OFF until
            the visitor accepts (GDPR/PECR). Consent defaults to denied; the banner
            grants it, and returning visitors' saved choice is re-applied here. */}
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
                  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', wait_for_update: 500 });
                  try { if (localStorage.getItem('notenix_consent') === 'granted') gtag('consent', 'update', { analytics_storage: 'granted' }); } catch (e) {}
                  gtag('config', '${GA_ID}', { anonymize_ip: true });
                `,
              }}
            />
          </>
        )}
        <CookieConsent />
      </body>
    </html>
  );
}
