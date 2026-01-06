import datetime
import sqlmodel
import reflex as rx
from typing import Optional

class MprArticles(rx.Model, table=True):
    pdf_file: str
    link_article: str