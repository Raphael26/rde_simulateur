import reflex as rx
from prime_simulateur.admin import admin_history_metrics, admin_history_table, admin_user_table
from prime_simulateur import prime_simulateur as ps
import prime_simulateur.components.text_styles as ts
from prime_simulateur.admin.admin_history_table import AdminState
from prime_simulateur.components.history_table import *
import plotly.express as px
import numpy as np
from sqlmodel import select

SECTEUR_COLORS = {
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

sunbuster_secteurs_typologies = None

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

def typologie_badge(typology):
    return rx.el.span(
        typology,
        class_name=rx.match(
            typology,
            ("Industrie", "px-2 py-1 text-xs text-center font-medium rounded-full bg-red-100 text-red-800"),
            ("Résidentiel", "px-2 py-1 text-xs text-center font-medium rounded-full bg-pink-100 text-pink-800"),
            ("Tertiaire", "px-2 py-1 text-xs text-center font-medium rounded-full bg-slate-100 text-slate-800"),
            ("Réseaux", "px-2 py-1 text-xs text-center font-medium rounded-full bg-purple-100 text-purple-800"),
            ("Agriculture", "px-2 py-1 text-xs text-center font-medium rounded-full bg-green-100 text-green-800"),
            ("Transport", "px-2 py-1 text-xs text-center font-medium rounded-full bg-teal-100 text-teal-800"),
            ("Utilité", "px-2 py-1 text-xs text-center font-medium rounded-full bg-gray-100 text-gray-800"),
            ("Bâtiment", "px-2 py-1 text-xs text-center font-medium rounded-full bg-yellow-100 text-yellow-800"),
            ("Enveloppe", "px-2 py-1 text-xs text-center font-medium rounded-full bg-stone-100 text-stone-800"),
            ("Thermique", "px-2 py-1 text-xs text-center font-medium rounded-full bg-purple-100 text-purple-800"),
            ("Équipement", "px-2 py-1 text-xs text-center font-medium rounded-full bg-rose-100 text-rose-800"),
            ("Service", "px-2 py-1 text-xs text-center font-medium rounded-full bg-blue-100 text-blue-800"),
            ("Eclairage", "px-2 py-1 text-xs text-center font-medium rounded-full bg-yellow-100 text-yellow-800"),
            ("Chaleur", "px-2 py-1 text-xs text-center font-medium rounded-full bg-orange-100 text-orange-800"),
            "px-2 py-1 text-xs text-center font-medium rounded-full bg-gray-100 text-gray-800"
        )
    )

def secteur_badge(sector):
    return rx.el.span(
        sector,
        class_name=rx.match(
            sector,
            ("Industrie",    "px-2 py-1 text-xs text-center font-medium rounded-full bg-red-100 text-red-800"),
            ("Résidentiel",  "px-2 py-1 text-xs text-center font-medium rounded-full bg-pink-100 text-pink-800"),
            ("Tertiaire",    "px-2 py-1 text-xs text-center font-medium rounded-full bg-slate-100 text-slate-800"),
            ("Réseaux",       "px-2 py-1 text-xs text-center font-medium rounded-full bg-purple-100 text-purple-800"),
            ("Agriculture",  "px-2 py-1 text-xs text-center font-medium rounded-full bg-green-100 text-green-800"),
            ("Transport",    "px-2 py-1 text-xs text-center font-medium rounded-full bg-teal-100 text-teal-800"),
            "px-2 py-1 text-xs text-center font-medium rounded-full bg-gray-100 text-gray-800"
        )
    )

def navigation_item(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        font_family="Open Sans",
        class_name=rx.cond(
            ps.State.current_path == href,
            "px-5 py-3 text-sm font-medium text-white bg-emerald-700 rounded-md shadow-sm",
            "px-5 py-3 text-sm font-medium text-black-100 hover:bg-emerald-600 hover:text-white rounded-md transition-colors duration-150 ease-in-out",
        ),
    )

def header_bar() -> rx.Component:
    """The header bar component."""
    return rx.el.div(
        rx.el.div(
        rx.hstack(
            navigation_item("Simulations", "/dashboard/"),
            rx.cond(
                AuthState.connected_user == "test1",
                rx.hstack(
                    navigation_item("Admin", "/admin/"),
                    navigation_item("Mpr", "/mpr/"),
                    )
                )
            ),
        ),
        rx.el.div(),
        class_name="flex items-center justify-between px-6 bg-white border-b border-gray-200",
        padding_y="2%",
        spacing="1"
    )

def sidebar() -> rx.Component:
    """A simple static sidebar component."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src="/RDE_consulting_icon.jpg",
                    width="80%",
                    on_click=rx.redirect("/"),
                    cursor="pointer"
                )
            ),
            class_name="flex items-center p-4 border-b border-white-200",
        ),
        rx.el.nav(
            rx.el.a(
                rx.icon(
                    tag="plus",
                    size=24,
                    class_name="mr-3",
                ),
                "Nouvelle simulation",
                href="/options",
                class_name="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded",
            ),
            rx.el.a(
                rx.icon(
                    tag="shield_ellipsis",
                    size=24,
                    class_name="mr-3",
                ),
                "Admin",
                href="/admin",
                class_name="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded",
            ),
        ),
        rx.spacer(),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    rx.link(
                        AuthState.connected_user,
                        class_name="text-xs font-sm flex-grow",
                        href="/profile",
                        cursor="pointer",
                    ),
                ),
                rx.spacer(),
                rx.el.button(
                    rx.icon(tag="power", size=16),
                    variant="ghost",
                    class_name="text-gray-600 hover:text-gray-900",
                    on_click=AuthState.disconnect
                ),
                class_name="flex items-center p-4",
            ),
            class_name="border-t border-gray-200",
        ),
        class_name="w-64 border-r border-white-200 flex flex-col h-screen",
        bg="white"
    )


def display_sunbuster():
    sunbuster_secteurs_typologies = px.sunburst(
        AdminState.sunbuster_secteurs_typologies_data,
        path=['secteur', 'typologie'],
        values='count',
        color='typologie',
        color_discrete_map=TYPOLOGIE_COLORS,
    )
    return rx.flex(
        rx.box(
            rx.text("Secteurs et typologies", class_name="font-bold text-xl mb-4"),
            rx.plotly(data=sunbuster_secteurs_typologies),
            # rx.vstack(
            #     rx.text("Typologies :", class_name="mt-4 font-medium"),
            #     rx.hstack(
            #         *[typologie_badge(t) for t in typologies_uniques],
            #     ),
            #     rx.text("Secteurs :", class_name="mt-4 font-medium"),
            #     rx.hstack(
            #         *[secteur_badge(s) for s in secteurs_uniques],
            #     ),
            #     margin_top="1em"
            # ),
            class_name="bg-white p-6 rounded-lg shadow-md",
        ),
        #on_mount=AdminState.secteur_typologie_chart(),
        align="center",
        justify="center",
        direction="column",
        width="100%",
        margin_top="1em",
    )


@rx.page(route="/admin", title="RDE Simulateur")
def page_admin_results_history():
    # REMOVED: data = fetch_all_user_simulation()  <-- This was causing the build error!
    # Data is now loaded at RUNTIME via on_mount
    ps.MultiStepFormState.set_page_progress(8)
    return rx.cond(
        AuthState.connected_user == "",
        rx.center(""),
        rx.cond(
            (AuthState.connected_user == "test1"),
            rx.el.div(
                sidebar(),
                rx.el.main(
                    header_bar(),
                    rx.el.div(
                        rx.hstack(
                            rx.button(
                                "Simulations",
                                on_click=AdminState.set_admin_view(value="simulations"),
                            ),
                            rx.button(
                                "Utilisateurs",
                                on_click=AdminState.set_admin_view(value="users"),
                            ),
                            justify="center",
                            margin_top="1em",
                        ),
                        rx.cond(
                            (AdminState.admin_view == "simulations"),
                            view_all_simulations(),  # CHANGED: No longer passing data parameter
                            view_all_users()
                        )
                    ),
                    class_name = "ml-100 w-full h-[100vh] overflow-y-auto",
                    on_mount=[
                        AdminState.fetch_all_user,
                        AdminState.fetch_all_simulations_for_admin,  # NEW: Load chart data at runtime
                    ],
                ),
                class_name = "flex bg-gray-50 h-[100vh] w-full overflow-hidden",
                on_mount = AuthState.fetch_simulations_result_admin,
                # on_mount=admin_history_metrics.DashboardState.load_initial_data,
                ),
            rx.center("Vous n'avez pas les permissions pour voir cette page !")
        )
    )

def view_all_simulations():
    """View all simulations - no longer takes data parameter, uses state instead."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"{AuthState.average_euro:.2f} €",
                    class_name="text-2xl font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.el.p(
                        "Moyenne des aides en euros",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    class_name="flex items-center justify-between mb-1",
                ),
                class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-md",
            ),
            rx.el.div(
                rx.el.p(
                    f"{AuthState.average_cumacs:.2f}",
                    class_name="text-2xl font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.el.p(
                        "Moyenne cumacs",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    class_name="flex items-center justify-between mb-1",
                ),
                class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-md",
            ),
            rx.el.div(
                rx.el.p(
                    f"{AuthState.number_of_simulation}",
                    class_name="text-2xl font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.el.p(
                        "Nombre de simulations réalisés",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    class_name="flex items-center justify-between mb-1",
                ),
                class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-md",
            ),
            rx.el.div(
                rx.el.p(
                    f"{AdminState.number_of_users}",
                    class_name="text-2xl font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.el.p(
                        "Nombre total d'utilisateurs",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    class_name="flex items-center justify-between mb-1",
                ),
                class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-md",
            ),
            # rx.el.div(
            #     rx.el.p(
            #         f"{AuthState.most_typology}",
            #         class_name="text-2xl font-semibold text-gray-900 mb-2",
            #     ),
            #     rx.el.div(
            #         rx.el.p(
            #             "Typologie le plus prisé",
            #             class_name="text-sm font-medium text-gray-500",
            #         ),
            #         class_name="flex items-center justify-between mb-1",
            #     ),
            #     class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-md",
            # ),
            # rx.el.div(
            #     rx.el.p(
            #         f"{AuthState.most_department}",
            #         class_name=rx.cond(
            #             AuthState.most_department.length() > 15,
            #             "text-1xl font-semibold text-gray-900 mb-2",
            #             "text-3xl font-semibold text-gray-900 mb-2"
            #         )
            #     ),
            #     rx.el.div(
            #         rx.el.p(
            #             "Département le plus selectionné",
            #             class_name="text-sm font-medium text-gray-500",
            #         ),
            #         class_name="flex items-center justify-between mb-1",
            #     ),
            #     class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-md",
            # ),
            class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5 sm:rounded-lg overflow-x-auto",
            margin_bottom="1em",
        ),
        admin_history_table.data_table(),
        secteur_typologie_chart(),  # CHANGED: No longer passing data parameter
        padding="2em",
    )

