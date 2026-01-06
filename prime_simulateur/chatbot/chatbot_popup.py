import reflex as rx
import reflex_chakra as rc
from prime_simulateur import prime_simulateur as ps
from prime_simulateur.components import text_styles as ts
from prime_simulateur.chatbot.state import State
from prime_simulateur.chatbot.style import *

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=answer_style),
            text_align="left",
        ),
        margin_y="1em",
    )


def chatbot():
    return rx.center(
        rx.box(
            rx.box(
                rx.text("Ask AI", color="#368278", size="3"),
                position="absolute",
                top="0.5em",
                left="0.5em",
                z_index="10",
            ),
            rx.box(
                rx.icon("circle-x", color="#368278", on_click=State.toggle_chat),
                position="absolute",
                top="0.5em",
                right="0.5em",
                z_index="10",
            ),
            rx.vstack(
                rx.scroll_area(
                    rx.foreach(
                        State.chat_history,
                        lambda messages: qa(messages[0], messages[1]),
                    ),
                    style={"height": "90%", "width": "100%"},
                    scrollbars="vertical",
                    type="always",
                ),
                rx.hstack(
                    rx.input(
                        value=State.question,
                        placeholder="Votre question ?",
                        on_change=State.set_question,
                        style=input_style,
                        size="3"
                    ),
                    rx.cond(
                        (State.question != ""),
                        rx.button(
                            rx.icon("send"),
                            on_click=State.answer,
                            style=button_style,
                        ),
                    ),
                    width="95%",
                    position="absolute",
                    bottom="1em"
                ),
                height="100%",
            ),
            width="60%",
            height="60%",
            padding="2em",
            border_radius="8px",
            style={
                "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
            },
            bg="white",
            border="8px",
            border_color="#a9c7c2",
            z_index="100",
            display="flex",
            flex_direction="column",
            position="relative",
        ),
        position="fixed",
        inset=0,
        z_index="1000",
    )

def floating_chat_button():
    return rx.box(
        rx.cond(
            State.chat_open,
            chatbot(),
            rx.button(
                rx.text("Ask AI"),
                rx.image("/RDE_icon.jpg", width="30%"),
                position="fixed",
                bottom="1.5rem",
                right="1.5rem",
                border_radius="full",
                box_shadow="lg",
                size="3",
                style={
                    "width": "10%",
                    "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
                },
                _hover={
                    "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
                    "transform": "scale(1.05)",
                    "transition": "all 1s ease-in-out"
                },
                on_click=State.toggle_chat,
            )
        ),
        justify="center"
    )