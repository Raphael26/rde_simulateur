import reflex as rx
import variables
from prime_simulateur import prime_simulateur as ps
from prime_simulateur.components import text_styles as ts


def get_icon_by_typology(typology: str, color) -> rx.Component:
    icon_size = 30
    return rx.cond(
        typology == "Utilité",
        rx.icon(tag="plug", size=icon_size, color="#368278"),
        rx.cond(
            typology == "Bâtiment",
            rx.icon(tag="building", size=icon_size, color="#368278"),
            rx.cond(
                typology == "Enveloppe",
                rx.icon(tag="layers", size=icon_size, color="#368278"),
                rx.cond(
                    typology == "Équipement",
                    rx.icon(tag="cpu", size=icon_size, color="#368278"),
                    rx.cond(
                        typology == "Service",
                        rx.icon(tag="briefcase", size=icon_size, color="#368278"),
                        rx.cond(
                            typology == "Eclairage",
                            rx.icon(tag="lightbulb", size=icon_size, color="#368278"),
                            rx.cond(
                                typology == "Chaleur",
                                rx.icon(tag="thermometer", size=icon_size, color="#368278"),
                                rx.cond(
                                    typology == "Thermique",
                                    rx.icon(tag="flame", size=icon_size, color="#368278"),
                                )
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

def make_typology_card(option: dict) -> rx.Component:
    selected = ps.MultiStepFormState.typology == option["name"]
    return rx.box(
        rx.vstack(
            get_icon_by_typology(option["name"], "#368278"),
            rx.text(
                option["name"],
                font_size="1.2em",
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
            "0 8px 20px rgba(0, 0, 0, 0.25)"
        ),
        cursor="pointer",
        on_click=lambda: ps.MultiStepFormState.select_typology(option["name"], option["abbr"]),
        width="42%",
        height="42%",
        text_align="center",
        _hover={
            "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
            "transform": "scale(1.05)",
            "transition": "all 0.2s ease-in-out"
        },
        transition="all 0.2s ease-in-out",
    )


@rx.page(route="/typology", title="RDE Simulateur")
def page_typology():
    ps.MultiStepFormState.set_page_progress(4)
    content = rx.vstack(
        ts.title_text("Quelle est la typologie de votre projet ?"),
        # rx.text("Souhaitez-vous faire une recherche par mots clés ?"),
        # rx.radio(
        #     ["Oui", "Non"],
        #     value=ps.MultiStepFormState.research_manually,
        #     on_change=ps.MultiStepFormState.set_research_manually,
        #     direction="row",
        #     size="3",
        #     required=True,
        # ),
        rx.cond(
            ps.MultiStepFormState.research_manually == "Non",
            rx.hstack(
                rx.foreach(
                    ps.MultiStepFormState.available_typologies,
                    lambda option: make_typology_card(option)
                ),
                spacing="4",
                justify="center",
                wrap="wrap",
                width="40%",
                height="70%",
                padding="2em",
            ),
        ),
        width="100%",
        height="70vh",
        align_items="center",
    )
    return ps.multi_step_layout(content, 60)
