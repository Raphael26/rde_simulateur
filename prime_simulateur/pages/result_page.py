import reflex as rx
from prime_simulateur import prime_simulateur as ps
import variables
from back.auth_class import AuthState
from prime_simulateur.components import popups
from prime_simulateur.pages.typology import get_icon_by_typology

def tracker_item_component(
    item: rx.Var[dict],
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                item["icon"],
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
        ps.MultiStepFormState.sector,
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
        ps.MultiStepFormState.typology,
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

def trackers_section_component() -> rx.Component:
    data_items = [
        {
            "icon": "map-pin",
            "label": "Département",
            "data": ps.MultiStepFormState.department,
        },
        {
            "icon": "calendar",
            "label": "Date prévue de signature",
            "data": ps.MultiStepFormState.date_signature,
        },
        {
            "icon": sector_icon_component(),
            "label": "Secteur",
            "data": ps.MultiStepFormState.sector,
        },
        {
            "icon": get_typology_icon_str(),
            "label": "Typologie",
            "data": ps.MultiStepFormState.typology,
        },
        {
            "icon": "file",
            "label": "Fiche",
            "data": ps.MultiStepFormState.selected_pdf.replace(".pdf", "").strip(),
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
                tracker_item_component,
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
                rx.text(f"Bénéficiaire: {ps.MultiStepFormState.beneficiary}",  font_family="Open Sans",),
                rx.foreach(
                    ps.MultiStepFormState.simulator_function_params,
                    lambda entry: parameter_entry(entry[0], entry[1]),
                ),
            ),
    class_name="flex flex-wrap gap-5",
        ),
        width="100%",
        class_name="p-6 bg-white rounded-xl shadow-sm border border-gray-100 mt-6",
    )


def error_detail() -> rx.Component:
    return rx.el.div(
        rx.vstack(
            height="25%"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Détails de l'erreur",
                    class_name="text-lg font-semibold text-gray-800",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.vstack(
                    rx.text(ps.MultiStepFormState.error)
                ),
                class_name="flex flex-wrap gap-5",
            ),
            width="100%",
            class_name="p-6 bg-white rounded-xl shadow-sm border border-gray-100 mt-6",
        ),
        align="center",
        width="60%",
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
            f"{(ps.MultiStepFormState.simulator_result):.2f} cumacs",
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
            f"{(ps.MultiStepFormState.simulator_result * 0.0065):.2f} €",
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
                    "Résultat de simulation",
                    # rx.el.span(
                    #     #AuthState.connected_user,
                    #     AuthState.last_simulation_order,
                    #     class_name="font-semibold",
                    # ),
                    class_name="text-2xl text-gray-800",
                ),
                class_name="flex-grow",
            ),
            rx.spacer(),
            class_name="flex items-center justify-between w-full",
        ),
        on_mount=AuthState.get_next_simulation_number(),
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
            # rx.el.a(
            #     rx.icon(
            #         tag="circle-user",
            #         size=24,
            #         class_name="mr-3",
            #     ),
            #     "Espace client",
            #     href="/dashboard",
            #     class_name="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded",
            #     font_family="Open Sans"
            # ),
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
        class_name="w-64 border-r border-white-200 flex flex-col h-screen",
        bg="white"
    )


@rx.page(route="/result",title="RDE Simulateur")
def result_page():
    ps.MultiStepFormState.set_page_progress(7)
    # return rx.fragment(
    #     rx.el.div(
    #         on_mount=ps.MultiStepFormState.set_check_result,
    #     ),
    #     rx.cond(
    #         ps.MultiStepFormState.check_result,
    #         rx.el.div(on_mount=ps.MultiStepFormState.redirect_to_dashboard),
    return rx.cond(
        ps.MultiStepFormState.selected_pdf == "",
        rx.text(""),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    header_component(),
                    sidebar(),
                    rx.el.main(
                        rx.vstack(
                            height="15%"
                        ),
                        rx.cond(
                            ps.MultiStepFormState.error != "",
                            error_detail(),
                            rx.el.div(
                                rx.vstack(
                                    height="15%"
                                ),
                                rx.hstack(
                                    result_euro_card(),
                                    result_cumac_card(),
                                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                                ),
                                trackers_section_component(),
                                input_detail(),
                                rx.vstack(
                                    rx.vstack(
                                        rx.text("Nom de la simulation"),
                                        rx.input(
                                            default_value=rx.cond(
                                                ps.MultiStepFormState.simulation_name,
                                                ps.MultiStepFormState.simulation_name,
                                                ""
                                            ),
                                            on_change=ps.MultiStepFormState.set_simulation_name,
                                            name="phone_number",
                                            placeholder="",
                                            label="Nom de la simulation",
                                        ),
                                        align="center",
                                        margin="1em"
                                    ),
                                    popups.save_simulation(True),
                                    # rx.button(
                                    #     "Sauvegarder",
                                    #     type="button",
                                    #     size="4",
                                    #     on_click=ps.MultiStepFormState.save_simulation_result(
                                    #         user_id=AuthState.get_user_id),
                                    #     cursor="pointer",
                                    #     style=
                                    #     {"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)"},
                                    #     margin_bottom="1em",
                                    # ),
                                    align="center",
                                ),
                                align="center",
                                width="60%",
                                # height="100%",
                            ),
                        ),
                        margin_left="16%",
                        class_name="flex justify-center p-8 space-y-6 flex-grow",
                    ),
                )
            ),
            align_items="center",
            on_mount=ps.MultiStepFormState.execute_string_function(),
            height="140vh",
            # background_color="#fcfcfd",
            bg="#fcfcfd",
        )
    )

# @rx.page(route="/result")
# def result_page():
#     ps.MultiStepFormState.set_page_progress(7)
#     #ps.MultiStepFormState.save_simulation_result()
#     return rx.fragment(
#         rx.el.div(
#             on_mount=ps.MultiStepFormState.set_check_result,
#         ),
#         rx.cond(
#             (ps.MultiStepFormState.check_result == False),
#             rx.el.div(on_mount=ps.MultiStepFormState.redirect_to_dashboard),
#             rx.el.div(
#                 rx.el.div(
#                     rx.el.div(
#                         header_component(),
#                         sidebar(),
#                         rx.el.main(
#                             rx.el.div(
#                                 rx.vstack(
#                                     height="22%"
#                                 ),
#                                 rx.hstack(
#                                     result_euro_card(),
#                                     result_cumac_card(),
#                                     class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
#                                 ),
#                                 trackers_section_component(),
#                                 align="center",
#                                 width="60%",
#                             ),
#                             class_name="flex justify-center p-8 space-y-6 flex-grow",
#                         ),
#                     )
#                 ),
#                 on_mount=ps.MultiStepFormState.execute_string_function(),
#                 bg="#fcfcfd",
#             )
#         )
#     )
