import reflex as rx
import variables
from prime_simulateur import prime_simulateur as ps
from prime_simulateur.components import text_styles as ts

def make_sector_card(option: dict) -> rx.Component:
    selected = ps.MultiStepFormState.sector == option["value"]
    icon_name = option["icon"]
    return rx.box(
        rx.vstack(
            rx.icon(
                tag=icon_name,
                size=rx.breakpoints(
                    initial=48,  # mobile
                    sm=64,
                    lg=100
                ),
                color="#368278",
            ),
            rx.text(
                option["label"],
                font_size=rx.breakpoints(
                    initial="0.9em",
                    sm="1.1em",
                    lg="1.2em"
                ),
                font_weight=rx.cond(
                    selected,
                    "bold",
                    "normal"
                ),
            ),
            align_items="center"
        ),
        bg="white",
        border=rx.cond(
            selected,
            "2px solid",
            "1px solid #ccc"
        ),
        border_color=rx.cond(
            selected,
            "#368278",
            "#ccc"
        ),
        border_radius="16px",
        padding="1.5rem",
        box_shadow=rx.cond(
            selected,
            "0 4px 6px rgba(0,0,0,0.1)",
            "0 6px 15px rgba(0, 0, 0, 0.25)"
        ),
        cursor="pointer",
        on_click=lambda: ps.MultiStepFormState.select_sector(option["value"], option["abbr"]),
        width="30%",
        height="36%",
        text_align="center",
        _hover={
            "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
            "transform": "scale(1.05)",
            "transition": "all 0.2s ease-in-out"
        },
        transition="all 0.2s ease-in-out",
    )

@rx.page(route="/sector", title="RDE Simulateur")
def page_sector():
    ps.MultiStepFormState.set_page_progress(3)
    contenu = rx.vstack(
        ts.title_text("Quel est le secteur de votre projet ?"),
        rx.hstack(
            rx.input(
                placeholder="Rechercher une fiche",
                value=ps.MultiStepFormState.research_input,
                on_change=ps.MultiStepFormState.set_research_input,
                width="100%"
            ),
            rx.button(
                rx.icon("search"),
                on_click=rx.redirect("/choice-pdf"),
                type="button"
            )
        ),
        rx.hstack(
            rx.foreach(
                variables.Variables.sector_dict_list,
                lambda option: make_sector_card(option)
            ),
            spacing="4",
            justify="center",
            wrap="wrap",
            width="50%",
            height="80%",
            padding="2em",
        ),
        width="100%",
        height="70vh",
        align_items="center",
    )

    return ps.multi_step_layout(contenu, 40)
