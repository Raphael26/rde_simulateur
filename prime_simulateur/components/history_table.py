from collections import defaultdict
from typing import Tuple, Optional, Literal, List, Any

from sqlalchemy import and_

from back.auth_class import AuthState
from models.models import CustomerData
import ast
from datetime import datetime

import reflex as rx
from reflex.event import EventSpec

from models.simulation import SimulationResult
from prime_simulateur import prime_simulateur as ps

def parse_date(date_str: str) -> Optional[datetime]:
    """Helper function to parse date strings into datetime objects.
    Handles common formats found in the data. Returns None if parsing fails.
    """
    try:
        return datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None

SortColumn = Literal[
    "id",
    "date_simulation",
    "description",
    "secteur",
    "typologie",
]
SortOrder = Literal["asc", "desc"]


class TableState(rx.State):
    query: str = ""
    selected_simulation_id: Optional[int] = None
    selected_simulation: dict = {}
    selected_simulation_inputs_dict: dict = {}
    selected_simulation_name: str = ""
    result_count: int = 1
    sort_order: SortOrder = "asc"
    sort_column: str = "id"
    sort_asc: bool = True
    search_term: str = ""
    sort_prime: bool = False
    sort_sector: bool = False
    sort_typology: bool = False
    user_simulations: list[dict] = []


    COLUMN_MAPPING: List[Tuple[str, str]] = [
        ("ID", "id"),
        ("Nom simulation", "name"),
        ("Fiche", "nom"),
        ("Date simulation", "date_simulation"),
        ("Département", "departement"),
        ("Nom de la fiche", "description"),
        ("Bénéficiaire", "beneficiary"),
        ("Montant en euro", "result_eur"),
        ("Montant en cumacs", "result_cumacs"),
        ("Secteur", "secteur"),
        ("Typologie", "typologie"),
        ("Date signature", "chosen_date"),
    ]

    @rx.var
    def column_data(
            self,
    ) -> List[Tuple[str, Optional[SortColumn]]]:
        """Returns the master list of column configurations (name and sort key)."""
        return self.COLUMN_MAPPING

    @rx.event
    def select_simulation(self, simulation):
        """Handles clicking on a customer row. Selects the customer or deselects if already selected."""
        print(self.selected_simulation_id)
        self.selected_simulation_id = simulation["id"]
        self.selected_simulation = simulation
        self.selected_simulation_inputs_dict = ast.literal_eval(simulation["parameters"])
        self.selected_simulation_name = simulation["name"]
        print(self.selected_simulation)
        print(self.selected_simulation_inputs_dict)
        return rx.redirect("/details")

    @rx.event
    def sort_by(self, column_key: SortColumn):
        """Handles clicking on a sortable table header. Updates the sort column and order."""
        if self.sort_column == column_key:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_column = column_key
            self.sort_order = "asc"

    def generate_fake_data(self):
        """Generates fake data for the dashboard."""
        self.key_metrics = [
            {
                "title": "Moyenne des aides en euros",
                "value": 12, #AuthState.get_average_euro,
            },
            {
                "title": "Moyenne des cumacs",
                "value": 6,
            },
        ]

    def set_sort(self, column: str):
        if self.sort_by == column:
            self.sort_asc = not self.sort_asc
        else:
            self.sort_by = column
            self.sort_asc = True

    def set_prime_status(self):
        self.sort_prime = not self.sort_prime

    def set_sector_status(self):
        self.sort_sector = not self.sort_sector

    def set_typology_status(self):
        self.sort_typology = not self.sort_typology

    @rx.event
    def set_search_term(self, term: str):
        """Updates the search term based on user input."""
        self.search_term = term
        if self.selected_simulation_id is not None:
            found = any(
                (
                    simulation["id"] == self.selected_simulation_id
                    for simulation in self.user_simulations
                )
            )
            if not found:
                self.selected_simulation_id = None

    @rx.event
    def remove_simulation(self):
        with rx.session() as session:
            simulation = session.exec(
                SimulationResult.select().where(
                    and_(
                        SimulationResult.user_id == self.selected_simulation["user_id"],
                        SimulationResult.id == self.selected_simulation_id,
                    )
                )
            ).first()
            if simulation:
                session.delete(simulation)
                session.commit()
                return rx.redirect("/dashboard")

    @rx.event
    def set_selected_simulation_name(self, value):
        self.selected_simulation_name = value

    @rx.event
    def save_simulation_name(self):
        with rx.session() as session:
            simulation = session.exec(
                SimulationResult.select().where(
                    and_(
                        SimulationResult.user_id == self.selected_simulation["user_id"],
                        SimulationResult.id == self.selected_simulation_id,
                    )
                )
            ).first()
            if simulation:
                simulation.name = self.selected_simulation_name.capitalize()
                session.commit()
                return rx.redirect("/dashboard")


