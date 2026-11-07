"""Renders every email Notenix sends, with sample data, into docs/notenix-email-gallery.html.
Nothing is sent: delivery is replaced by a recorder.  Run: python email_gallery.py"""
import asyncio
import html as H
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./_gallery.db")
sys.path.insert(0, str(Path(__file__).parent))
from services import email as E  # noqa: E402
from services import ks3  # noqa: E402
from services import mail_template as T  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LOCAL_LOGO = (ROOT / "frontend" / "public" / "brand" / "notenix-email-logo.png").as_uri()
SHOTS: list[dict] = []
CURRENT = {"name": "", "who": ""}


async def _record(to, subject, html, text):
    html = html.replace(T.site("/brand/notenix-email-logo.png"), LOCAL_LOGO)  # logo not deployed yet
    SHOTS.append({**CURRENT, "to": to, "subject": subject, "html": html, "text": text})
    return True

E._deliver = _record
E._send_resend = lambda to, s, h, t: _record(to, s, h, t)
E.settings.resend_api_key = "x"
E.settings.admin_emails = "hello@thebeyondtutors.com"
ks3._deliver = _record


def label(name, who):
    CURRENT.update(name=name, who=who)


BT = SimpleNamespace(full_name="Musa Khan", email="musa@thebeyondtutors.com", parent_email="musa.parent@example.com", ks3_year=None)
REAL = SimpleNamespace(full_name="Priya Patel", email="priya.patel@gmail.com", parent_email=None, ks3_year=None)
KS = SimpleNamespace(full_name="Aisha Khan", email="aisha@notenix.com", parent_email="aisha.mum@example.com", ks3_year=7, billing_currency="GBP", ks3_emails=[], notify_email=None)


