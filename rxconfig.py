#import reflex as rx
#from reflex import Config
#from sqlmodel import Field, SQLModel, Session, create_engine
#
#config = rx.Config(
#    app_name="prime_simulateur",
#    db_url = "postgresql://postgres:WsFRRqGxUkEyZZHxECjfstKSHARGXclw@maglev.proxy.rlwy.net:25478/railway",
#	show_built_with_reflex=False,
#)

import reflex as rx
import os

# Get DATABASE_URL from environment variable (set in Railway)
database_url = os.getenv("DATABASE_URL", "")

# Railway uses postgres:// but SQLAlchemy requires postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Fallback for local development (optional - remove or update as needed)
if not database_url:
    database_url = "sqlite:///reflex.db"  # Local SQLite for development

config = rx.Config(
    app_name="prime_simulateur",
    db_url=database_url,
    show_built_with_reflex=False,
)
