import reflex as rx
from reflex import Config
from sqlmodel import Field, SQLModel, Session, create_engine

config = rx.Config(
    app_name="prime_simulateur",
    db_url = "postgresql://postgres:WsFRRqGxUkEyZZHxECjfstKSHARGXclw@maglev.proxy.rlwy.net:25478/railway",
	show_built_with_reflex=False,
)