async def main():
    for kind, who in (("ks3", "Parent starting the KS3 free week"), ("activate", "Parent activating a Beyond Tutors account"),
                      ("reset", "Password reset (goes to the student's real email, else the parent)"),
                      ("verify", "Public sign-up (switched off at the moment)")):
        label(f"Code: {kind}", who)
        await E.send_otp_email("parent@example.com", "Aisha Khan" if kind == "ks3" else "Musa Khan", "482913", kind=kind)

    label("Test assigned (to parent)", "BT student's login isn't an inbox, so the parent gets it")
    await E.send_assignment_email(BT, "TMUA Algebra Mock 1", "Maths", "Aryan", datetime.utcnow() + timedelta(days=3))
    label("Test assigned (to student)", "Student whose login is a real email")
    await E.send_assignment_email(REAL, "SAT Practice Test 2", "Maths", "The Notenix team", None)
    label("Test marked (to parent)", "Parent, when a written test is marked")
    await E.send_marked_email(BT, "GCSE Higher Paper 1", 72, "7")
    STU = SimpleNamespace(full_name="Musa Khan", email="musa@thebeyondtutors.com", parent_email="musa.parent@example.com",
                          notify_email="musa.khan@gmail.com", ks3_year=None)
    label("Homework updates switched on", "Student, right after adding their own email")
    await E.send_update_email_confirmed(STU, STU.notify_email)
    label("New homework", "Student's own email, when homework is added")
    await E.send_new_material(STU, "homework", "Fractions worksheet", "Maths", datetime.utcnow() + timedelta(days=5), "Do questions 1-10. Show your working.", "Aryan")
    label("New class notes", "Student's own email, when class notes are added")
    await E.send_new_material(STU, "notes", "Algebra: expanding brackets", "Maths", None, None, "Aryan")
    label("Payment received", "Parent, when you confirm a payment")
    await E.send_payment_result(KS, True, "Aisha Khan's Notenix KS3 year", 149, "GBP", "NX-K42",
                                "Notenix KS3 is on for a year: a test every half-term, homework help, notes and a progress report every month.")
    label("Payment not matched", "Parent, when you reject a payment claim")
    await E.send_payment_result(KS, False, "Aisha Khan's Notenix KS3 year", 149, "GBP", "NX-K42")
    label("Test request cancelled", "Student/parent, when you cancel a test request")
    await E.send_request_cancelled(REAL, "SAT", 12, "Please book a time with us first.")
    label("Homework question answered", "KS3 parent, when a tutor replies")
    await E.send_help_answered(KS, "Maths")
    label("Admin alert: homework question", "You (ADMIN_EMAILS)")
    await E.notify_admins("Homework question from Aisha Khan", "Aisha Khan sent a Maths homework question. Please reply within a day.",
                          "/teacher/help", rows=[("Student", "Aisha Khan (Year 7)"), ("Subject", "Maths"),
                                                 ("Question", "Q4: how do I find the missing angle?"), ("Photos", "1")])
    label("Admin alert: payment to check", "You (ADMIN_EMAILS)")
    await E.notify_admins("Payment to check: NX-K42", "Aisha Khan (aisha@notenix.com, Year 7) says they paid £149 for Notenix KS3 via UK bank. Payer: R Khan.",
                          "/admin/requests")

    p = {"taken": [{"title": "a", "subject": "Maths", "score": 67, "date": datetime.utcnow() - timedelta(days=4)},
                   {"title": "b", "subject": "Science", "score": 74, "date": datetime.utcnow() - timedelta(days=5)},
                   {"title": "c", "subject": "English", "score": 81, "date": datetime.utcnow() - timedelta(days=3)}],
         "missed": [], "subjects": {"Maths": {"first": 58, "latest": 67, "count": 2}, "Science": {"first": 74, "latest": 74, "count": 1},
                                    "English": {"first": 81, "latest": 81, "count": 1}},
         "strengths": [{"subject": "Maths", "topic": "Algebra basics", "pct": 100}, {"subject": "Science", "topic": "Cells", "pct": 92}],
         "focus": [{"subject": "Maths", "topic": "Negative numbers", "pct": 25}, {"subject": "Science", "topic": "Forces", "pct": 40}],
         "average": 70, "gcse": "5–6"}
    for kind, who in (("welcome", "KS3 parent, day 0"), ("checkin", "KS3 parent, day 3"), ("ending", "KS3 parent, day 5"),
                      ("report", "KS3 parent, day 7"), ("monthly", "KS3 paying parent, monthly")):
        label(f"KS3: {kind}", who)
        s, h, t = ks3.BUILDERS[kind](KS, p)
        await _record(KS.parent_email, s, h, t)

    cards = []
    for i, s in enumerate(SHOTS, 1):
        cards.append(f"""<section><div class="meta"><span class="n">{i}</span><div><b>{H.escape(s['name'])}</b>
<div class="who">{H.escape(s['who'])} &nbsp;·&nbsp; sent to <code>{H.escape(s['to'])}</code> &nbsp;·&nbsp; Reply-To: <code>{H.escape(E.settings.support_email)}</code></div>
<div class="subj">Subject: <b>{H.escape(s['subject'])}</b></div></div></div>
<iframe srcdoc="{H.escape(s['html'])}" loading="lazy"></iframe></section>""")
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Notenix emails</title><style>
body{{font:14px system-ui,sans-serif;background:#e2e8f0;margin:0;padding:24px;color:#0f172a}}h1{{margin:0 0 4px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(640px,1fr));gap:20px;margin-top:20px}}
section{{background:#fff;border:1px solid #cbd5e1;border-radius:14px;overflow:hidden}}
.meta{{display:flex;gap:12px;padding:14px 16px;border-bottom:1px solid #e2e8f0}}.n{{background:#5444DC;color:#fff;border-radius:99px;
width:26px;height:26px;display:grid;place-items:center;font-weight:700;flex:none}}.who,.subj{{font-size:12px;color:#64748b;margin-top:3px}}
iframe{{width:100%;height:820px;border:0}}</style></head><body>
<h1>Every Notenix email, new design</h1><p>{len(SHOTS)} emails with sample data. Nothing was sent.</p>
<div class="grid">{''.join(cards)}</div></body></html>"""
    out = ROOT / "docs" / "notenix-email-gallery.html"
    out.write_text(page, encoding="utf-8")
    print(f"{len(SHOTS)} emails -> {out}")
    for s in SHOTS:
        print(f"  - {s['name']} -> {s['to']}: {s['subject']}")


asyncio.run(main())