def sort_icon(column_key: SortColumn) -> rx.Component:
    """Displays sort direction icon or a neutral sortable indicator."""
    icon_base_class = (
        "ml-1 inline-block w-3 h-3 transition-colors duration-150 ease-in-out"
    )
    active_icon_class = f"{icon_base_class} text-gray-700"
    inactive_icon_class = f"{icon_base_class} text-gray-400 group-hover:text-gray-600"
    is_active_column = TableState.sort_column == column_key
    return rx.cond(
        is_active_column,
        rx.cond(
            TableState.sort_order == "asc",
            rx.icon(
                "arrow-up",
                size=12,
                class_name=active_icon_class,
            ),
            rx.icon(
                "arrow-down",
                size=12,
                class_name=active_icon_class,
            ),
        ),
        rx.icon(
            "chevrons-up-down",
            size=12,
            class_name=inactive_icon_class,
        ),
    )

def get_sector_tag(sector: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        sector,
        class_name=rx.match(
            sector,
            (
                "Industrie",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-red-100 text-red-800",
            ),
            (
                "Résidentiel",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-pink-100 text-pink-800",
            ),
            (
                "Tertiaire",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-slate-100 text-slate-800",
            ),
            (
                "Réseau",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-purple-100 text-purple-800",
            ),
            (
                "Agriculture",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-green-100 text-green-800",
            ),
            (
                "Transport",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-teal-100 text-teal-800",
            ),
            "px-2 py-1 text-xs text-center font-medium rounded-full bg-gray-100 text-gray-800"
        ),
    )

def get_typology_tag(typology: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        typology,
        class_name=rx.match(
            typology,
            (
                "Utilité",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-gray-100 text-gray-800",
            ),
            (
                "Bâtiment",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-yellow-100 text-yellow-800",
            ),
            (
                "Enveloppe",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-stone-100 text-stone-800",
            ),
            (
                "Thermique",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-purple-100 text-purple-800",
            ),
            (
                "Équipement",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-rose-100 text-rose-800",
            ),
            (
                "Services",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-blue-100 text-blue-800",
            ),
            (
                "Eclairage",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-yellow-100 text-yellow-800",
            ),
            (
                "Chaleur",
                "px-2 py-1 text-xs text-center font-medium rounded-full bg-orange-100 text-orange-800",
            ),
            "px-2 py-1 text-xs text-center font-medium rounded-full bg-gray-100 text-gray-800"
        ),
    )

def filter_status_button(
    label: str,
    is_active: rx.Var[bool],
    on_click: EventSpec,
) -> rx.Component:
    return rx.el.button(
        rx.el.span(
            rx.icon(tag="plus", size=14, class_name="mr-1"),
            label,
            class_name="flex",
        ),
        rx.icon(tag="chevron_down", size=14, class_name="ml-1"),
        on_click=on_click,
        class_name="flex px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1",
        aria_expanded=is_active,
    )

