# GEO Audit Report: Notenix

**Audit Date:** 2026-11-04
**URL:** https://www.notenix.com (notenix.com 308-redirects to www)
**Business Type:** SaaS (EdTech practice-test platform, free + paid tiers, tutor-marked mocks)
**Pages Analyzed:** 13 (home, 10 exam pages, /request, /pricing). Legal pages (terms/privacy/refunds) were skipped as low-value.

---

## Executive Summary

**Overall GEO Score: 48/100 (Poor)**

The technical side is strong. Pages are server-rendered on Next.js/Vercel, AI crawlers are allowed, an llms.txt is in place, and every exam page has rich JSON-LD (FAQPage, Course, BreadcrumbList). The score is held down by brand authority: a web search for "Notenix" returns nothing about the product, so AI models have no outside source that tells them Notenix exists. E-E-A-T is also weak, with no named tutors, no About page and no credentials anywhere. The schema has a pricing conflict to fix too: it says £9.99 while the pricing page says £49 a year.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 62/100 | 25% | 15.5 |
| Brand Authority | 10/100 | 20% | 2.0 |
| Content E-E-A-T | 40/100 | 20% | 8.0 |
| Technical GEO | 88/100 | 15% | 13.2 |
| Schema & Structured Data | 72/100 | 10% | 7.2 |
| Platform Optimization | 25/100 | 10% | 2.5 |
| **Overall GEO Score** | | | **48/100** |

---

## Critical Issues (Fix Immediately)

1. **The brand isn't recognised as an entity.** A web search for `"Notenix" practice tests` returns no results about the product (the top hit is an unrelated tool, Notelyn). No AI system can cite or recommend Notenix without some outside corroboration.
   *Fix:* create LinkedIn, YouTube, Facebook and Instagram profiles and link to them from the Beyond Tutors site (see the Quick Wins and Week 1 below).

## High Priority Issues

1. **The pricing data conflicts.** The homepage `WebApplication.offers` lists Pro at **£9.99 GBP**, while the `/pricing` title says "Notenix for Beyond Tutors Students, **£49 a Year**". AI answers will quote the wrong price. Pick one and make the schema, the page copy and llms.txt agree.
2. **No author or expert attribution.** The exam pages say "written by tutors" and "marked by our team", but no tutor is named, has a bio or lists credentials. For high-stakes exams like ESAT, TMUA, JEE and NEET, this is the main trust signal AI models look for.
3. **No About page.** It isn't in the sitemap or the navigation. llms.txt only says "Built by Beyond Imagination".
4. **The Organization schema is thin.** It has no `logo`, `sameAs`, `contactPoint`, `email` or `founder`. `parentOrganization` says "Beyond Groups", llms.txt says "Beyond Imagination" and the copy says "Beyond Tutors". Settle on one consistent ownership statement.

## Medium Priority Issues

1. **Exam pages are thin and templated.** They run about 565–800 words each, and all 10 share an identical H2/H3 skeleton. They are useful, but AI models favour deeper pages: a marking breakdown, score-to-grade tables, dates, and how each board differs.
2. **Every sitemap URL has the same `lastmod` (2026-11-04T10:12:09Z).** The date is generated at build time, so it tells crawlers nothing about freshness. Use real content-change dates.
3. **The Organization description in the schema is stale.** It lists only "SAT, ESAT, TMUA, GCSE and A-Level", leaving out IGCSE, CBSE, ICSE, JEE and NEET.
4. **Maths renders as duplicated text.** In the plain-text extraction, KaTeX outputs every expression three times, e.g. "(x + 3)(x - 5) (x + 3)(x - 5) ( x + 3 ) ( x − 5 )". Crawlers that skip MathML quote this garbled text. Add an `aria-hidden` or plain-text version, or keep the annotation out of the text flow.
5. **No Reddit, Quora or Student Room presence.** These are the places AI models draw on for "best free ESAT/TMUA practice" questions.

## Low Priority Issues

1. **No images.** There are 0 `<img>` tags, so no screenshots of the test UI or report. That's fine for crawlers, but it rules out image results and makes the product less concrete.
2. **The `/pricing` and `/request` pages have no FAQPage or BreadcrumbList schema**, unlike the exam pages.
3. **robots.txt uses a non-standard `Host:` directive.** It's harmless, and Google ignores it.

---

## Category Deep Dives

### AI Citability (62/100)
- **Strengths:** each exam page opens with a clear "X: an overview" block plus a format block, e.g. "Three papers of 1 hour 30 minutes each, one of them non-calculator… Foundation tier covers grades 1–5; Higher tier covers grades 4–9." These are short, factual and self-contained, which makes them ideal for AI citation. The FAQ sections and the 4-step process ("Request → We send it → Sit it online → Tutor marks it") are also easy to quote.
- **Weaknesses:** the pages offer no unique data, such as average scores, pass-mark history or "students who did X mocks scored Y". The sample questions are only 5 per page. The homepage itself reads mostly as a list of links.
- **Rewrite suggestion:** add a one-sentence definition at the top of every page. For example: *"Notenix ESAT mocks are full-length, timed papers that mirror the ESAT's 40-minute, 27-question modules, marked instantly and optionally reviewed by a Beyond Tutors tutor."*

