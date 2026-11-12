from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Core
    database_url: str = "sqlite+aiosqlite:///./notenix.db"
    secret_key: str = "dev-secret-change-me"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # Anthropic
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"

    # URLs
    frontend_url: str = "http://localhost:3000"
    app_url: str = "http://localhost:8000"
    public_url: str = "https://www.notenix.com"  # used in notification email links

    # Manual payments (bank transfer / Wise). Nothing is charged automatically: students
    # transfer money, then an admin confirms it in /admin/requests.
    # PAYMENT_ACCOUNTS is a JSON list shown on the pay page, e.g.
    #   [{"label": "UK bank transfer (GBP)", "currency": "GBP",
    #     "details": {"Account holder": "...", "Sort code": "...", "Account number": "..."}},
    #    {"label": "India (UPI / bank)", "currency": "INR", "details": {"UPI ID": "..."}}]
    # Keep real details in the Render env, never in this public repo.
    payment_accounts: str = "[]"
    price_currency: str = "GBP"
    pro_price: float = 9.99           # per 30 days
    request_price: float = 0.0        # per requested test; 0 = free
    revision_price: float = 149.0     # full revision access for non-Beyond Tutors students, per year
    # Wise payment link for the £149 checkout (button + QR). Empty = bank details only.
    # Accounts in PAYMENT_ACCOUNTS can also carry their own "pay_link".
    revision_pay_link: str = "https://wise.com/pay/r/BeDOBG4eucVVAg0"
    pay_link_99: str = "https://wise.com/pay/r/pmJ_vlY6iKl8a8k"    # Wise card link, GBP 99 (one GCSE subject, SAT)
    pay_link_349: str = "https://wise.com/pay/r/76Ch6kq7sJpErfU"   # Wise card link, GBP 349 (all four GCSEs)

    # Freemium limits
    free_quiz_limit: int = 3

    # Data retention: student responses (typed answers + uploaded photos) are purged
    # this many days after submission. Marks, grades and feedback are kept. 0 = never.
    response_retention_days: int = 28

    # Admin — comma-separated emails auto-treated as admin (for /admin dashboard)
    admin_emails: str = ""

    # Email — for signup OTP verification.
    # Prefer an HTTPS email API (works on hosts that block SMTP, e.g. Render):
    resend_api_key: str = ""     # https://resend.com  (set RESEND_API_KEY)
    brevo_api_key: str = ""      # https://brevo.com   (set BREVO_API_KEY)
    support_email: str = "support@notenix.com"   # Reply-To on every email, and shown in the footer
    email_from: str = ""         # the verified sender address, e.g. noreply@notenix.com
    # SMTP fallback (used only if no API key is set; blocked on Render):
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""          # e.g. beyondimagination608@gmail.com
    smtp_password: str = ""      # Google App Password (not the account password)
    smtp_from: str = ""          # falls back to smtp_user
    smtp_from_name: str = "Notenix"

    # Accounts are issued by Beyond Tutors (admin panel). Public sign-up and
    # self-service password reset stay off unless OPEN_SIGNUP=true.
    open_signup: bool = False
    # One-off admin recovery: on boot, create/reset this account as admin with this password.
    # Set both in Render, sign in, then delete BOOTSTRAP_ADMIN_PASSWORD.
    bootstrap_admin_email: str = ""
    bootstrap_admin_password: str = ""
    student_id_domain: str = "beyondtutors.com"      # musa@beyondtutors.com (new IDs)
    # Every domain used for Notenix login IDs (no inbox behind them), comma-separated.
    # Older accounts were issued on thebeyondtutors.com, so it stays here.
    login_id_domains: str = "beyondtutors.com,thebeyondtutors.com"
    subscription_days: int = 365                     # £49 per year
    # Student subscription price per billing currency, JSON, e.g. {"GBP": 49, "AED": 229}.
    # Empty = the defaults in services/pricing.py.
    subscription_prices: str = ""
    # Notenix KS3 (Year 7-9): yearly price per currency (JSON, empty = defaults) and free trial length.
    ks3_prices: str = ""
    sat_prices: str = ""   # Notenix SAT yearly price per currency, JSON; empty = pricing.SAT_PRICES
    ks3_trial_days: int = 7
    ks3_help_trial_cap: int = 5      # homework-help questions during the free week
    ks3_help_monthly_cap: int = 30   # fair use for paying KS3 families
    ks3_id_domain: str = "notenix.com"              # KS3 trial user IDs: zara@notenix.com
    # Where trial emails send parents to continue, and to book a Beyond Tutors class.
    ks3_upgrade_url: str = "https://www.notenix.com/ks3/continue"
    book_class_url: str = "https://www.thebeyondtutors.com/book"
    trial_days: int = 7                              # free access around the trial class

    # Private key for the BT Sessions desktop app (/sync/*). Empty = sync disabled.
    gcse_bundle_prices: str = ""   # optional JSON to override pricing.GCSE_BUNDLE_PRICES
    gcse_prices: str = ""   # optional JSON {"GBP": 99, ...} to override pricing.GCSE_PRICES
    sync_key: str = ""
    sync_owner_email: str = "hello@thebeyondtutors.com"  # uploads from the app are owned by this account

    # How often a user may change their display name.
    name_change_cooldown_days: int = 60

    # OTP policy
    otp_expiry_minutes: int = 10
    otp_max_attempts: int = 5
    otp_resend_cooldown_seconds: int = 60
    dev_expose_otp: bool = False  # DEV ONLY: return the code in the API response for local testing. Never true in prod.


settings = Settings()
