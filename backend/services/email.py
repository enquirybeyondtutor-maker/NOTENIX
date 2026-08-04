"""Email delivery (Gmail SMTP) + OTP helpers for signup verification."""
import smtplib
import secrets
from email.message import EmailMessage
from fastapi.concurrency import run_in_threadpool
from config import settings


def generate_otp() -> str:
    """A 6-digit numeric one-time code."""
    return f"{secrets.randbelow(1_000_000):06d}"


def _build_message(to_email: str, full_name: str, code: str) -> EmailMessage:
    from_addr = settings.smtp_from or settings.smtp_user
    msg = EmailMessage()
    msg["Subject"] = f"{code} is your Notenix verification code"
    msg["From"] = f"{settings.smtp_from_name} <{from_addr}>"
    msg["To"] = to_email
    mins = settings.otp_expiry_minutes
    name = (full_name or "there").split(" ")[0]
    msg.set_content(
        f"Hi {name},\n\n"
        f"Your Notenix verification code is: {code}\n\n"
        f"It expires in {mins} minutes. If you didn't sign up, you can ignore this email.\n\n"
        f"— Notenix"
    )
    msg.add_alternative(
        f"""\
<div style="font-family:Inter,system-ui,sans-serif;max-width:440px;margin:0 auto;color:#0f172a">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:24px">
    <span style="display:inline-grid;place-items:center;width:32px;height:32px;border-radius:10px;background:#4F46E5;color:#fff;font-weight:700">N</span>
    <span style="font-size:17px;font-weight:700">Notenix</span>
  </div>
  <h1 style="font-size:20px;margin:0 0 8px">Verify your email</h1>
  <p style="color:#475569;margin:0 0 24px">Hi {name}, enter this code to finish creating your account.</p>
  <div style="font-size:34px;font-weight:800;letter-spacing:10px;background:#EEF2FF;color:#4F46E5;
              text-align:center;padding:18px;border-radius:14px">{code}</div>
  <p style="color:#94a3b8;font-size:13px;margin:20px 0 0">
    This code expires in {mins} minutes. If you didn't sign up for Notenix, you can safely ignore this email.
  </p>
</div>""",
        subtype="html",
    )
    return msg


def _send_sync(msg: EmailMessage) -> None:
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)


async def send_otp_email(to_email: str, full_name: str, code: str) -> None:
    """Email the OTP. If SMTP isn't configured, print it to the console (dev fallback)."""
    if not settings.smtp_user or not settings.smtp_password:
        print(f"[DEV] OTP for {to_email}: {code} (SMTP not configured — email not sent)")
        return
    msg = _build_message(to_email, full_name, code)
    try:
        await run_in_threadpool(_send_sync, msg)
    except Exception as e:  # don't leak SMTP internals to the client; log + fall back
        print(f"[WARN] Failed to send OTP email to {to_email}: {e}")
        print(f"[DEV] OTP for {to_email}: {code}")