def sortable_table_header(col_name: str, column_key: SortColumn) -> rx.Component:
    """Renders a sortable table header cell."""
    base_class = "px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider group"
    sortable_class = f"{base_class} cursor-pointer"
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
        "flex-start",
    )
    combined_class = f"{sortable_class} {text_align_class}"
    header_content_inner = rx.el.div(
        col_name,
        sort_icon(column_key),
        class_name="flex group-hover:text-gray-700 transition-colors duration-150 ease-in-out",
        style={"justify_content": justify_content_val},
    )
    return rx.el.th(
        rx.vstack(
            header_content_inner,
            scope="col",
            class_name=combined_class,
            on_click=lambda: TableState.sort_by(column_key),
        )
    )


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
        "flex-start",
    )
    combined_class = f"{base_class} {text_align_class}"
    header_content_inner = rx.el.div(
        col_name,
        class_name="flex",
        style={"justify_content": justify_content_val},
    )
    return rx.el.th(
        rx.vstack(
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
    # return rx.el.th(
    #     column_key
    # )
    return rx.cond(
        column_key,
        sortable_table_header(col_name, column_key.to(SortColumn)),
        non_sortable_table_header(col_name),
    )

def table_row(simulation) -> rx.Component:
    """Renders a single row in the data table."""
    return rx.el.tr(
        rx.foreach(
            TableState.column_data,
            lambda col_data: get_cell_content(col_data[0], simulation),
        ),
        on_click=lambda: TableState.select_simulation(simulation),
        #class_name="w-full bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
        class_name=rx.cond(
            TableState.selected_simulation_id == simulation["id"],
            "w-full bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
            "w-full border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors duration-150 ease-in-out",
        ),
    )

def get_cell_content(col_name: rx.Var[str], customer) -> rx.Component:
    """Gets the appropriate component for a specific cell based on column name."""
    base_class = "px-4 py-3 whitespace-nowrap text-sm"
    tag_sector = get_sector_tag(customer["secteur"])
    tag_typology = get_typology_tag(customer["typologie"])
    print(customer)
    return rx.match(
        col_name,
        (
            "ID",
            rx.el.td(
                customer["order"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Nom simulation",
            rx.el.td(
                customer["name"],
                class_name=f"{base_class} font-medium text-gray-900 text-left",
            ),
        ),
        (
            "Fiche",
            rx.el.td(
                customer["fiche"],
                class_name=f"{base_class} font-medium text-gray-900 text-left",
            ),
        ),
        (
            "Date signature",
            rx.el.td(
                customer["chosen_date"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Département",
            rx.el.td(
                customer["departement"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Nom de la fiche",
            rx.el.td(
                customer["description"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Bénéficiaire",
            rx.el.td(
                customer["beneficiary"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Montant en euro",
            rx.el.td(
                f"{customer["result_eur"]:.2f} €",
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Montant en cumacs",
            rx.el.td(
                f"{customer["result_cumacs"]:.2f}",
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Secteur",
            rx.el.td(
                tag_sector,
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Typologie",
            rx.el.td(
                tag_typology,
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Date simulation",
            rx.el.td(
                customer["date_simulation"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
    )

def sortable_th(label: str, column: str, size_percent: int) -> rx.Component:
    arrow = rx.cond(
        TableState.sort_by == column,
        rx.el.span(""),
    )
    return rx.el.th(
        rx.el.div(
            rx.el.span(label),
            arrow,
            class_name="flex items-center gap-1 cursor-pointer justify-center",
            on_click=TableState.set_sort(column),
        ),
        class_name="py-2 text-lg font-medium text-gray-500 uppercase text-center",
        width=f"{size_percent}%",
    )

def filter_status_button(
    label: str,
    is_active: rx.Var[bool],
    on_click: EventSpec,
) -> rx.Component:
    return rx.el.button(
        rx.el.span(
            rx.icon(tag="plus", size=14, class_name="mr-1"),
            label,
            class_name="flex items-center",
        ),
        rx.icon(tag="chevron_down", size=14, class_name="ml-1"),
        on_click=on_click,
        class_name="flex items-center px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1",
        aria_expanded=is_active,
    )


def data_table() -> rx.Component:
    """The main data table component including search and results count."""
    return rx.el.div(
        rx.hstack(
            # filter_status_button(
            #     "Prime",
            #     is_active=TableState.sort_prime,
            #     on_click=TableState.set_prime_status
            # ),
            filter_status_button(
                "Secteur",
                is_active=TableState.sort_sector,
                on_click=AuthState.sort_by_secteur_count
            ),
            filter_status_button(
                "Typologie",
                is_active=TableState.sort_typology,
                on_click=AuthState.sort_by_typology_count
            ),
            rx.el.input(
                placeholder="Recherchez par nom de simulation...",
                value=AuthState.research_input,
                on_change=AuthState.set_research_input_simulation_name,
                class_name="w-4/5 pl-10 pr-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-sm text-gray-800 placeholder-gray-500",
            ),
            margin_bottom="1em",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.foreach(
                                TableState.column_data,
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
                            TableState.result_count == 0,
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
                #TableState.result_count.to_string() + " results",
                class_name="text-sm text-gray-500 mt-4",
            ),

            class_name="flex justify-end",
        ),
        on_mount=AuthState.fetch_simulations_result,
        class_name="bg-white p-6 rounded-lg shadow-md",
    )
