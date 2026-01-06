import reflex as rx
import reflex_chakra as rc
from prime_simulateur.components import history_metrics, history_table
from prime_simulateur import prime_simulateur as ps
from back.auth_class import AuthState

def navigation_item(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        font_family="Open Sans",
        class_name=rx.cond(
            ps.State.current_path == href,
            "px-5 py-3 text-sm font-medium text-white bg-emerald-700 rounded-md shadow-md",
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
            rx.cond(
                AuthState.connected_user == "test1",
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
            )
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

@rx.page(route="/dashboard", title="RDE Simulateur")
def page_results_history():
    ps.MultiStepFormState.set_page_progress(8)
    return (
        rx.cond(
            AuthState.connected_user == "",
            rx.center(""),
            rx.cond(
                AuthState.is_logged_in,
                rx.el.div(
                    sidebar(),
                    rx.el.main(
                        header_bar(),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        f"{AuthState.average_euro:.2f} €",
                                        class_name="text-3xl font-semibold text-gray-900 mb-2",
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
                                        class_name="text-3xl font-semibold text-gray-900 mb-2",
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
                                class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4",
                                margin_bottom="1em",
                            ),
                            history_table.data_table(),
                            padding="2em",
                        ),
                        class_name="ml-100 w-full h-[100vh] overflow-y-auto",
                    ),
                    class_name="flex bg-gray-50 h-[100vh] w-full overflow-hidden",
                ),
                rx.center("Vous n'êtes pas connecté !")
            ))
    )
