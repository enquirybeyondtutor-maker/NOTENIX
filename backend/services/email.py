"""Email delivery and every Notenix email except the KS3 parent series (services/ks3.py).

Sends over an HTTPS email API (Resend or Brevo) so it works on hosts that block outbound SMTP
(e.g. Render). Falls back to SMTP, then to the console (dev). Every email is sent from
EMAIL_FROM (noreply@notenix.com) with Reply-To SUPPORT_EMAIL (support@notenix.com), and is
built from services/mail_template.py so they all share one design.

Who receives what: Notenix user IDs (name@thebeyondtutors.com, name@notenix.com) are logins,
not mailboxes. recipients() sends to the parent's email instead (worded for a parent), and to
the student as well when their login is a real address.
"""
import smtplib
import secrets
from html import escape
import httpx
from email.message import EmailMessage
from fastapi.concurrency import run_in_threadpool
from config import settings
from services import mail_template as T


class EmailSendError(Exception):
    """Raised when a configured email provider fails to accept the message."""


def generate_otp() -> str:
    """A 6-digit numeric one-time code."""
    return f"{secrets.randbelow(1_000_000):06d}"


def _from() -> tuple[str, str]:
    name = settings.smtp_from_name or "Notenix"
    email = settings.email_from or settings.smtp_from or settings.smtp_user or "onboarding@resend.dev"
    return name, email


def is_mailbox(address: str | None) -> bool:
    """False for Notenix login IDs, which look like emails but have no inbox."""
    if not address or "@" not in address:
        return False
    domain = address.rsplit("@", 1)[1].lower()
    return domain not in {settings.student_id_domain.lower(), settings.ks3_id_domain.lower()}


def recipients(user) -> list[tuple[str, str]]:
    """[(address, "parent" | "student")] for a student account, de-duplicated."""
    out: list[tuple[str, str]] = []
    parent = (getattr(user, "parent_email", None) or "").strip().lower()
    if parent and is_mailbox(parent):
        out.append((parent, "parent"))
    for own in ((getattr(user, "notify_email", None) or "").strip().lower(),
                (getattr(user, "email", None) or "").strip().lower()):
        if is_mailbox(own) and own not in {a for a, _ in out}:
            out.append((own, "student"))
            break  # one student address is enough
    return out


def student_inbox(user) -> str | None:
    """The student's own inbox: the update email they gave, else their login if it's a real address."""
    for a in (getattr(user, "notify_email", None), getattr(user, "email", None)):
        if is_mailbox(a):
            return a.strip().lower()
    return None


_background: set = set()


def in_background(coro) -> None:
    """Send without making the web request wait (and never fail it)."""
    import asyncio

    async def run():
        try:
            await coro
        except Exception as e:
            print(f"[email] background send failed: {e}")
    task = asyncio.create_task(run())
    _background.add(task)
    task.add_done_callback(_background.discard)


def best_address(user) -> str | None:
    """Single address for one-time codes: the student's own inbox if real, else the parent's."""
    own = student_inbox(user)
    if own:
        return own
    parent = getattr(user, "parent_email", None)
    return parent if is_mailbox(parent) else None


# ── Providers ──────────────────────────────────────────────────────────────────

async def _send_resend(to_email: str, subject: str, html: str, text: str) -> None:
    name, email = _from()
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.resend_api_key}"},
            json={"from": f"{name} <{email}>", "to": [to_email], "subject": subject, "html": html, "text": text,
                  "reply_to": settings.support_email},
        )
    if r.status_code >= 300:
        raise EmailSendError(f"resend {r.status_code}: {r.text[:200]}")


async def _send_brevo(to_email: str, subject: str, html: str, text: str) -> None:
    name, email = _from()
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"api-key": settings.brevo_api_key, "content-type": "application/json"},
            json={
                "sender": {"name": name, "email": email},
                "replyTo": {"email": settings.support_email, "name": "Notenix support"},
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html,
                "textContent": text,
            },
        )
    if r.status_code >= 300:
        raise EmailSendError(f"brevo {r.status_code}: {r.text[:200]}")


def _send_smtp_sync(to_email: str, subject: str, html: str, text: str) -> None:
    name, email = _from()
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{name} <{email}>"
    msg["To"] = to_email
    msg["Reply-To"] = settings.support_email
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)


