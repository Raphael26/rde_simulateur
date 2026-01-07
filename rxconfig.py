import reflex as rx
import os

# Get DATABASE_URL from environment variable (set in Railway)
database_url = os.getenv("DATABASE_URL", "")

# Railway uses postgres:// but SQLAlchemy requires postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Fallback for local development
if not database_url:
    database_url = "sqlite:///reflex.db"

# Get the public URL from environment (Railway sets RAILWAY_PUBLIC_DOMAIN)
public_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")

# Build config - only include api_url if we have a public domain
if public_domain:
    config = rx.Config(
        app_name="prime_simulateur",
        db_url=database_url,
        api_url=f"https://{public_domain}",
        show_built_with_reflex=False,
    )
else:
    config = rx.Config(
        app_name="prime_simulateur",
        db_url=database_url,
        show_built_with_reflex=False,
    )