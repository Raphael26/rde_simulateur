import reflex as rx
import reflex_chakra as rc
import prime_simulateur.function_loader
from prime_simulateur import prime_simulateur as ps

def build_input_choices(data):
    input_choices = []
    for k, v in data.items():
        if isinstance(v, dict) and v:
            input_choices.append((k, list(v.keys()), False))
        else:
            input_choices.append((k, [], True))
    return input_choices


def select_box(item):
    return rx.box(
        rx.select(
            item[1].keys(),
            placeholder="Selectionnez une valeur ",
            width="100%",
            size="3",
            style={
                "background_color": "white",
                "font_size": "1.0em",
                "width": "100%",
                "border": "1px solid #e5e7eb",
            },
            on_change=lambda value: ps.MultiStepFormState.set_param(
                item[0],
                ps.MultiStepFormState.simulator_var_matching.get(item[0], item[0]),
                value
            ),
        ),
        style={
            "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
            "border_radius": "8px",
            "width": "100%",
        },
    )


def input_box(item):
    return rx.box(
        rx.input(
            placeholder="Saisissez une valeur",
            name=item[0],
            width="100%",
            size="3",
            required=True,
            variant="surface",
            style={
                "background_color": "white",
                "font_size": "1.0em",
                "width": "100%",
                "border": "1px solid #e5e7eb",
            },
            on_change=lambda value: ps.MultiStepFormState.set_param(
                item[0],
                ps.MultiStepFormState.simulator_var_matching.get(item[0], item[0]),
                value
            ),
        ),
        style={
            "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
            "border_radius": "8px",
            "width": "100%",
        },
    )

def display_inputs(input_choices):
    return rx.vstack(
        rx.foreach(
            input_choices,
            lambda item: rx.cond((ps.MultiStepFormState.simulator_function_requirements[item[0]]) &
                (ps.MultiStepFormState.simulator_function_requirements[item[0]].get('annotation') == "<class 'bool'>"),
                rx.select.root(
                    rx.text(f"{item[0].capitalize().replace("_", " ")}", font_weight="bold"),
                    rx.radio(
                        ["Oui", "Non"],
                        placeholder="...",
                        width="100%",
                        size="3",
                        direction="column",
                        required=True,
                        on_change=lambda value: ps.MultiStepFormState.set_param(item[0],
                            ps.MultiStepFormState.simulator_var_matching.get(item[0], item[0]), value
                        ),
                    ),
                    name=item[0],
                    width="100%",
                ),
                rx.cond(
                    item[1],
                    rx.select.root(
                        rx.text(f"{item[0].capitalize().replace("_", " ")}", font_weight="bold"),
                        select_box(item),
                        name=item[0],
                        width="100%",
                        justify="center",
                        required=True,
                    ),
                    rx.vstack(
                        rx.text(f"{item[0].capitalize().replace('_', ' ')}", font_weight="bold"),
                        input_box(item),
                        width="100%"
                    ),
                ),
            ),
        ),
        #rx.text(f"{ps.MultiStepFormState.simulator_result}€"),
        spacing="4",
        wrap="wrap",
        width="50%",
        padding="2em",
        justify="center",
    )


@rx.page(route="/simulator", title="RDE Simulateur")
def page_simulator():
    ps.MultiStepFormState.set_page_progress(5)
    content = rx.vstack(
        rx.heading("Entrez les données", size="6"),
        display_inputs(ps.MultiStepFormState.simulator_input_choices),
        width="100%",
        align_items="center",
    )
    return ps.multi_step_layout(content, 100)
