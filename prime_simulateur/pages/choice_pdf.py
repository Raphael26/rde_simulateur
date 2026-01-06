import os

import reflex as rx
from prime_simulateur.components import text_styles as ts
from prime_simulateur import prime_simulateur as ps
from prime_simulateur.admin.mpr_table import *
import os
from dotenv import load_dotenv
from typing import Optional, Any
from supabase import create_client, Client
import json

load_dotenv()

BUCKET_NAME = "fiches-operations"

# Initialize Supabase client
try:
    # Supabase connection
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY"),
    )
except Exception as e:
    print(f"Error initializing supabase clients: {e}")


def read_file_from_bucket(
    supabase_client,
    bucket_name: str,
    file_path: str,
    file_type: str = "txt",
    encoding: str = "utf-8",
) -> Any:
    # Read file from bucket
    try:
        raw = supabase_client.storage \
            .from_(bucket_name) \
            .download(file_path)
    except Exception as e:
        print(repr(e))

    if file_type == "txt":
        return raw.decode(encoding)
    elif file_type == "json":
        return json.loads(raw)


def badge_pdf(pdf_name) -> rx.Component:
    pdf_code = pdf_name.replace(".pdf", "").strip()
    pdf_code = f"   {pdf_code}"
    return rx.center(
        rx.badge(
            rx.flex(
                rx.text(
                    pdf_code,
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

def pdf_preview_modal(pdf_name):
    return rx.dialog.root(
        rx.dialog.trigger(
            badge_pdf(pdf_name),
        ),
        rx.cond(
            ps.MultiStepFormState.show_preview,
            rx.dialog.content(
                rx.html(
                    f'<iframe src="/downloaded_pdfs/{pdf_name}" width=525px height=600px style="border: 1px solid #E2E8F0; border-radius: 8px;";"></iframe>',
                ),
            ),
        ),
    )

def badge_mpr(pdf_name) -> rx.Component:
    print(pdf_name)
    ps.MultiStepFormState.set_pdf_to_check(filename=pdf_name)
    return rx.center(
        rx.cond(
            ps.MultiStepFormState.find_in_linked_articles,
            rx.badge(
                rx.flex(
                    rx.text(
                        "Articles MaPrimeRénov' (MPR)",
                        weight="medium",
                    ),
                    rx.icon("link", size=15),
                    direction="row",
                    # gap="6",
                    spacing="2",
                    align="center",
                ),
                #on_click=rx.redirect(ps.MultiStepFormState.all_linked_articles),
                cursor="pointer",
                size="1",
                radius="large",
            ),
            #rx.text("pas concerné")
        ),
        #on_mount=ps.MultiStepFormState.find_in_linked_articles(pdf_name),
    )

def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text



def pdf_item(pdf_file):
    filename = pdf_file[0]
    description = pdf_file[1]
    #ps.MultiStepFormState.set_pdf_to_check(filename=filename.to(str))
    #print(f"filename is {ps.MultiStepFormState.pdf_to_check}")
    return rx.hstack(
        rx.box(
            rx.hstack(
                rx.text(
                    description,
                    font_weight="medium",
                    text_overflow="ellipsis",
                    overflow="hidden",
                    title=filename,
                    on_click=lambda: ps.MultiStepFormState.set_selected_pdf(filename, description),
                ),
                pdf_preview_modal(filename),
                badge_mpr(filename),
            ),
            #on_mount=ps.MultiStepFormState.set_pdf_to_check(pdf_file),
            width="100%",
            height="100%",
            cursor="pointer",
            #padding="1%",
            _hover={"background": "rgba(13, 36, 44, 0.2)"},
            border_radius="md",
        ),
        width="100%",
        height="100%",
        spacing="1",
    )

def display_linked_article(article):
    return rx.table.row(
        rx.table.cell(
            #pdf_settings_modal(article["pdf_file"])
            rx.text(article["pdf_file"].to(str).replace(".pdf", "").strip())
        ),
        rx.table.cell(
            rx.link(
                article["link_article"].to(str).replace("https://www.legifrance.gouv.fr/loda/article_lc/", "").strip(),
                href=article["link_article"],
                cursor="pointer",
            )
        ),
    )

def mpr_list_modal():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.badge(
                rx.flex(
                    rx.text(
                        "Articles MaPrimeRénov' (MPR)",
                        weight="medium",
                    ),
                    rx.icon("link", size=15),
                    direction="row",
                    spacing="2",
                    align="center",
                ),
                on_click=ps.MultiStepFormState.toggle_mpr_list,
                cursor="pointer",
                size="1",
                radius="large",
            )
        ),
        rx.dialog.content(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Nom"),
                        rx.table.column_header_cell("Lien"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        ps.MultiStepFormState.all_linked_articles,
                        display_linked_article,
                    ),
                ),
                width="100%",
            ),
        ),
    )

@rx.page(route="/choice-pdf", title="RDE Simulateur")
def page_pdf():
    content = rx.vstack(
        rx.hstack(
            rx.spacer(),
            rx.center(
                rx.heading(
                    "Liste des fiches",
                    size="5",
                    color="#0d242c"
                ),
            ),
            rx.spacer(),
            rx.cond(
                (ps.MultiStepFormState.sector == "Résidentiel"),
                mpr_list_modal()
            ),
            width="100%",
        ),
        rx.cond(
            ps.MultiStepFormState.research_input != "",
            rx.vstack(
                rx.scroll_area(
                    rx.flex(
                        rx.foreach(ps.MultiStepFormState.keyword_search_pdf, pdf_item),
                        #on_mount=ps.MultiStepFormState.fetch_linked_articles,
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
                    bg="#f9f9fb",
                    type="always",
                    scrollbars="vertical",
                    class_name="shadow-md border border-gray-200",
                    style={"height": 300, "width": 1000},
                ),
                #on_mount=ps.MultiStepFormState.init_research_input,
            ),
            rx.scroll_area(
                rx.flex(
                    rx.foreach(ps.MultiStepFormState.pdf_mapping, pdf_item),
                    on_mount=ps.MultiStepFormState.fetch_linked_articles,
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
                bg="#f9f9fb",
                type="always",
                scrollbars="vertical",
                class_name="shadow-md border border-gray-200",
                style={"height": 300, "width": 1000},
            ),
        ),
        on_mount=ps.MultiStepFormState.show_sector_toast,
        align="center"
    )
    return ps.multi_step_layout(content, 80)
