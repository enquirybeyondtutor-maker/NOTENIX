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

    # Stripe (freemium)
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_id: str = ""

    # Freemium limits
    free_quiz_limit: int = 3

    # Admin — comma-separated emails auto-treated as admin (for /admin dashboard)
    admin_emails: str = ""

    # Email / SMTP (Gmail app password) — for signup OTP verification
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""          # e.g. beyondimagination608@gmail.com
    smtp_password: str = ""      # Google App Password (not the account password)
    smtp_from: str = ""          # falls back to smtp_user
    smtp_from_name: str = "Notenix"

    # OTP policy
    otp_expiry_minutes: int = 10
    otp_max_attempts: int = 5
    otp_resend_cooldown_seconds: int = 60
    dev_expose_otp: bool = False  # DEV ONLY: return the code in the API response for local testing. Never true in prod.


settings = Settings()