async def _deliver(to_email: str, subject: str, html: str, text: str) -> bool:
    """Best-effort send via the first configured provider. Never raises — used for
    notification emails that must not block or fail the originating request."""
    provider = None
    try:
        if settings.resend_api_key:
            provider = "resend"; await _send_resend(to_email, subject, html, text)
        elif settings.brevo_api_key:
            provider = "brevo"; await _send_brevo(to_email, subject, html, text)
        elif settings.smtp_user and settings.smtp_password:
            provider = "smtp"; await run_in_threadpool(_send_smtp_sync, to_email, subject, html, text)
        else:
            print(f"[DEV] email to {to_email}: {subject}")
            return False
        return True
    except Exception as e:
        print(f"[WARN] {provider} notification email failed for {to_email}: {e}")
        return False


async def _to_family(user, build) -> None:
    """build(role) -> (subject, html, text); sent to every real inbox for this student."""
    for address, role in recipients(user):
        try:
            await _deliver(address, *build(role))
        except Exception as e:  # never fail the request because of an email
            print(f"[email] {address}: {e}")


# ── One-time codes ─────────────────────────────────────────────────────────────

def _content(full_name: str, code: str, kind: str = "verify") -> tuple[str, str, str]:
    """(subject, html, text). kind = verify | reset | activate | ks3."""
    mins = settings.otp_expiry_minutes
    child = T.first_name(full_name)
    if kind == "doubt":
        subject = f"{code} is your code to start {child}'s free trial"
        heading, pre = f"Start {child}'s free trial", "Enter this code on notenix.com to continue."
        lead = f"Enter this code on notenix.com to confirm your email and start {child}'s free Ask a Tutor trial."
        ignore, audience = "If you didn't ask for this, you can ignore this email; nothing will be set up.", "signup"
    elif kind == "ks3":
        subject = f"{code} is your code to start {child}'s free week"
        heading, pre = f"Start {child}'s free week", "Enter this code on notenix.com to continue."
        lead = f"Enter this code on notenix.com to confirm your email and start {child}'s free Notenix KS3 week."
        ignore, audience = "If you didn't ask for this, you can ignore this email; nothing will be set up.", "signup"
    elif kind == "activate":
        subject = f"{code} is your Notenix activation code"
        heading, pre = f"Activate {child}'s Notenix account", "Enter this code to finish setting up the account."
        lead = f"Enter this code to confirm your email and activate the Notenix account Beyond Tutors set up for {escape(full_name)}."
        ignore, audience = "If you didn't ask for this, you can ignore this email.", "parent"
    elif kind == "reset":
        subject = f"{code} is your Notenix password reset code"
        heading, pre = "Reset your password", "Enter this code to choose a new password."
        lead = f"Enter this code to choose a new password for {escape(full_name)}'s Notenix account."
        ignore, audience = "If you didn't ask to reset the password, you can ignore this email; the password stays the same.", "student"
    else:
        subject = f"{code} is your Notenix verification code"
        heading, pre = "Verify your email", "Enter this code to finish creating your account."
        lead = "Enter this code to finish creating your Notenix account."
        ignore, audience = "If you didn't sign up, you can ignore this email.", "signup"
    body = T.para(lead) + T.code_box(code, mins) + f'<p style="margin:0;font-size:13px;color:{T.FAINT}">{ignore}</p>'
    html = T.layout(preheader=f"{code} · {pre}", heading=heading, body=body, audience=audience)
    text = f"{heading}\n\nYour code: {code}\nIt expires in {mins} minutes.\n\n{ignore}" + T.text_footer()
    return subject, html, text


async def send_otp_email(to_email: str, full_name: str, code: str, kind: str = "verify") -> None:
    """Email a one-time code via the first configured provider. Resend/Brevo failures raise
    EmailSendError so the caller can tell the user; with no provider the code is logged (dev)."""
    subject, html, text = _content(full_name, code, kind)
    provider = None
    try:
        if settings.resend_api_key:
            provider = "resend"
            await _send_resend(to_email, subject, html, text)
        elif settings.brevo_api_key:
            provider = "brevo"
            await _send_brevo(to_email, subject, html, text)
        elif settings.smtp_user and settings.smtp_password:
            provider = "smtp"
            await run_in_threadpool(_send_smtp_sync, to_email, subject, html, text)
        else:
            print(f"[DEV] OTP for {to_email}: {code} (no email provider configured)")
            return
    except Exception as e:
        print(f"[WARN] {provider} email send failed for {to_email}: {e}")
        if provider in ("resend", "brevo"):
            raise EmailSendError(str(e)) from e
        print(f"[DEV] OTP for {to_email}: {code}")


# ── Tests ──────────────────────────────────────────────────────────────────────

