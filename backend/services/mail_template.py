"""The one Notenix email design. Every email is built from these pieces so they all look alike.

layout(...) wraps a body in the branded card (logo, heading, buttons, footer with support@notenix.com).
Pieces: para, code_box, login_box, info_table, bars, topic_list, callout.
Inline styles and tables only: that is what Gmail, Outlook and Apple Mail render reliably.
"""
from html import escape
from urllib.parse import quote
from config import settings

BRAND, INK, MUTED, FAINT, LINE, SOFT = "#5444DC", "#151829", "#475569", "#94a3b8", "#e2e8f0", "#f8fafc"
GOOD, OK, WEAK = "#059669", "#d97706", "#dc2626"
FONT = "Inter,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

WHY = {
    "parent": "You're receiving this as the parent or guardian on a Notenix account.",
    "student": "You're receiving this because you have a Notenix account.",
    "ks3": "You're receiving this because you started Notenix KS3 for your child.",
    "signup": "You're receiving this because this email address was entered on notenix.com.",
    "admin": "Admin alert for the Notenix team.",
}


def site(path: str = "/") -> str:
    return settings.public_url.rstrip("/") + path


def signin_url(login_id: str | None = None) -> str:
    """notenix.com/login with the user ID already filled in."""
    return site("/login") + (f"?id={quote(login_id)}" if login_id else "")


def first_name(full_name: str | None, fallback: str = "there") -> str:
    return escape((full_name or fallback).split(" ")[0])


# ── Pieces ─────────────────────────────────────────────────────────────────────

def para(html: str) -> str:
    return f'<p style="margin:0 0 14px">{html}</p>'


def button(url: str, label: str, primary: bool = True) -> str:
    bg, fg = (BRAND, "#ffffff") if primary else ("#ffffff", BRAND)
    return (f'<a href="{url}" style="display:inline-block;background:{bg};color:{fg};border:1.5px solid {BRAND};'
            f'text-decoration:none;font-weight:600;font-size:14px;line-height:20px;padding:11px 20px;'
            f'border-radius:10px;margin:0 8px 8px 0">{escape(label)}</a>')


def code_box(code: str, minutes: int) -> str:
    """Big one-time code; one tap selects it on phones (user-select:all)."""
    return (f'<div style="font-size:34px;font-weight:800;letter-spacing:10px;background:#EEF2FF;color:{BRAND};'
            f'text-align:center;padding:18px 10px;border-radius:14px;margin:6px 0 10px;'
            f'-webkit-user-select:all;user-select:all;font-family:Menlo,Consolas,monospace">{escape(code)}</div>'
            f'<p style="margin:0 0 14px;font-size:13px;color:{FAINT}">Expires in {minutes} minutes.</p>')


def login_box(login_id: str, child: str | None = None) -> str:
    """The user ID in its own box (one tap selects it) plus a sign-in link that fills it in."""
    who = f"{first_name(child)}'s Notenix user ID" if child else "Your Notenix user ID"
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 16px">'
            f'<tr><td style="background:#EEF2FF;border-radius:12px;padding:14px 16px">'
            f'<div style="font-size:12px;color:{MUTED}">{who}</div>'
            f'<div style="font-size:17px;font-weight:700;color:{INK};margin-top:4px;font-family:Menlo,Consolas,monospace;'
            f'-webkit-user-select:all;user-select:all">{escape(login_id)}</div>'
            f'<div style="font-size:12px;color:{MUTED};margin-top:6px">Tap the ID to select it, or '
            f'<a href="{signin_url(login_id)}" style="color:{BRAND};font-weight:600">sign in with it filled in</a>.</div>'
            f'</td></tr></table>')


def info_table(rows: list[tuple[str, str]]) -> str:
    """Label / value rows (values are already-escaped HTML)."""
    tr = "".join(f'<tr><td style="padding:7px 12px 7px 0;color:{MUTED};font-size:13px;white-space:nowrap;vertical-align:top">'
                 f'{escape(k)}</td><td style="padding:7px 0;color:{INK};font-size:14px;font-weight:600">{v}</td></tr>'
                 for k, v in rows)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-top:1px solid {LINE};'
            f'border-bottom:1px solid {LINE};margin:4px 0 18px">{tr}</table>')


def callout(title: str, big: str, note: str = "") -> str:
    return (f'<div style="background:{SOFT};border:1px solid {LINE};border-radius:12px;padding:14px 16px;margin:16px 0">'
            f'<div style="font-size:12px;color:{MUTED}">{escape(title)}</div>'
            f'<div style="font-size:18px;font-weight:700;color:{INK};margin-top:2px">{big}</div>'
            + (f'<div style="font-size:12px;color:{MUTED};margin-top:4px">{note}</div>' if note else "") + "</div>")


