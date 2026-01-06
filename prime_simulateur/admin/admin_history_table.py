#from typing import Tuple, Optional, Literal, List, Any, Dict, Union
#
#from sqlalchemy import and_, select
#
#from back.auth_class import AuthState
#from models.models import CustomerData
#import ast
#from datetime import datetime
#
#import reflex as rx
#import plotly.express as px
#
#from reflex.event import EventSpec
#
#from models.simulation import SimulationResult
#from models.user import User
#from prime_simulateur import prime_simulateur as ps
#from prime_simulateur.components import history_table
#
#SECTEUR_COLORS = {
#    "Industrie": "#fee2e2",
#    "Résidentiel": "#fbcfe8",
#    "Tertiaire": "#f1f5f9",
#    "Réseaux": "#f3e8ff",
#    "Agriculture": "#dcfce7",
#    "Transport": "#ccfbf1",
#    "Indéfini": "#f3f4f6"
#}
#
#TYPOLOGIE_COLORS = {
#"Industrie": "#fee2e2",
#    "Résidentiel": "#fbcfe8",
#    "Tertiaire": "#f1f5f9",
#    "Réseaux": "#f3e8ff",
#    "Agriculture": "#dcfce7",
#    "Transport": "#ccfbf1",
#    "Utilité": "#f3f4f6",      # gray-100
#    "Bâtiment": "#fef9c3",     # yellow-100
#    "Enveloppe": "#f5f5f4",    # stone-100
#    "Thermique": "#f3e8ff",    # purple-100
#    "Équipement": "#ffe4e6",   # rose-100
#    "Service": "#dbeafe",     # blue-100
#    "Eclairage": "#fef9c3",    # yellow-100
#    "Chaleur": "#ffedd5",      # orange-100
#    "Indéfini": "#f3f4f6"      # gray-100
#}
#
#
#SortColumn = Literal[
#    "id",
#    "date_simulation",
#    "description",
#    "secteur",
#    "typologie",
#]
#SortOrder = Literal["asc", "desc"]
#
#
#
#class AdminState(rx.State):
#    query: str = ""
#    research_input: str = ""
#    user_list: list[dict] = []
#    number_of_users: int = 0
#    selected_simulation_id: Optional[int] = None
#    selected_simulation: dict = {}
#    selected_simulation_inputs_dict: dict = {}
#    selected_simulation_name: str = ""
#    result_count: int = 1
#    sort_order: SortOrder = "asc"
#    sort_column: str = "id"
#    sort_asc: bool = True
#    search_term: str = ""
#    sort_prime: bool = False
#    sort_sector: bool = False
#    sort_typology: bool = False
#    user_simulations: list[dict] = []
#    filtered_simulations: list[dict] = []
#    admin_view: str = "simulations"
#    sunbuster_secteurs_typologies_data: List[Dict[str, Union[str, int]]] = []
#
#    COLUMN_MAPPING: List[Tuple[str, str]] = [
#        ("ID", "id"),
#        ("ID utilisateur", "user_id"),
#        ("Nom simulation", "name"),
#        ("Fiche", "nom"),
#        ("Date simulation", "date_simulation"),
#        ("Département", "departement"),
#        ("Nom de la fiche", "description"),
#        ("Bénéficiaire", "beneficiary"),
#        ("Montant en euro", "result_eur"),
#        ("Montant en cumacs", "result_cumacs"),
#        ("Secteur", "secteur"),
#        ("Typologie", "typologie"),
#        ("Date signature", "chosen_date"),
#    ]
#    COLUMN_MAPPING_USER: List[Tuple[str, str]] = [
#        ("ID utilisateur", "id"),
#        ("Identifiant", "username"),
#        ("N° Téléphone", "phone_number"),
#        ("Prénom", "first_name"),
#        ("Nom", "last_name"),
#    ]
#
#
#    @rx.var
#    def column_data(
#            self
#    ) -> List[Tuple[str, Optional[SortColumn]]]:
#        """Returns the master list of column configurations (name and sort key)."""
#        return self.COLUMN_MAPPING
#
#    @rx.var
#    def column_data_user(self) -> List[Tuple[str, Optional[SortColumn]]]:
#        """Returns the master list of column configurations (name and sort key)."""
#        return self.COLUMN_MAPPING_USER
#
#    @rx.event
#    def select_simulation(self, simulation):
#        """Handles clicking on a customer row. Selects the customer or deselects if already selected."""
#        print(self.selected_simulation_id)
#        self.selected_simulation_id = simulation["id"]
#        self.selected_simulation = simulation
#        self.selected_simulation_inputs_dict = ast.literal_eval(simulation["parameters"])
#        print(self.selected_simulation)
#        print(self.selected_simulation_inputs_dict)
#        return rx.redirect("/details")
#
#    @rx.event
#    def sort_by(self, column_key: SortColumn):
#        """Handles clicking on a sortable table header. Updates the sort column and order."""
#        if self.sort_column == column_key:
#            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
#        else:
#            self.sort_column = column_key
#            self.sort_order = "asc"
#
#    # def fetch_all_user_simulation(self):
#    #     with rx.session() as session:
#    #         all_simulations = session.exec(
#    #             select(SimulationResult)
#    #         ).all()
#    #         if all_simulations:
#    #             sorted_simulations = sorted(all_simulations)
#    #             user_simulations = [
#    #                 {**sim.__dict__, "order": idx + 1}
#    #                 for idx, sim in enumerate(sorted_simulations)
#    #             ]
#    #             print(f"simulations are : {user_simulations}")
#    #             # number_of_simulation = len(all_simulations)
#    #             # sunbuster_data = user_simulations
#    #             return user_simulations
#
#    # @rx.event
#    # def secteur_typologie_chart(self):
#    #     dicts = []
#    #     data = self.fetch_all_user_simulation()
#    #     print(f"sunburst chart: {data}")
#    #     for item in data:
#    #         secteur = item.get('secteur', 'Indéfini')
#    #         typologie = item.get('typologie', 'Indéfini')
#    #         couleur_typo = TYPOLOGIE_COLORS.get(typologie, "#f3f4f6")
#    #         couleur_secteur = SECTEUR_COLORS.get(secteur, "#f3f4f6")
#    #         dicts.append({
#    #             'secteur': secteur,
#    #             'typologie': typologie,
#    #             'count': 1,
#    #             'color_typo': couleur_typo,
#    #             'color_secteur': couleur_secteur
#    #         })
#    #     self.sunbuster_secteurs_typologies_data = dicts
#    #     # self.sunbuster_secteurs_typologies = px.sunburst(
#    #     #     dicts,
#    #     #     path=['secteur', 'typologie'],
#    #     #     values='count',
#    #     #     color='typologie',
#    #     #     color_discrete_map=TYPOLOGIE_COLORS,
#    #     # )
#
#    def set_admin_view(self, value):
#        self.admin_view = value
#        print(self.admin_view)
#
#    def set_sort(self, column: str):
#        if self.sort_by == column:
#            self.sort_asc = not self.sort_asc
#        else:
#            self.sort_by = column
#            self.sort_asc = True
#
#    def set_prime_status(self):
#        self.sort_prime = not self.sort_prime
#
#    def set_sector_status(self):
#        self.sort_sector = not self.sort_sector
#
#    def set_typology_status(self):
#        self.sort_typology = not self.sort_typology
#
#    @rx.event
#    def set_research_input_simulation_name(self, keyword):
#        self.research_input = keyword
#        print(keyword)
#        self.filtered_simulations = [
#            sim for sim in self.user_simulations
#            if sim.get("name") and keyword.lower() in sim["name"].lower()
#        ]
#        yield
#
#    @rx.event
#    def remove_simulation(self):
#        with rx.session() as session:
#            simulation = session.exec(
#                SimulationResult.select().where(
#                    and_(
#                        SimulationResult.user_id == self.selected_simulation["user_id"],
#                        SimulationResult.id == self.selected_simulation_id,
#                    )
#                )
#            ).first()
#            if simulation:
#                session.delete(simulation)
#                session.commit()
#                return rx.redirect("/dashboard")
#
#    @rx.event
#    def fetch_all_user(self):
#        """Récupère tous les utilisateurs, les trie par id croissant et ajoute un ordre."""
#        with rx.session() as session:
#            all_users = session.exec(select(
#                User.id, User.username, User.password, User.oAuth, User.phone_number,
#                User.first_name, User.last_name, User.superuser
#            )).all()
#            self.user_list = [
#                {
#                    "id": row[0],
#                    "username": row[1],
#                    "phone_number": row[4],
#                    "first_name": row[5],
#                    "last_name": row[6],
#                    "order": idx + 1
#                }
#                for idx, row in enumerate(all_users)
#            ]
#            self.number_of_users = len(self.user_list)
#            print(f"user list is: {self.user_list}")
#
#
#def sort_icon(column_key: SortColumn) -> rx.Component:
#    """Displays sort direction icon or a neutral sortable indicator."""
#    icon_base_class = (
#        "ml-1 inline-block w-3 h-3 transition-colors duration-150 ease-in-out"
#    )
#    active_icon_class = f"{icon_base_class} text-gray-700"
#    inactive_icon_class = f"{icon_base_class} text-gray-400 group-hover:text-gray-600"
#    is_active_column = AdminState.sort_column == column_key
#    return rx.cond(
#        is_active_column,
#        rx.cond(
#            AdminState.sort_order == "asc",
#            rx.icon(
#                "arrow-up",
#                size=12,
#                class_name=active_icon_class,
#            ),
#            rx.icon(
#                "arrow-down",
#                size=12,
#                class_name=active_icon_class,
#            ),
#        ),
#        rx.icon(
#            "chevrons-up-down",
#            size=12,
#            class_name=inactive_icon_class,
#        ),
#    )
#
#def filter_status_button(
#    label: str,
#    is_active: rx.Var[bool],
#    on_click: EventSpec,
#) -> rx.Component:
#    return rx.el.button(
#        rx.el.span(
#            rx.icon(tag="plus", size=14, class_name="mr-1"),
#            label,
#            class_name="flex items-center",
#        ),
#        rx.icon(tag="chevron_down", size=14, class_name="ml-1"),
#        on_click=on_click,
#        class_name="flex items-center px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1",
#        aria_expanded=is_active,
#    )
#
#def sortable_table_header(col_name: str, column_key: SortColumn) -> rx.Component:
#    """Renders a sortable table header cell."""
#    base_class = "px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider group"
#    sortable_class = f"{base_class} cursor-pointer"
#    text_align_class = rx.match(
#        col_name,
#        ("Revenue", "text-right"),
#        ("Licenses", "text-center"),
#        ("Active licenses", "text-center"),
#        "text-left",
#    )
#    justify_content_val = rx.match(
#        col_name,
#        ("Revenue", "flex-end"),
#        ("Licenses", "center"),
#        ("Active licenses", "center"),
#        "flex-start",
#    )
#    combined_class = f"{sortable_class} {text_align_class}"
#    header_content_inner = rx.el.div(
#        col_name,
#        sort_icon(column_key),
#        class_name="flex items-center group-hover:text-gray-700 transition-colors duration-150 ease-in-out",
#        style={"justify_content": justify_content_val},
#    )
#    return rx.el.th(
#        rx.center(
#            header_content_inner,
#            scope="col",
#            class_name=combined_class,
#            on_click=lambda: AdminState.sort_by(column_key),
#        )
#    )
#
#
#def non_sortable_table_header(
#    col_name: str,
#) -> rx.Component:
#    """Renders a non-sortable table header cell."""
#    base_class = (
#        "px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
#    )
#    text_align_class = rx.match(
#        col_name,
#        ("Revenue", "text-right"),
#        ("Licenses", "text-center"),
#        ("Active licenses", "text-center"),
#        "text-left",
#    )
#    justify_content_val = rx.match(
#        col_name,
#        ("Revenue", "flex-end"),
#        ("Licenses", "center"),
#        ("Active licenses", "center"),
#        "flex-start",
#    )
#    combined_class = f"{base_class} {text_align_class}"
#    header_content_inner = rx.el.div(
#        col_name,
#        class_name="flex items-center",
#        style={"justify_content": justify_content_val},
#    )
#    return rx.el.th(
#        rx.center(
#            header_content_inner,
#            scope="col",
#            class_name=combined_class,
#        )
#    )
#
#def table_header(
#    col_data: rx.Var[Tuple[str, Optional[SortColumn]]],
#) -> rx.Component:
#    """Renders a table header cell, deciding if it's sortable or not."""
#    col_name = col_data[0]
#    column_key = col_data[1].to_string()
#    return rx.cond(
#        column_key,
#        sortable_table_header(col_name, column_key.to(SortColumn)),
#        non_sortable_table_header(col_name),
#    )
#
#def table_row(customer) -> rx.Component:
#    """Renders a single row in the data table."""
#    return rx.el.tr(
#        rx.foreach(
#            AdminState.column_data,
#            lambda col_data: get_cell_content(col_data[0], customer),
#        ),
#        #on_click=lambda: AdminState.select_simulation(customer),
#        #class_name="w-full bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
#        class_name=rx.cond(
#            AdminState.selected_simulation_id == customer["id"],
#            "w-full bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
#            "w-full border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors duration-150 ease-in-out",
#        ),
#    )
#
#def get_cell_content(col_name: rx.Var[str], customer) -> rx.Component:
#    """Gets the appropriate component for a specific cell based on column name."""
#    base_class = "px-4 py-3 whitespace-nowrap text-sm"
#    user_id = history_table.get_sector_tag(customer["user_id"])
#    tag_sector = history_table.get_sector_tag(customer["secteur"])
#    tag_typology = history_table.get_typology_tag(customer["typologie"])
#    return rx.match(
#        col_name,
#        (
#            "ID",
#            rx.el.td(
#                customer["order"],
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "ID utilisateur",
#            rx.el.td(
#                user_id,
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "Nom simulation",
#            rx.el.td(
#                customer["name"],
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "Fiche",
#            rx.el.td(
#                customer["fiche"],
#                class_name=f"{base_class} font-medium text-gray-900 text-left",
#            ),
#        ),
#        (
#            "Date signature",
#            rx.el.td(
#                customer["chosen_date"],
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "Département",
#            rx.el.td(
#                customer["departement"],
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "Nom de la fiche",
#            rx.el.td(
#                customer["description"],
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "Montant en euro",
#            rx.el.td(
#                f"{customer["result_eur"]:.2f} €",
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "Montant en cumacs",
#            rx.el.td(
#                f"{customer["result_cumacs"]:.2f}",
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "Secteur",
#            rx.el.td(
#                tag_sector,
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#        (
#            "Typologie",
#            rx.el.td(
#                tag_typology,
#                class_name=f"{base_class} text-gray-700 text-left",
#            ),
#        ),
#    )
#
#def sortable_th(label: str, column: str, size_percent: int) -> rx.Component:
#    arrow = rx.cond(
#        AdminState.sort_by == column,
#        rx.el.span(""),
#    )
#    return rx.el.th(
#        rx.el.div(
#            rx.el.span(label),
#            arrow,
#            class_name="flex items-center gap-1 cursor-pointer justify-center",
#            on_click=AdminState.set_sort(column),
#        ),
#        class_name="py-2 text-lg font-medium text-gray-500 uppercase text-center",
#        width=f"{size_percent}%",
#    )
#
#def filter_status_button(
#    label: str,
#    is_active: rx.Var[bool],
#    on_click: EventSpec,
#) -> rx.Component:
#    return rx.el.button(
#        rx.el.span(
#            rx.icon(tag="plus", size=14, class_name="mr-1"),
#            label,
#            class_name="flex items-center",
#        ),
#        rx.icon(tag="chevron_down", size=14, class_name="ml-1"),
#        on_click=on_click,
#        class_name="flex items-center px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1",
#        aria_expanded=is_active,
#    )
#
#
#def data_table() -> rx.Component:
#    """The main data table component including search and results count."""
#    return rx.el.div(
#        rx.hstack(
#            filter_status_button(
#                "Secteur",
#                is_active=AdminState.sort_sector,
#                on_click=AuthState.sort_by_secteur_count
#            ),
#            filter_status_button(
#                "Typologie",
#                is_active=AdminState.sort_typology,
#                on_click=AuthState.sort_by_typology_count
#            ),
#            rx.el.input(
#                placeholder="Recherchez par nom de simulation...",
#                value=AuthState.research_input,
#                on_change=AuthState.set_research_input_simulation_name,
#                class_name="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-sm text-gray-800 placeholder-gray-500",
#            ),
#            margin_bottom="1em",
#        ),
#        rx.el.div(
#            rx.el.div(
#                rx.el.table(
#                    rx.el.thead(
#                        rx.el.tr(
#                            rx.foreach(
#                                AdminState.column_data,
#                                table_header,
#                            ),
#                            class_name="bg-gray-50 border-b border-gray-200 whitespace-nowrap",
#                        )
#                    ),
#                    rx.el.tbody(
#                        rx.cond(
#                            AuthState.filter_by_sector == True,
#                            rx.foreach(
#                                AuthState.simulations_sorted_by_sector,
#                                table_row,
#                            ),
#                            rx.cond(
#                                AuthState.filter_by_typology == True,
#                                rx.foreach(
#                                    AuthState.simulations_sorted_by_typology,
#                                    table_row,
#                                ),
#                                rx.cond(
#                                    AuthState.research_input != "",
#                                    rx.foreach(
#                                        AuthState.filtered_simulations,
#                                        table_row,
#                                    ),
#                                    rx.foreach(
#                                        AuthState.user_simulations,
#                                        table_row,
#                                    ),
#                                ),
#                            ),
#                        ),
#                        rx.cond(
#                            AdminState.result_count == 0,
#                            rx.el.tr(
#                                rx.el.td(
#                                    "No customers found matching your criteria.",
#                                    class_name="px-4 py-3 text-center text-gray-500 italic",
#                                )
#                            ),
#                            rx.fragment(),
#                        ),
#                        class_name="divide-y divide-gray-200",
#                    ),
#                    class_name="min-w-full min-h-full",
#                ),
#                style={
#                    "maxHeight": "400px",  # Hauteur maximale
#                    "overflowY": "auto",  # Scroll vertical
#                }
#            ),
#            class_name="shadow overflow-hidden border border-gray-200 sm:rounded-lg overflow-x-auto overflow-y-auto",
#        ),
#        rx.el.div(
#            rx.el.p(
#                #AdminState.result_count.to_string() + " results",
#                class_name="text-sm text-gray-500 mt-4",
#            ),
#
#            class_name="flex justify-end",
#        ),
#        on_mount=AuthState.fetch_simulations_result_admin,
#        class_name="bg-white p-6 rounded-lg shadow-md",
#    )
#

