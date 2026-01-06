from typing import Tuple, Optional, Literal, List, Any, Dict, Union

from sqlalchemy import and_, select

from back.auth_class import AuthState
from models.models import CustomerData
import ast
from datetime import datetime

import reflex as rx
import plotly.express as px

from reflex.event import EventSpec

from models.simulation import SimulationResult
from models.user import User
from prime_simulateur import prime_simulateur as ps
from prime_simulateur.admin.admin_history_table import AdminState
from prime_simulateur.components import history_table



SortColumn = Literal[
    "id",
    "date_simulation",
    "description",
    "secteur",
    "typologie",
]
SortOrder = Literal["asc", "desc"]


COLUMN_MAPPING: List[Tuple[str, str]] = [
        ("ID utilisateur", "id"),
        ("Identifiant", "username"),
        ("N° Téléphone", "phone_number"),
        ("Prénom", "first_name"),
        ("Nom", "last_name"),
    ]

def non_sortable_table_header(
    col_name: str,
) -> rx.Component:
    """Renders a non-sortable table header cell."""
    base_class = (
        "px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
    )
    text_align_class = rx.match(
        col_name,
        ("Revenue", "text-right"),
        ("Licenses", "text-center"),
        ("Active licenses", "text-center"),
        "text-left",
    )
    justify_content_val = rx.match(
        col_name,
        ("Revenue", "flex-end"),
        ("Licenses", "center"),
        ("Active licenses", "center"),
        "text-left",
    )
    combined_class = f"{base_class} {text_align_class}"
    header_content_inner = rx.el.div(
        col_name,
        class_name="flex",
    )
    return rx.el.th(
        rx.hstack(
            header_content_inner,
            scope="col",
            class_name=combined_class,
        )
    )


def table_header(
    col_data: rx.Var[Tuple[str, Optional[SortColumn]]],
) -> rx.Component:
    """Renders a table header cell, deciding if it's sortable or not."""
    col_name = col_data[0]
    column_key = col_data[1].to_string()
    return non_sortable_table_header(col_name)

def table_row(customer) -> rx.Component:
    """Renders a single row in the data table."""
    print(f"customer is: {customer}")
    return rx.el.tr(
        rx.foreach(
            AdminState.column_data_user,
            lambda col_data: get_cell_content_users(col_data[0], customer),
        ),
        #on_click=lambda: AdminState.select_simulation(customer),
        #class_name="w-full bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
    )

def get_cell_content_users(col_name: rx.Var[str], customer) -> rx.Component:
    """Gets the appropriate component for a specific cell based on column name."""
    base_class = "px-4 py-3 whitespace-nowrap text-sm"
    return rx.match(
        col_name,
        (
            "Ordre",
            rx.el.td(
                customer["order"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "ID utilisateur",
            rx.el.td(
                customer["id"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Identifiant",
            rx.el.td(
                customer["username"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "N° Téléphone",
            rx.el.td(
                customer["phone_number"],
                class_name=f"{base_class} font-medium text-gray-900 text-left",
            ),
        ),
        (
            "Prénom",
            rx.el.td(
                customer["first_name"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Nom",
            rx.el.td(
                customer["last_name"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
    )

def data_table() -> rx.Component:
    """The main data table component including search and results count."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.foreach(
                                AdminState.user_list,
                                table_header,
                            ),
                            class_name="bg-gray-50 border-b border-gray-200 whitespace-nowrap",
                        )
                    ),
                    rx.el.tbody(
                        rx.cond(
                            AuthState.filter_by_sector == True,
                            rx.foreach(
                                AuthState.simulations_sorted_by_sector,
                                table_row,
                            ),
                            rx.cond(
                                AuthState.filter_by_typology == True,
                                rx.foreach(
                                    AuthState.simulations_sorted_by_typology,
                                    table_row,
                                ),
                                rx.cond(
                                    AuthState.research_input != "",
                                    rx.foreach(
                                        AuthState.filtered_simulations,
                                        table_row,
                                    ),
                                    rx.foreach(
                                        AuthState.user_simulations,
                                        table_row,
                                    ),
                                ),
                            ),
                        ),
                        rx.cond(
                            AdminState.result_count == 0,
                            rx.el.tr(
                                rx.el.td(
                                    "No customers found matching your criteria.",
                                    class_name="px-4 py-3 text-center text-gray-500 italic",
                                )
                            ),
                            rx.fragment(),
                        ),
                        class_name="divide-y divide-gray-200",
                    ),
                    class_name="min-w-full min-h-full",
                ),
                style={
                    "maxHeight": "400px",  # Hauteur maximale
                    "overflowY": "auto",  # Scroll vertical
                }
            ),
            class_name="shadow overflow-hidden border border-gray-200 sm:rounded-lg overflow-x-auto overflow-y-auto",
        ),
        rx.el.div(
            rx.el.p(
                #AdminState.result_count.to_string() + " results",
                class_name="text-sm text-gray-500 mt-4",
            ),

            class_name="flex justify-end",
        ),
        #on_mount=AuthState.fetch_simulations_result_admin,
        class_name="bg-white p-6 rounded-lg shadow-md",
    )


def user_data_table():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.foreach(
                                COLUMN_MAPPING,
                                table_header,
                            ),
                            class_name="bg-gray-50 border-b border-gray-200 whitespace-nowrap",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            AdminState.user_list,
                            table_row,
                        ),
                        class_name="divide-y divide-gray-200",
                    ),
                    width="100%"
                ),
            ),
            on_mount=AdminState.fetch_all_user,
            class_name="shadow overflow-hidden border border-gray-200 sm:rounded-lg overflow-x-auto",
        ),
        class_name="bg-white p-6 rounded-lg shadow-md",
    )
