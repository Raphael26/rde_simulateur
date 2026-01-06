import reflex as rx
from back.auth_class import AuthState
from prime_simulateur.components.history_table import TableState
import ast

def tracker_item_component_detail(
    item: rx.Var[dict],
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                item["icon"].to(str),
                color="white",
                class_name="h-5 w-5",
            ),
            class_name="p-3 bg-teal-600 rounded-lg w-fit",
        ),
        rx.el.p(
            item["label"],
            font_family="Open Sans",
            class_name="text-sm font-medium text-gray-700 mt-2",
        ),
        rx.el.p(
            item["data"],
            font_family="Montserrat",
            class_name="text-md font-semibold text-gray-900",
        ),
        class_name="flex flex-col items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors flex-1 min-w-[100px] text-center",
    )

def sector_icon_component():
    return rx.match(
        TableState.selected_simulation["secteur"],
        ("Industrie", "factory"),
        ("Résidentiel", "house"),
        ("Tertiaire", "building-2"),
        ("Réseaux", "network"),
        ("Agriculture", "carrot"),
        ("Transport", "bus"),
        "help-circle",
    )

def get_typology_icon_str():
    return rx.match(
        TableState.selected_simulation["typologie"],
        ("Utilité", "plug"),
        ("Bâtiment", "building"),
        ("Enveloppe", "building"),
        ("Thermique", "flame"),
        ("Équipement", "cpu"),
        ("Service", "briefcase"),
        ("Eclairage", "lightbulb"),
        ("Chaleur", "thermometer"),
        "help-circle",
    )

def trackers_section_component_detail() -> rx.Component:
    data_items = [
        {
            "icon": "map-pin",
            "label": "Département",
            "data": TableState.selected_simulation["departement"],
        },
        {
            "icon": "calendar",
            "label": "Date prévue de signature",
            "data": TableState.selected_simulation["chosen_date"],
        },
        {
            "icon": sector_icon_component(),
            "label": "Secteur",
            "data": TableState.selected_simulation["secteur"],
        },
        {
            "icon": get_typology_icon_str(),
            "label": "Typologie",
            "data": TableState.selected_simulation["typologie"],
        },
        {
            "icon": "file",
            "label": "Fiche",
            "data": TableState.selected_simulation["fiche"],
        },
    ]
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Données entrées",
                font_family="Montserrat",
                class_name="text-lg font-semibold text-gray-800",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            rx.foreach(
                data_items,
                tracker_item_component_detail,
            ),
            class_name="flex flex-wrap gap-5",
        ),
        width="100%",
        class_name="p-6 bg-white rounded-xl shadow-sm border border-gray-100 mt-6",
    )

def parameter_entry(key: str, value: str) -> rx.Component:
    return rx.text(f"{key.capitalize().replace("_"," ")}: {value}",  font_family="Open Sans",)

def input_detail() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Entrée(s) du calculateur",
                font_family="Montserrat",
                class_name="text-lg font-semibold text-gray-800",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            rx.vstack(
                rx.text(f"Bénéficiaire: {TableState.selected_simulation["beneficiary"]}",  font_family="Open Sans",),
                rx.foreach(
                    TableState.selected_simulation_inputs_dict,
                    lambda entry: parameter_entry(entry[0], entry[1]),
                ),
            ),
    class_name="flex flex-wrap gap-5",
        ),
        width="100%",
        class_name="p-6 bg-white rounded-xl shadow-sm border border-gray-100 mt-6",
    )

def result_cumac_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "leaf",
                class_name="h-6 w-6 text-white opacity-75",
            ),
            color="white",
            class_name="p-3 bg-white/20 rounded-lg w-fit mb-4",
        ),
        rx.el.p(
            f"Résultat en cumacs",
            class_name="text-sm text-black/90 font-medium mb-1",
            font_family="Open Sans"
        ),
        rx.el.p(
            f"{TableState.selected_simulation["result_cumacs"]:.2f} cumacs",
            class_name="text-3xl font-bold",
            font_family="Montserrat"
        ),
        border="1px solid",
        border_color="gray-100",
        class_name=f"p-6 rounded-xl shadow-sm border border-gray-100 text-white flex flex-col justify-between h-full bg-gradient-to-br from-teal-600 to-teal-300",
    )