def color_for(pct: int) -> str:
    return GOOD if pct >= 70 else OK if pct >= 50 else WEAK


def _bar(pct: int, color: str) -> str:
    pct = max(0, min(100, pct))
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="height:8px;background:#f1f5f9;'
            f'border-radius:99px"><tr><td width="{max(pct, 2)}%" style="background:{color};border-radius:99px;height:8px;'
            f'font-size:0;line-height:0">&nbsp;</td><td style="font-size:0;line-height:0">&nbsp;</td></tr></table>')


def bars(rows: list[tuple[str, int, int | None]]) -> str:
    """(label, percent, change or None) per row."""
    out = ""
    for name, pct, change in rows:
        delta = "" if change is None else (
            f' <span style="color:{GOOD if change >= 0 else WEAK};font-size:12px">{"▲" if change >= 0 else "▼"} {abs(change)}</span>')
        out += (f'<tr><td style="padding:8px 0;width:30%;color:{INK};font-weight:600">{escape(name)}</td>'
                f'<td style="padding:8px 10px">{_bar(pct, color_for(pct))}</td>'
                f'<td style="padding:8px 0;width:74px;text-align:right;color:{INK};font-weight:700">{pct}%{delta}</td></tr>')
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:4px 0 6px">{out}</table>'


def topic_list(items: list[dict], title: str, color: str) -> str:
    if not items:
        return ""
    lis = "".join(f'<li style="margin:3px 0"><b style="color:{INK}">{escape(t["topic"])}</b> '
                  f'<span style="color:{FAINT}">({escape(t["subject"])}, {t["pct"]}%)</span></li>' for t in items)
    return (f'<p style="margin:16px 0 4px;color:{color};font-weight:700;font-size:12px;text-transform:uppercase;'
            f'letter-spacing:.5px">{escape(title)}</p><ul style="margin:0 0 6px;padding-left:18px">{lis}</ul>')


def subheading(text: str) -> str:
    return f'<p style="margin:18px 0 6px;color:{INK};font-weight:700">{escape(text)}</p>'


# ── The layout ─────────────────────────────────────────────────────────────────

def layout(*, preheader: str, heading: str, body: str, buttons: list[tuple[str, str]] | None = None,
           audience: str = "student", tagline: str = "") -> str:
    """buttons: [(url, label), ...]; the first is the main (filled) button."""
    btns = "".join(button(u, l, i == 0) for i, (u, l) in enumerate(buttons or []))
    logo = site("/brand/notenix-email-logo.png")
    tag = (f'<td style="padding-left:10px;font-size:13px;color:{FAINT};vertical-align:middle">{escape(tagline)}</td>'
           if tagline else "")
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>{escape(heading)}</title></head>
<body style="margin:0;padding:0;background:#f1f5f9">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{escape(preheader)}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border:1px solid {LINE};border-radius:16px">
<tr><td style="padding:26px 28px 0">
  <table role="presentation" cellpadding="0" cellspacing="0"><tr>
    <td style="vertical-align:middle"><img src="{logo}" width="135" height="40" alt="Notenix" style="display:block;border:0;outline:none;height:40px;width:135px;font:700 20px {FONT};color:{INK}"></td>{tag}
  </tr></table>
</td></tr>
<tr><td style="padding:22px 28px 8px;font-family:{FONT};color:{MUTED};font-size:15px;line-height:1.65">
  <h1 style="font-size:22px;line-height:1.3;color:{INK};margin:0 0 14px;font-weight:700">{escape(heading)}</h1>
  {body}
  {f'<div style="margin-top:18px">{btns}</div>' if btns else ''}
</td></tr>
<tr><td style="padding:10px 28px 26px;font-family:{FONT}">
  <div style="border-top:1px solid {LINE};padding-top:16px;font-size:13px;line-height:1.6;color:{MUTED}">
    Questions? Just reply to this email, or write to
    <a href="mailto:{settings.support_email}" style="color:{BRAND};font-weight:600;text-decoration:none">{settings.support_email}</a>.
  </div>
  <div style="font-size:12px;line-height:1.6;color:{FAINT};margin-top:8px">
    {escape(WHY.get(audience, WHY["student"]))}<br>Notenix, a unit of Beyond Groups ·
    <a href="{site('/')}" style="color:{FAINT}">notenix.com</a>
  </div>
</td></tr>
</table>
</td></tr></table></body></html>"""


def text_footer() -> str:
    return f"\n\nQuestions? Reply to this email or write to {settings.support_email}.\nNotenix · notenix.com"