async def send_assignment_email(student, test_title: str, subject: str, teacher_name: str, due_at) -> None:
    child = T.first_name(student.full_name)
    due = due_at.strftime("%a %d %b") if due_at else None

    def build(role):
        if role == "parent":
            heading = f"{child} has a new test"
            lead = f"{escape(teacher_name)} has set {child} a new {escape(subject)} test on Notenix."
            subj = f"{T.first_name(student.full_name)} has a new test: {test_title}"
        else:
            heading = "You've got a new test"
            lead = f"{escape(teacher_name)} has set you a new {escape(subject)} test."
            subj = f"New test: {test_title}"
        rows = [("Test", escape(test_title)), ("Subject", escape(subject))] + ([("Due", due)] if due else [])
        body = T.para(lead) + T.info_table(rows) + (T.login_box(student.email, student.full_name) if role == "parent" else "")
        html = T.layout(preheader=f"{test_title}" + (f", due {due}" if due else ""), heading=heading, body=body,
                        buttons=[(T.signin_url(student.email) if role == "parent" else T.site("/tests"), "Open the test")],
                        audience=role)
        return subj, html, f"{heading}\n\n{test_title} ({subject})" + (f", due {due}" if due else "") + f"\n{T.site('/tests')}" + T.text_footer()
    await _to_family(student, build)


async def send_marked_email(student, test_title: str, score, grade) -> None:
    child = T.first_name(student.full_name)
    score_txt = f"{round(score)}%" if isinstance(score, (int, float)) else str(score)

    def build(role):
        whose = f"{child}'s" if role == "parent" else "Your"
        rows = [("Test", escape(test_title)), ("Score", f'<span style="color:{T.color_for(round(score) if isinstance(score, (int, float)) else 0)}">{score_txt}</span>')]
        if grade:
            rows.append(("Estimated grade", escape(str(grade))))
        body = T.para(f"{whose} test has been marked{' by a tutor' if role == 'parent' else ''}. The feedback on each question is in Notenix.") + T.info_table(rows)
        html = T.layout(preheader=f"{score_txt}" + (f", grade {grade}" if grade else "") + f" on {test_title}",
                        heading=f"{whose} test has been marked", body=body,
                        buttons=[(T.site("/tests"), "See the feedback")], audience=role)
        subj = f"{child}'s test is marked: {score_txt}" if role == "parent" else f"Your test is marked: {test_title}"
        return subj, html, f"{whose} test '{test_title}' is marked: {score_txt}" + (f", grade {grade}" if grade else "") + T.text_footer()
    await _to_family(student, build)


async def send_request_cancelled(student, exam: str, request_id: int, note: str | None) -> None:
    child = T.first_name(student.full_name)

    def build(role):
        lead = (f"{child}'s {escape(exam)} test request (#{request_id}) has been cancelled." if role == "parent"
                else f"Your {escape(exam)} test request (#{request_id}) has been cancelled.")
        body = T.para(lead) + (T.callout("Note from the team", escape(note)) if note else "") + T.para(
            "If this isn't what you expected, just reply and we'll sort it out.")
        html = T.layout(preheader=f"{exam} request #{request_id}", heading="Test request cancelled", body=body,
                        buttons=[(T.site("/requests"), "View requests")], audience=role)
        return "Test request cancelled", html, lead + (f"\nNote: {note}" if note else "") + T.text_footer()
    await _to_family(student, build)


# ── Payments and homework help ─────────────────────────────────────────────────

async def send_payment_result(user, approved: bool, what: str, amount: float, currency: str,
                              reference: str, extra: str = "") -> None:
    from services.pricing import label as money
    amt = money((currency or "GBP").upper(), float(amount))  # £149, AED 699, ₹16,999

    def build(role):
        if approved:
            heading, subj = "Payment received", f"Payment received · {what}"
            body = (T.para(f"Thank you. We've received your payment for {escape(what)}.") +
                    T.info_table([("Amount", escape(amt)), ("Reference", escape(reference)), ("For", escape(what))]) +
                    (T.para(escape(extra)) if extra else "") + T.login_box(user.email, user.full_name if role == "parent" else None))
            btn = [(T.signin_url(user.email), "Open Notenix")]
        else:
            heading, subj = "We couldn't match your payment", f"Please check your payment · {reference}"
            body = (T.para(f"We couldn't find a payment for {escape(what)} in our account yet.") +
                    T.info_table([("Amount expected", escape(amt)), ("Reference", escape(reference))]) +
                    T.para("Please check the transfer went through with this reference, then tell us again from the pay page, or just reply to this email."))
            btn = [(T.site("/pay"), "Check payment")]
        html = T.layout(preheader=f"{amt} · {reference}", heading=heading, body=body, buttons=btn, audience=role)
        return subj, html, f"{heading}\n{what}: {amt}, reference {reference}" + T.text_footer()
    await _to_family(user, build)


