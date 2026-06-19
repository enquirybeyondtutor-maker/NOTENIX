from pydantic_settings import BaseSettings
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    secret_key: str = secrets.token_hex(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days

    # Database — defaults to SQLite, set DATABASE_URL to postgres for production
    database_url: str = "sqlite+aiosqlite:///./notenix.db"

    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_monthly_price_id: str = ""
    stripe_yearly_price_id: str = ""

    # Email (SMTP)
    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = "noreply@notenix.co.uk"
    mail_from_name: str = "Notenix"
    mail_server: str = "smtp.gmail.com"
    mail_port: int = 587
    mail_starttls: bool = True
    mail_ssl_tls: bool = False

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""

    # App
    frontend_url: str = "http://localhost:3000"
    chroma_persist_dir: str = "./chroma_db"
    app_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
