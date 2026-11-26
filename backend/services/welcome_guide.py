"""What to do next, sent in the "Payment received" email: how to sign in, the first thing to open
for what was bought, and (for the TMUA Mock Series) the whole schedule.

guide(user, payment) -> {"steps": [html, ...], "schedule_title": str, "schedule": [(label, value), ...]}
Steps are small, already-escaped HTML fragments (links built here from known paths only).
"""
from datetime import datetime
from html import escape

from services import courses as course_svc
from services import mail_template as T


def _link(path: str, label: str) -> str:
    return f'<a href="{T.site(path)}" style="color:{T.BRAND};font-weight:600">{escape(label)}</a>'


def _signin_steps(user) -> list[str]:
    return [
        f'Go to {_link("/login", "notenix.com/login")} and sign in with the user ID <b>{escape(user.email)}</b> '
        "(not your personal email).",
        "Use the password you chose when you signed up. Forgot it? Choose <b>Forgot password</b> on the sign-in page "
        "and we'll email you a code.",
    ]


def _first_steps(user, p) -> list[str]:
    from services import exams, tmua_series, ks3
    course = getattr(p, "course", None)
    if course == tmua_series.KEY:
        return [f"Open {_link('/tests', 'Tests')}: the <b>Baseline Mock</b> is waiting there. Take it first, under timed conditions.",
                "Each mock appears in Tests at <b>10 a.m. UK time</b> on its date (schedule below), with a 24-hour ranked window.",
                f"Stuck on a topic? Ask for a TMUA topic set from {_link('/request', 'Request a test')} "
                f"(up to {tmua_series.REQUESTS_PER_WEEK} a week)."]
    if p.purpose == "ks3":
        return [f"Open {_link('/tests', 'Tests')}: the {escape(ks3.year_label(user))} tests are waiting there, about 30 minutes each.",
                f"Stuck on homework? Send a photo from {_link('/help', 'Homework help')} and a tutor replies.",
                "A progress report arrives by email every month."]
    if p.purpose in ("doubt", "plus", "annual"):
        return [f"Open {_link('/help', 'Ask a tutor')} and send a photo of any question you're stuck on.",
                "A Beyond Tutors tutor replies with the method, step by step."]
    if p.purpose == "pro":
        return [f"Open {_link('/quiz', 'Quizzes')} for unlimited AI quizzes and written-answer practice with instant marking."]
    if p.purpose == "test_request":
        return [f"Our team is preparing your test. It will appear in {_link('/tests', 'Tests')} and we'll email you when it does."]
    if course:
        keys = course_svc.bundle_courses(course) if course_svc.is_bundle(course) else [course]
        out = []
        for k in keys:
            name = course_svc.course_name(k)
            if k == "sat":
                out.append(f"{escape(name)}: open {_link('/sat/practice', 'SAT practice')} for full adaptive tests and your skill map.")
            elif k in exams.EXAMS:
                out.append(f"{escape(name)}: open {_link(f'/{k}/practice', f'{name} practice')}. Start with the diagnostic, "
                           "then follow your study plan, practice tests and drills.")
            else:
                out.append(f"{escape(name)}: open {_link('/practice', 'Practice')} and {_link('/papers', 'Revision papers')}, "
                           f"and ask for a tutor-marked test from {_link('/request', 'Request a test')}.")
        return out
    return [f"Open {_link('/dashboard', 'your dashboard')} to see everything you can use."]


def _schedule(p) -> tuple[str, list[tuple[str, str]]]:
    from services import tmua_series
    if getattr(p, "course", None) != tmua_series.KEY:
        return "", []
    now = datetime.utcnow()
    rows = [(f"Mock {n}", escape(f"{at:%a %d %b %Y}, 10 a.m. UK · {level}" + (" (already open)" if at <= now else "")))
            for n, at, level in tmua_series.MOCKS]
    rows += [(escape(f"{at:%a %d %b %Y}"), escape(label)) for at, label in tmua_series.DEADLINES]
    rows.append(("TMUA exam", escape(tmua_series.EXAM_WINDOW)))
    return "Your TMUA Mock Series schedule", rows


def guide(user, p) -> dict:
    title, rows = _schedule(p)
    return {"steps": _signin_steps(user) + _first_steps(user, p), "schedule_title": title, "schedule": rows}
