import json
from typing import Tuple, Optional, Literal, List, Any

from sqlalchemy import and_, select

from back.auth_class import AuthState
from models.MprArticles import MprArticles
from models.models import CustomerData
import ast
from datetime import datetime
from sqlalchemy import and_

import reflex as rx
from reflex.event import EventSpec

from models.simulation import SimulationResult
from prime_simulateur import prime_simulateur as ps

SortColumn = Literal[
    "id",
    "date_simulation",
    "description",
    "secteur",
    "typologie",
]
SortOrder = Literal["asc", "desc"]



class MprState(rx.State):
    query: str = ""
    selected_simulation_id: Optional[int] = None
    selected_simulation: dict = {}
    selected_simulation_inputs_dict: dict = {}
    result_count: int = 1
    every_pdf: dict[str, str] = {}
    show_pdf_settings: bool = False
    selected_pdf: str = ""
    link_to_bind: str = ""
    all_linked_articles: list[dict] = []

    COLUMN_MAPPING: List[Tuple[str, str]] = [
        ("ID", "id"),
        ("Fiche", "nom"),
        ("Date signature", "chosen_date"),
        ("Département", "departement"),
        ("Nom de la fiche", "description"),
        ("Montant en euro", "result_eur"),
        ("Montant en cumacs", "result_cumacs"),
        ("Secteur", "secteur"),
        ("Typologie", "typologie")
    ]


    @rx.event
    def set_selected_pdf(self, pdf):
        """Handles clicking on a customer row. Selects the customer or deselects if already selected."""
        print(self.selected_pdf)
        self.selected_pdf = pdf

    @rx.event
    def set_link(self, link):
        self.link_to_bind = link

    @rx.event
    def add_article(self):
        pdf = self.selected_pdf
        link = self.link_to_bind
        with rx.session() as session:
            article = MprArticles(pdf_file=pdf, link_article=link, duration=5000)
            session.add(article)
            session.commit()
            self.fetch_linked_articles()
        return rx.toast(
            f"Article {link.replace("https://www.legifrance.gouv.fr/loda/article_lc/", "").strip()} lié à opération {pdf} !",
            duration="5000"
        )
            #return rx.toast(f"Lien {link} lié à article {pdf}")

    @rx.event
    def remove_linked_article(self, pdf_file, link_article):
        with rx.session() as session:
            article = session.exec(
                MprArticles.select().where(
                    and_(
                        MprArticles.pdf_file == pdf_file,
                        MprArticles.link_article == link_article,
                    )
                )
            ).first()
            if article:
                session.delete(article)
                session.commit()
                self.all_linked_articles = [
                    a for a in self.all_linked_articles
                    if not (a.get("pdf_file") == pdf_file and a.get("link_article") == link_article)
                ]
                return rx.toast(
            f"Article {link_article.replace("https://www.legifrance.gouv.fr/loda/article_lc/", "").strip()} supprimé pour opération {pdf_file} !",
            duration="5000"
        )

    def fetch_linked_articles(self):
        with rx.session() as session:
            all_simulations = session.exec(
                MprArticles.select()
            ).all()
            if all_simulations:
                sorted_linked_articles = sorted(all_simulations, key=lambda sim: sim.id)
                self.all_linked_articles = [
                    {**sim.__dict__, "order": idx + 1}
                    for idx, sim in enumerate(sorted_linked_articles)
                ]
                print(f"linked articles are : {self.all_linked_articles}")
            else:
                self.all_linked_articles = []


    @rx.event
    def get_all_pdf(self):
        json_path = 'assets/fiche_names_mapping.json'
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            matches = {k: v for k, v in data.items()}
            self.every_pdf = matches
        except FileNotFoundError:
            return {"error": f"JSON not found at {json_path}"}
        except json.JSONDecodeError:
            return {"error": "Error decoding JSON"}

    def open_settings(self):
        print("open setting")
        self.show_pdf_settings = True

def badge_pdf(pdf_name) -> rx.Component:
    pdf_code = pdf_name.replace(".pdf", "").strip()
    pdf_code = f"   {pdf_code}"
    return rx.center(
        rx.badge(
            rx.flex(
                rx.text(
                    pdf_code,
                    font_family="Open Sans",
                    weight="medium",
                ),
                rx.icon("file-text", size=15),
                direction="row",
                #gap="6",
                spacing="2",
                align="center",
            ),
            on_click=lambda: ps.MultiStepFormState.open_preview,
            cursor="pointer",
            size="1",
            #padding="0.5em 1em",
            radius="large",
        )
    )

def pdf_settings_modal(pdf_name):
    return rx.dialog.root(
        rx.dialog.trigger(
            badge_pdf(pdf_name),
        ),
        rx.cond(
            MprState.open_settings(),
            rx.dialog.content(
                rx.hstack(
                    rx.html(
                    f'<iframe src="/downloaded_pdfs/{pdf_name}" width=525px height=600px style="border: 1px solid #E2E8F0; border-radius: 8px;";"></iframe>',
                    ),
                ),

                width="100%"
            ),
        ),
    )

def pdf_item(pdf_file):
    filename = pdf_file[0]
    description = pdf_file[1]
    return rx.hstack(
        rx.box(
            rx.hstack(
                rx.text(
                    description,
                    font_weight="medium",
                    font_family="Open Sans",
                    text_overflow="ellipsis",
                    overflow="hidden",
                    title=filename,
                    on_click=lambda: MprState.set_selected_pdf(filename),
                ),
                pdf_settings_modal(filename),
            ),
            width="100%",
            height="100%",
            cursor="pointer",
            _hover={"background": "rgba(13, 36, 44, 0.2)"},
            border_radius="md",
        ),
        width="100%",
        height="100%",
        spacing="1",
    )

def list_every_pdf():
    return rx.scroll_area(
        rx.flex(
            rx.foreach(MprState.every_pdf, pdf_item),
            width="100%",
            align_items="stretch",
            height="auto",
            direction="column",
            spacing="3",
        ),
        padding="1em",
        border="1px solid",
        border_radius="8px",
        border_color="#e8e8ec",
        bg="white",
        type="always",
        scrollbars="vertical",
        class_name="shadow-md border border-gray-200",
        style={"height": 500, "width": "80%"},
        on_mount=MprState.get_all_pdf(),
        margin="1em",
    ),