from typing import Tuple, Optional, Literal, List, Any, Dict, Union

from sqlalchemy import and_, select

from back.auth_class import AuthState
from models.models import CustomerData
import ast
from datetime import datetime

import reflex as rx
import plotly.express as px
import plotly.graph_objects as go

from reflex.event import EventSpec

from models.simulation import SimulationResult
from models.user import User
from prime_simulateur import prime_simulateur as ps
from prime_simulateur.components import history_table

SECTEUR_COLORS = {
    "Industrie": "#fee2e2",
    "Résidentiel": "#fbcfe8",
    "Tertiaire": "#f1f5f9",
    "Réseaux": "#f3e8ff",
    "Agriculture": "#dcfce7",
    "Transport": "#ccfbf1",
    "Indéfini": "#f3f4f6"
}

TYPOLOGIE_COLORS = {
"Industrie": "#fee2e2",
    "Résidentiel": "#fbcfe8",
    "Tertiaire": "#f1f5f9",
    "Réseaux": "#f3e8ff",
    "Agriculture": "#dcfce7",
    "Transport": "#ccfbf1",
    "Utilité": "#f3f4f6",      # gray-100
    "Bâtiment": "#fef9c3",     # yellow-100
    "Enveloppe": "#f5f5f4",    # stone-100
    "Thermique": "#f3e8ff",    # purple-100
    "Équipement": "#ffe4e6",   # rose-100
    "Service": "#dbeafe",     # blue-100
    "Eclairage": "#fef9c3",    # yellow-100
    "Chaleur": "#ffedd5",      # orange-100
    "Indéfini": "#f3f4f6"      # gray-100
}


