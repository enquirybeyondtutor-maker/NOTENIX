"use client";
import { useEffect, useState } from "react";
import Script from "next/script";

// Google Analytics 4, loaded only once the visitor has accepted cookies:
// a saved "granted" choice on return visits, or the Accept button (which fires
// "notenix-consent-granted"). Declined or undecided visitors never download gtag.
// Page views on client-side navigation come from GA4 enhanced measurement.
export default function Analytics({ gaId }: { gaId: string }) {
  const [granted, setGranted] = useState(false);

  useEffect(() => {
    try {
      if (localStorage.getItem("notenix_consent") === "granted") setGranted(true);
    } catch {
      /* storage blocked: stay off */
    }
    const on = () => setGranted(true);
    window.addEventListener("notenix-consent-granted", on);
    return () => window.removeEventListener("notenix-consent-granted", on);
  }, []);

  if (!granted) return null;

  return (
    <>
      <Script src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`} strategy="lazyOnload" />
      <Script
        id="ga4-init"
        strategy="lazyOnload"
        dangerouslySetInnerHTML={{
          __html: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('consent', 'default', { analytics_storage: 'granted', ad_storage: 'denied' });
            gtag('config', '${gaId}', { anonymize_ip: true });
          `,
        }}
      />
    </>
  );
}