### Brand Authority (10/100)
| Platform | Status |
|---|---|
| Google / web mentions | None found |
| Wikipedia / Wikidata | None |
| Reddit | None found |
| YouTube | None (Beyond Tutors has a channel, @thebeyondtutors, that could carry Notenix) |
| LinkedIn | None for Notenix (Beyond Tutors company page exists) |
| Backlink from thebeyondtutors.com | Check this: it's the cheapest authority win |

### Content E-E-A-T (40/100)
- Experience: there's a real tutor-marking workflow, but no testimonials, case studies or sample marked scripts.
- Expertise: questions are "original, written by tutors", but nobody is named.
- Authority: no outside citations, and no links to official specs (College Board, UAT-UK, AQA, NTA).
- Trust: Terms, privacy and refunds pages exist, plus HTTPS/HSTS. There's no About page or physical/contact details beyond an email in llms.txt.

### Technical GEO (88/100)
- Pages are SSR/prerendered (`X-Nextjs-Prerender: 1`), and all content is in the initial HTML.
- GPTBot, ClaudeBot and PerplexityBot all get HTTP 200, and robots.txt only blocks app routes (good).
- llms.txt exists and is well structured (exams, how it works, about, contact).
- Canonicals, OG and Twitter tags are set on all pages, and the security headers are good (HSTS, X-Frame-Options, nosniff, Referrer-Policy).
- Lost points: the fake sitemap `lastmod`, the KaTeX text duplication, and no llms-full.txt.

### Schema & Structured Data (72/100)
- Exam pages carry WebSite, Organization, WebApplication, Course, CourseInstance, FAQPage, BreadcrumbList and Offer, which is strong coverage.
- Missing: Organization `logo`/`sameAs`/`contactPoint`; `Person` schema for tutors; `Quiz` (schema.org/Quiz) for the sample questions; FAQPage on /pricing.
- Error: the price mismatch (£9.99 vs £49/yr).

### Platform Optimization (25/100)
- **Google AI Overviews:** the FAQ and format blocks help, but the site has no authority yet to rank.
- **ChatGPT / Perplexity:** both lean on Reddit and Student Room threads for "best ESAT practice". Notenix isn't present there.
- **Gemini:** relies on YouTube, where Notenix has no presence.
- **Bing Copilot:** check whether the site is submitted to Bing Webmaster Tools and IndexNow.

---

## Quick Wins (Implement This Week)

1. Fix the price conflict across the schema, /pricing and llms.txt.
2. Add `logo`, `email`, `sameAs` (Beyond Tutors site, YouTube, LinkedIn) and one consistent `parentOrganization` to the Organization schema.
3. Link to Notenix from thebeyondtutors.com (footer + each exam tutor page). It's the fastest authority signal.
4. Publish an /about page naming the tutors who write and mark questions, with credentials. Add `Person` schema.
5. Submit the sitemap to Google Search Console and Bing Webmaster Tools, and switch `lastmod` to real dates.

## 30-Day Action Plan

### Week 1: Entity and trust foundations
- [ ] Fix the pricing schema; update the Organization schema
- [ ] Publish the /about page with tutor bios + Person schema
- [ ] Cross-link from thebeyondtutors.com and the BT LinkedIn/YouTube bios

### Week 2: Content depth
- [ ] Expand ESAT, TMUA and SAT pages to 1,200+ words: score scales, test dates, section timings, common mistakes
- [ ] Add one-sentence definition blocks at the top of each exam page
- [ ] Fix the KaTeX duplicate text for crawlers

### Week 3: Off-site presence
- [ ] Answer genuine ESAT/TMUA questions on Reddit (r/6thForm, r/Oxbridge) and The Student Room, disclosing your link to Notenix
- [ ] Add Notenix to the description and end card of BT YouTube videos (TMUA/TARA playlists)
- [ ] Create a LinkedIn showcase page or product listing

### Week 4: Proof and measurement
- [ ] Publish one data piece, e.g. "What 100 ESAT mocks taught us: the most-missed topics"
- [ ] Add testimonials and a sample marked script
- [ ] Re-run `/geo-audit notenix.com` and compare with `/geo-compare`

---

## Appendix: Pages Analyzed

| URL | Title | Words | GEO Issues |
|---|---|---|---|
| / | Notenix: Free Practice Tests Marked by Tutors (SAT, ESAT, TMUA, IGCSE, JEE, NEET) | 795 | 3 (price conflict, thin Org schema, stale description) |
| /sat | Free Digital SAT Practice Test & Tutor-Marked SAT Mocks | 796 | 2 |
| /esat | ESAT Practice Tests & Mock Exams | 763 | 2 |
| /tmua | TMUA practice | ~700 | 2 |
| /gcse-maths | GCSE Maths Practice Tests & Quizzes (AQA, Edexcel, OCR) | 723 | 3 (KaTeX duplication) |
| /a-level-maths | A-Level Maths Practice Tests & Mock Papers | 668 | 3 |
| /igcse | IGCSE Practice Tests & Mock Papers | 601 | 2 |
| /cbse | CBSE Class 10 & 12 Practice Tests | 565 | 2 |
| /icse | ICSE Class 10 & ISC Class 12 Practice Tests | 601 | 2 |
| /jee | JEE Main Mock Tests & Practice Questions | 677 | 2 |
| /neet | NEET practice | ~650 | 2 |
| /request | Request a Tutor-Marked Mock Test | 258 | 2 (thin, no FAQ schema) |
| /pricing | Pricing: Notenix for Beyond Tutors Students, £49 a Year | 221 | 2 (price conflict, no FAQ schema) |