def result_euro_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "euro",
                class_name="h-6 w-6 text-white opacity-75",
            ),
            color="white",
            class_name="p-3 bg-white/20 rounded-lg w-fit mb-4",
        ),
        rx.el.p(
            "Résultat en euro",
            class_name="text-sm text-black/90 font-medium mb-1",
            font_family="Open Sans"
        ),
        rx.el.p(
            f"{(TableState.selected_simulation["result_eur"]):.2f} €",
            class_name="text-3xl font-bold text-white",
            font_family="Montserrat"
        ),
        border="1px solid",
        border_color="gray-100",
        class_name=f"p-6 rounded-xl shadow-sm border border-gray-100 text-white flex flex-col justify-between h-full bg-gradient-to-br from-teal-600 to-teal-300",
    )

def header_component() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Résultat de simulation n°",
                    rx.el.span(
                        #AuthState.connected_user,
                        TableState.selected_simulation["order"],
                        class_name="font-semibold",
                    ),
                    class_name="text-2xl text-gray-800",
                ),
                class_name="flex-grow",
            ),
            rx.spacer(),
            class_name="flex items-center justify-between w-full",
        ),
        position="fixed",
        z_index=50,
        class_name="py-6 px-8 bg-white border-b border-gray-200 w-full",
        width="100vw",
        height="15%",
        top=0,
        left=0,
    )

def sidebar() -> rx.Component:
    return rx.el.div(
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
                    tag="circle-user",
                    size=24,
                    class_name="mr-3",
                ),
                "Espace client",
                href="/dashboard",
                class_name="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded",
            ),
        ),
        rx.spacer(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "ES",
                    class_name="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-sm font-medium text-gray-700 mr-3",
                ),
                rx.el.p(
                    AuthState.connected_user,
                    class_name="text-sm font-medium text-gray-800 flex-grow",
                ),
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
        position="fixed",
        top="15%",
        width="15%",
        class_name="w-64 border-r border-white-200 flex flex-col h-screen",
        bg="white"
    )


@rx.page(route="/details", title="RDE Simulateur")
def details_page():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                header_component(),
                sidebar(),
                rx.el.main(
                    rx.el.div(
                        rx.vstack(
                            height="15%"
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Modifier le nom de la simulation"),
                                rx.hstack(
                                    rx.input(
                                        default_value=rx.cond(
                                            TableState.selected_simulation["name"],
                                            TableState.selected_simulation["name"],
                                            ""
                                        ),
                                        on_change=TableState.set_selected_simulation_name,
                                        name="phone_number",
                                        placeholder="",
                                        label="Nom de la simulation",
                                    ),
                                    rx.button(
                                        "Modifier",
                                        type="button",
                                        size="2",
                                        on_click=TableState.save_simulation_name,
                                        cursor="pointer",
                                        style=
                                        {"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)"},
                                        margin_bottom="1em",
                                    ),
                                ),
                                margin="1em"
                            ),
                        ),
                        rx.hstack(
                            result_euro_card(),
                            result_cumac_card(),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                        ),
                        trackers_section_component_detail(),
                        input_detail(),
                        rx.hstack(
                            rx.button(
                                "Retour",
                                type="button",
                                size="4",
                                on_click=rx.redirect("/dashboard"),
                                cursor="pointer",
                                style=
                                {"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)"},
                                margin_y="1em",
                            ),
                            rx.button(
                                "Supprimer",
                                type="button",
                                size="4",
                                on_click=TableState.remove_simulation,
                                cursor="pointer",
                                style=
                                {"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)"},
                                margin_y="1em",
                                bg="red"
                            ),
                            bg="#fcfcfd",
                            justify="center",
                        ),
                        align="center",
                        width="70%",
                    ),
                    margin_left="16%",
                    class_name="flex justify-center p-8 space-y-6 flex-grow",
                ),
            )
        ),
        height="140vh",
        align_items="center",
        bg="#fcfcfd",
    )
