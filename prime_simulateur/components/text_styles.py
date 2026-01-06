import reflex as rx
import reflex_chakra as rc
import variables
from prime_simulateur import prime_simulateur as ps

def paragraph_text(paragraph):
    return rx.text(paragraph, size="4")

def title_text(title):
    return rx.heading(f"{title}", size="5", color="#0d242c")

def button_text(text, icon):
    return rx.button(
        rx.hstack(
            rx.icon(icon),
            text,
        ),
        size="4",
        padding="1em",
        style={
            "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
        },
        _hover={
            "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
            "transform": "scale(1.05)",
            "transition": "all 0.2s ease-in-out"
        },
        transition="all 0.2s ease-in-out",
    )