SortColumn = Literal[
    "id",
    "date_simulation",
    "description",
    "secteur",
    "typologie",
]
SortOrder = Literal["asc", "desc"]



class AdminState(rx.State):
    query: str = ""
    research_input: str = ""
    user_list: list[dict] = []
    number_of_users: int = 0
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
    filtered_simulations: list[dict] = []
    admin_view: str = "simulations"
    sunbuster_secteurs_typologies_data: List[Dict[str, Union[str, int]]] = []
    
    # NEW: State variables for chart data (loaded at runtime)
    all_simulations_data: list[dict] = []
    chart_secteur_typologie_data: List[Dict[str, Union[str, int]]] = []
    chart_departement_data: List[Dict[str, Union[str, int]]] = []
    # Store complete figure specs as dicts
    secteur_figure_spec: dict = {}
    departement_figure_spec: dict = {}
    data_loaded: bool = False

    COLUMN_MAPPING: List[Tuple[str, str]] = [
        ("ID", "id"),
        ("ID utilisateur", "user_id"),
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
    COLUMN_MAPPING_USER: List[Tuple[str, str]] = [
        ("ID utilisateur", "id"),
        ("Identifiant", "username"),
        ("N° Téléphone", "phone_number"),
        ("Prénom", "first_name"),
        ("Nom", "last_name"),
    ]


    @rx.var
    def column_data(
            self
    ) -> List[Tuple[str, Optional[SortColumn]]]:
        """Returns the master list of column configurations (name and sort key)."""
        return self.COLUMN_MAPPING

    @rx.var
    def has_chart_data(self) -> bool:
        """Check if chart data is available."""
        return len(self.chart_secteur_typologie_data) > 0

    @rx.var
    def secteur_counts(self) -> List[Dict[str, Union[str, int]]]:
        """Aggregate counts by secteur."""
        if not self.chart_secteur_typologie_data:
            return []
        counts = {}
        for item in self.chart_secteur_typologie_data:
            secteur = item.get('secteur', 'Indéfini')
            counts[secteur] = counts.get(secteur, 0) + 1
        return [{"name": k, "count": v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]

    @rx.var
    def typologie_counts(self) -> List[Dict[str, Union[str, int]]]:
        """Aggregate counts by typologie."""
        if not self.chart_secteur_typologie_data:
            return []
        counts = {}
        for item in self.chart_secteur_typologie_data:
            typologie = item.get('typologie', 'Indéfini')
            counts[typologie] = counts.get(typologie, 0) + 1
        return [{"name": k, "count": v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]

    @rx.var
    def departement_counts(self) -> List[Dict[str, Union[str, int]]]:
        """Aggregate counts by departement."""
        if not self.chart_departement_data:
            return []
        counts = {}
        for item in self.chart_departement_data:
            dept = item.get('departement', 'Indéfini')
            counts[dept] = counts.get(dept, 0) + 1
        return [{"name": k, "count": v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]

    @rx.var
    def column_data_user(self) -> List[Tuple[str, Optional[SortColumn]]]:
        """Returns the master list of column configurations (name and sort key)."""
        return self.COLUMN_MAPPING_USER

    @rx.event
    def select_simulation(self, simulation):
        """Handles clicking on a customer row. Selects the customer or deselects if already selected."""
        print(self.selected_simulation_id)
        self.selected_simulation_id = simulation["id"]
        self.selected_simulation = simulation
        self.selected_simulation_inputs_dict = ast.literal_eval(simulation["parameters"])
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

    @rx.event
    def fetch_all_simulations_for_admin(self):
        """
        Fetches all simulations from the database at RUNTIME (not build time).
        This is called via on_mount when the admin page loads.
        """
        with rx.session() as session:
            all_simulations = session.exec(
                select(SimulationResult)
            ).all()
            if all_simulations:
                sorted_simulations = sorted(all_simulations, key=lambda sim: sim.id)
                self.all_simulations_data = [
                    {**sim.__dict__, "order": idx + 1}
                    for idx, sim in enumerate(sorted_simulations)
                ]
                # Remove SQLAlchemy internal state if present
                for sim_dict in self.all_simulations_data:
                    sim_dict.pop('_sa_instance_state', None)
                
                # Build chart data
                self._build_chart_data()
                self.data_loaded = True
                print(f"Loaded {len(self.all_simulations_data)} simulations for admin")
            else:
                self.all_simulations_data = []
                self.chart_secteur_typologie_data = []
                self.chart_departement_data = []
                self.data_loaded = True

    def _build_chart_data(self):
        """Build the chart data and figure specs from loaded simulations."""
        dicts_department = []
        dicts = []
        
        for item in self.all_simulations_data:
            departements = item.get('departement', 'Indéfini')
            secteur = item.get('secteur', 'Indéfini')
            typologie = item.get('typologie', 'Indéfini')
            couleur_typo = TYPOLOGIE_COLORS.get(typologie, "#f3f4f6")
            couleur_secteur = SECTEUR_COLORS.get(secteur, "#f3f4f6")
            
            dicts_department.append({
                "departement": departements,
                'count': 1,
            })
            dicts.append({
                'secteur': secteur,
                'typologie': typologie,
                'count': 1,
                'color_typo': couleur_typo,
                'color_secteur': couleur_secteur
            })
        
        self.chart_departement_data = dicts_department
        self.chart_secteur_typologie_data = dicts
        
        # Build the plotly figure specs and store as dicts
        if dicts:
            fig_secteur = px.sunburst(
                dicts,
                title="Secteurs et typologies",
                path=['secteur', 'typologie'],
                values='count',
                color='secteur',
                color_discrete_map=TYPOLOGIE_COLORS,
            )
            self.secteur_figure_spec = fig_secteur.to_plotly_json()
        
        if dicts_department:
            fig_dept = px.sunburst(
                dicts_department,
                title="Départements",
                path=['departement'],
                values='count',
            )
            self.departement_figure_spec = fig_dept.to_plotly_json()

    def set_admin_view(self, value):
        self.admin_view = value
        print(self.admin_view)

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
    def set_research_input_simulation_name(self, keyword):
        self.research_input = keyword
        print(keyword)
        self.filtered_simulations = [
            sim for sim in self.user_simulations
            if sim.get("name") and keyword.lower() in sim["name"].lower()
        ]
        yield

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
    def fetch_all_user(self):
        """Récupère tous les utilisateurs, les trie par id croissant et ajoute un ordre."""
        with rx.session() as session:
            all_users = session.exec(select(
                User.id, User.username, User.password, User.oAuth, User.phone_number,
                User.first_name, User.last_name, User.superuser
            )).all()
            self.user_list = [
                {
                    "id": row[0],
                    "username": row[1],
                    "phone_number": row[4],
                    "first_name": row[5],
                    "last_name": row[6],
                    "order": idx + 1
                }
                for idx, row in enumerate(all_users)
            ]
            self.number_of_users = len(self.user_list)
            print(f"user list is: {self.user_list}")


def sort_icon(column_key: SortColumn) -> rx.Component:
    """Displays sort direction icon or a neutral sortable indicator."""
    icon_base_class = (
        "ml-1 inline-block w-3 h-3 transition-colors duration-150 ease-in-out"
    )
    active_icon_class = f"{icon_base_class} text-gray-700"
    inactive_icon_class = f"{icon_base_class} text-gray-400 group-hover:text-gray-600"
    is_active_column = AdminState.sort_column == column_key
    return rx.cond(
        is_active_column,
        rx.cond(
            AdminState.sort_order == "asc",
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
        class_name="flex items-center group-hover:text-gray-700 transition-colors duration-150 ease-in-out",
        style={"justify_content": justify_content_val},
    )
    return rx.el.th(
        rx.center(
            header_content_inner,
            scope="col",
            class_name=combined_class,
            on_click=lambda: AdminState.sort_by(column_key),
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
        class_name="flex items-center",
        style={"justify_content": justify_content_val},
    )
    return rx.el.th(
        rx.center(
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
    return rx.cond(
        column_key,
        sortable_table_header(col_name, column_key.to(SortColumn)),
        non_sortable_table_header(col_name),
    )

def table_row(customer) -> rx.Component:
    """Renders a single row in the data table."""
    return rx.el.tr(
        rx.foreach(
            AdminState.column_data,
            lambda col_data: get_cell_content(col_data[0], customer),
        ),
        #on_click=lambda: AdminState.select_simulation(customer),
        #class_name="w-full bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
        class_name=rx.cond(
            AdminState.selected_simulation_id == customer["id"],
            "w-full bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
            "w-full border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors duration-150 ease-in-out",
        ),
    )

def get_cell_content(col_name: rx.Var[str], customer) -> rx.Component:
    """Gets the appropriate component for a specific cell based on column name."""
    base_class = "px-4 py-3 whitespace-nowrap text-sm"
    user_id = history_table.get_sector_tag(customer["user_id"])
    tag_sector = history_table.get_sector_tag(customer["secteur"])
    tag_typology = history_table.get_typology_tag(customer["typologie"])
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
            "ID utilisateur",
            rx.el.td(
                user_id,
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Nom simulation",
            rx.el.td(
                customer["name"],
                class_name=f"{base_class} text-gray-700 text-left",
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
    )

def sortable_th(label: str, column: str, size_percent: int) -> rx.Component:
    arrow = rx.cond(
        AdminState.sort_by == column,
        rx.el.span(""),
    )
    return rx.el.th(
        rx.el.div(
            rx.el.span(label),
            arrow,
            class_name="flex items-center gap-1 cursor-pointer justify-center",
            on_click=AdminState.set_sort(column),
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
            filter_status_button(
                "Secteur",
                is_active=AdminState.sort_sector,
                on_click=AuthState.sort_by_secteur_count
            ),
            filter_status_button(
                "Typologie",
                is_active=AdminState.sort_typology,
                on_click=AuthState.sort_by_typology_count
            ),
            rx.el.input(
                placeholder="Recherchez par nom de simulation...",
                value=AuthState.research_input,
                on_change=AuthState.set_research_input_simulation_name,
                class_name="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-sm text-gray-800 placeholder-gray-500",
            ),
            margin_bottom="1em",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.foreach(
                                AdminState.column_data,
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
        on_mount=AuthState.fetch_simulations_result_admin,
        class_name="bg-white p-6 rounded-lg shadow-md",
    )