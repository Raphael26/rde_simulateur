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


@rx.page(route="/beneficiary", title="RDE Simulateur")
def page_beneficiary():
    content = rx.vstack(
        rx.heading(
            "Bénéficiaire :",
            size="5",
            color="#0d242c",
            margin_bottom="2em",
        ),
        rx.radio(
            ["Particulier", "Personne morale"],
            placeholder="...",
            value=ps.MultiStepFormState.beneficiary,
            width="100%",
            size="3",
            direction="row",
            required=True,
            on_change=lambda value: ps.MultiStepFormState.set_beneficiary(value),
            margin_bottom="10em",
        ),
        align_items="center",
    )
    return ps.multi_step_layout(content, 80)