def view_all_users():
    return rx.el.div(
        admin_user_table.user_data_table(),
        #secteur_typologie_chart(data),
        padding="2em",
    )


def secteur_typologie_chart():
    """
    Chart component that displays data statistics.
    Plotly sunburst charts require special handling with Reflex state,
    so we use a simpler visualization that works reliably.
    """
    return rx.flex(
        rx.cond(
            AdminState.data_loaded,
            rx.box(
                rx.el.div(
                    rx.el.h3("Répartition des données", class_name="font-bold text-xl mb-4"),
                    rx.el.div(
                        # Secteurs summary
                        rx.el.div(
                            rx.el.h4("Par Secteur", class_name="font-semibold text-lg mb-2"),
                            rx.foreach(
                                AdminState.secteur_counts,
                                lambda item: rx.el.div(
                                    rx.el.span(item["name"], class_name="font-medium"),
                                    rx.el.span(f": {item['count']}", class_name="text-gray-600"),
                                    class_name="py-1",
                                )
                            ),
                            class_name="bg-gray-50 p-4 rounded-lg",
                        ),
                        # Typologies summary
                        rx.el.div(
                            rx.el.h4("Par Typologie", class_name="font-semibold text-lg mb-2"),
                            rx.foreach(
                                AdminState.typologie_counts,
                                lambda item: rx.el.div(
                                    rx.el.span(item["name"], class_name="font-medium"),
                                    rx.el.span(f": {item['count']}", class_name="text-gray-600"),
                                    class_name="py-1",
                                )
                            ),
                            class_name="bg-gray-50 p-4 rounded-lg",
                        ),
                        # Départements summary
                        rx.el.div(
                            rx.el.h4("Par Département", class_name="font-semibold text-lg mb-2"),
                            rx.foreach(
                                AdminState.departement_counts,
                                lambda item: rx.el.div(
                                    rx.el.span(item["name"], class_name="font-medium"),
                                    rx.el.span(f": {item['count']}", class_name="text-gray-600"),
                                    class_name="py-1",
                                )
                            ),
                            class_name="bg-gray-50 p-4 rounded-lg max-h-64 overflow-y-auto",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                    ),
                    class_name="w-full",
                ),
                width="100%",
                class_name="bg-white p-6 rounded-lg shadow-md",
                margin="auto",
            ),
            rx.center(
                rx.vstack(
                    rx.spinner(size="3"),
                    rx.text("Chargement des données...", class_name="text-gray-500"),
                    spacing="4",
                ),
                padding="4em",
                width="100%",
                class_name="bg-white p-6 rounded-lg shadow-md",
            ),
        ),
        align="center",
        justify="center",
        direction="column",
        width="90%",
        margin_top="1em",
    )