async def send_help_answered(student, subject: str) -> None:
    child = T.first_name(student.full_name)

    def build(role):
        lead = (f"A Beyond Tutors tutor has replied to {child}'s {escape(subject)} homework question with a worked hint."
                if role == "parent" else f"A tutor has replied to your {escape(subject)} homework question.")
        body = T.para(lead) + T.para(f"{child if role == 'parent' else 'You'} can see the reply in Notenix under <b>Homework help</b>.")
        html = T.layout(preheader="The worked hint is waiting in Notenix", heading="Homework question answered",
                        body=body, buttons=[(T.signin_url(student.email) if role == "parent" else T.site("/help"), "Open Homework help")],
                        audience="ks3" if role == "parent" else role)
        subj = f"A tutor answered {child}'s homework question" if role == "parent" else "Your homework question has a reply"
        return subj, html, lead + T.text_footer()
    await _to_family(student, build)


# ── Homework and class notes, straight to the student ──────────────────────────

async def send_update_email_confirmed(user, address: str) -> None:
    child = T.first_name(user.full_name)
    body = (T.para(f"Hi {child}, you're all set. From now on we'll email you here whenever new homework or class notes "
                   "are added to your Notenix account, so you don't need to keep checking.") +
            T.login_box(user.email) +
            T.para(f'<span style="font-size:13px;color:{T.FAINT}">Didn\'t ask for this? You can ignore it, or change the '
                   "email in Notenix → Settings.</span>"))
    html = T.layout(preheader="Homework and class notes will arrive here", heading="Homework updates are on",
                    body=body, buttons=[(T.signin_url(user.email), "Open Notenix")], audience="student")
    await _deliver(address, "You'll get your homework updates here", html,
                   "You're set up: we'll email you here whenever homework or class notes are added." + T.text_footer())


async def send_new_material(student, kind: str, title: str, subject: str | None = None, due_at=None,
                            message: str | None = None, teacher_name: str | None = None) -> None:
    """kind: homework | notes | test. Goes to the student's own inbox only (not the parent)."""
    to = student_inbox(student)
    if not to:
        return
    child = T.first_name(student.full_name)
    due = due_at.strftime("%a %d %b") if due_at else None
    what = {"homework": "homework", "notes": "class notes", "test": "test"}[kind]
    heading = {"homework": "New homework", "notes": "New class notes", "test": "New test"}[kind]
    by = f"{escape(teacher_name)} has" if teacher_name else "Your tutor has"
    rows = [("Title", escape(title))] + ([("Subject", escape(subject))] if subject else []) + ([("Due", due)] if due else [])
    body = T.para(f"Hi {child}, {by} added new {what} for you on Notenix.") + T.info_table(rows)
    if message:
        short = message.strip()
        body += T.callout("Message", escape(short[:400] + ("…" if len(short) > 400 else "")))
    page = "/tests" if kind == "test" else "/notes"
    html = T.layout(preheader=f"{title}" + (f", due {due}" if due else ""), heading=heading, body=body,
                    buttons=[(T.site(page), f"Open the {what}")], audience="student")
    subj = f"{heading}: {title}" + (f" (due {due})" if due else "")
    text = f"{heading}: {title}" + (f", due {due}" if due else "") + f"\n{T.site(page)}" + T.text_footer()
    await _deliver(to, subj, html, text)


# ── Generic notice and admin alerts ────────────────────────────────────────────

async def send_notice(to_email: str, subject: str, heading: str, body_html: str, text: str,
                      path: str, cta_label: str, audience: str = "student") -> None:
    """Any one-off notice in the standard design. `path` is relative to the site."""
    if not is_mailbox(to_email):
        print(f"[email] skipped {subject!r}: {to_email} is a login ID, not a mailbox")
        return
    html = T.layout(preheader=text[:90], heading=heading, body=T.para(body_html),
                    buttons=[(T.site(path), cta_label)], audience=audience)
    await _deliver(to_email, subject, html, text + T.text_footer())


async def notify_admins(subject: str, text: str, path: str, rows: list[tuple[str, str]] | None = None) -> None:
    """Best-effort alert to everyone in ADMIN_EMAILS, with an optional summary table."""
    emails = [e.strip() for e in (settings.admin_emails or "").split(",") if e.strip()]
    body = T.para(escape(text)) + (T.info_table([(k, escape(v)) for k, v in rows]) if rows else "")
    html = T.layout(preheader=text[:90], heading=subject, body=body, buttons=[(T.site(path), "Open in Notenix")],
                    audience="admin", tagline="Admin")
    for e in emails:
        try:
            await _deliver(e, f"[Notenix] {subject}", html, f"{text}\n{T.site(path)}")
        except Exception as ex:  # never fail the request because an email bounced
            print(f"[email] admin notice to {e} failed: {ex}")
