"""Email delivery + OTP helpers for signup verification.

Sends over an HTTPS email API (Resend or Brevo) so it works on hosts that block
outbound SMTP ports (e.g. Render). Falls back to SMTP, then to console (dev).
"""
import smtplib
import secrets
import httpx
from email.message import EmailMessage
from fastapi.concurrency import run_in_threadpool
from config import settings


class EmailSendError(Exception):
    """Raised when a configured email provider fails to accept the message."""


def generate_otp() -> str:
    """A 6-digit numeric one-time code."""
    return f"{secrets.randbelow(1_000_000):06d}"


def _from() -> tuple[str, str]:
    name = settings.smtp_from_name or "Notenix"
    email = settings.email_from or settings.smtp_from or settings.smtp_user or "onboarding@resend.dev"
    return name, email


def _content(full_name: str, code: str, kind: str = "verify") -> tuple[str, str, str]:
    """Returns (subject, html, plaintext). kind = 'verify' | 'reset'."""
    mins = settings.otp_expiry_minutes
    name = (full_name or "there").split(" ")[0]
    if kind == "reset":
        subject = f"{code} is your Notenix password reset code"
        heading = "Reset your password"
        lead = "enter this code to set a new password."
        text = (
            f"Hi {name},\n\n"
            f"Your Notenix password reset code is: {code}\n\n"
            f"It expires in {mins} minutes. If you didn't request a password reset, you can ignore this email.\n\n"
            f"— Notenix"
        )
        ignore = "If you didn't request a password reset, you can safely ignore this email."
    else:
        subject = f"{code} is your Notenix verification code"
        heading = "Verify your email"
        lead = "enter this code to finish creating your account."
        text = (
            f"Hi {name},\n\n"
            f"Your Notenix verification code is: {code}\n\n"
            f"It expires in {mins} minutes. If you didn't sign up, you can ignore this email.\n\n"
            f"— Notenix"
        )
        ignore = "If you didn't sign up for Notenix, you can safely ignore this email."
    html = f"""\
<div style="font-family:Inter,system-ui,sans-serif;max-width:440px;margin:0 auto;color:#0f172a">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:24px">
    <span style="display:inline-grid;place-items:center;width:32px;height:32px;border-radius:10px;background:#4F46E5;color:#fff;font-weight:700">N</span>
    <span style="font-size:17px;font-weight:700">Notenix</span>
  </div>
  <h1 style="font-size:20px;margin:0 0 8px">{heading}</h1>
  <p style="color:#475569;margin:0 0 24px">Hi {name}, {lead}</p>
  <div style="font-size:34px;font-weight:800;letter-spacing:10px;background:#EEF2FF;color:#4F46E5;
              text-align:center;padding:18px;border-radius:14px">{code}</div>
  <p style="color:#94a3b8;font-size:13px;margin:20px 0 0">
    This code expires in {mins} minutes. {ignore}
  </p>
</div>"""
    return subject, html, text


async def _send_resend(to_email: str, subject: str, html: str, text: str) -> None:
    name, email = _from()
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.resend_api_key}"},
            json={"from": f"{name} <{email}>", "to": [to_email], "subject": subject, "html": html, "text": text},
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
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)


async def send_otp_email(to_email: str, full_name: str, code: str, kind: str = "verify") -> None:
    """Email the OTP via the first configured provider. Providers (Resend/Brevo)
    raise EmailSendError on failure so signup can report it; SMTP/no-provider
    fall back to logging the code so local dev keeps working. kind = 'verify' | 'reset'."""
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
        # SMTP (blocked on Render) or unexpected — keep signup usable; code is logged.
        print(f"[DEV] OTP for {to_email}: {code}")
