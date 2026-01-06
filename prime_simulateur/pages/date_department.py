import reflex as rx
import reflex_chakra as rc
from prime_simulateur import prime_simulateur as ps
from prime_simulateur.components import text_styles as ts


def department_item(description):
    return rx.text(
        description,
        font_weight="medium",
        text_overflow="ellipsis",
        overflow="hidden",
        title=description,
        cursor="pointer",
        on_click=ps.MultiStepFormState.set_department(description),
    ),

@rx.page(route="/date-department", title="RDE Simulateur")
def page_date_departement():
    ps.MultiStepFormState.set_page_progress(2)
    list_department = ps.MultiStepFormState.get_list_departements
    content = rx.vstack(
        ts.title_text("Date prévue de signature :"),
        rx.box(
            rx.center(
                rx.input(
                    type="date",
                    name="date",
                    required=True,
                    size="3",
                    style={
                        "text_align": "center",
                        "appearance": "none",
                        "background_color": "white",
                        "font_size": "1.0em",
                        "width": "100%",
                    },
                    padding_x="20%",
                    value=ps.MultiStepFormState.date_signature,
                    on_change=ps.MultiStepFormState.set_date_signature,
                    align="center"
                ),
            ),
            style={
                "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                "border_radius": "8px",
                "width": "100%",
            },
            margin_bottom="4em",
        ),
        # rx.input(
        #     type="date",
        #     name="date",
        #     required=True,
        #     size="3",
        #     style={
        #         "text_align": "center",
        #         "background_color": "white",
        #         "font_size": "1.0em",
        #         "width": "100%",
        #     },
        #     value=ps.MultiStepFormState.date_signature,
        #     on_change=ps.MultiStepFormState.set_date_signature,
        #     align="center"
        # ),
        ts.title_text("Département :"),
        rx.vstack(
            rx.box(
            rx.center(
                rx.input(
                    placeholder="Recherchez un département",
                    on_change=ps.MultiStepFormState.set_research_department,
                    value=ps.MultiStepFormState.department,
                    width="100%",
                    size="3",
                    border_color="black",
                ),
            ),
            style={
                "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                "border_radius": "8px",
                "width": "100%",
            },
            ),
            rx.cond(
                ps.MultiStepFormState.research_department != "",
                rx.scroll_area(
                    rx.flex(
                        rx.foreach(ps.MultiStepFormState.list_department, department_item),
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
                    width="100%",
                    style={"height": 100},
                ),
                rx.text("")
            ),
            width="100%",
            spacing="0"
        ),
        # rx.box(
        #     rx.select(
        #         ps.MultiStepFormState.list_department,
        #         placeholder="Selectionnez votre département",
        #         value=ps.MultiStepFormState.department,
        #         on_change=ps.MultiStepFormState.set_department,
        #         required=True,
        #         size="3",
        #         border_radius="8px",
        #         width="100%",
        #         style={
        #             "background_color": "white",
        #             "font_size": "1.0em",
        #             "width": "100%",
        #             "border": "1px solid #e5e7eb",
        #         },
        #     ),
        #     style={
        #         "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
        #         "border_radius": "8px",
        #     },
        #     width="100%",
        # ),
        width="30%",
        wrap="wrap",
        align="center",
        padding="0.5em",
        spacing="2",
        margin_bottom="3em",
    )
    return ps.multi_step_layout(content, 20)
