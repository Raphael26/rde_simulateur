import reflex as rx
from prime_simulateur.admin import admin_history_metrics, admin_history_table, mpr_table
from prime_simulateur import prime_simulateur as ps
from back.auth_class import AuthState
from prime_simulateur.admin.mpr_table import MprState, pdf_settings_modal


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

def display_linked_article(article):
    return rx.table.row(
        rx.table.cell(
            #pdf_settings_modal(article["pdf_file"])
            rx.text(article["pdf_file"])
        ),
        rx.table.cell(
            rx.link(
                article["link_article"].to(str).replace("https://www.legifrance.gouv.fr/loda/article_lc/", "").strip(),
                href=article["link_article"],
                cursor="pointer",
                font_family="Open Sans"
            )
        ),
        rx.table.cell(
            rx.button(
                rx.icon("trash", size=12),
                on_click=lambda: MprState.remove_linked_article(article["pdf_file"], article["link_article"]),
                size="1",
                bg="red"
            )
        ),
    )

def loading():
    return rx.center(
        rx.button("Chargement...", loading=True, disabled=True, variant="solid")
    )

@rx.page(route="/mpr", title="RDE Simulateur")
def page_admin_mpr_link():
    return rx.cond(
        AuthState.connected_user == "",
        rx.center(""),
        # rx.center(
        #     rx.button("Chargement...", loading=True, disabled=True, variant="solid")
        # ),
        rx.cond(
            (AuthState.connected_user == "test1"),
            rx.el.div(
                sidebar(),
                rx.el.main(
                    header_bar(),
                    rx.el.div(
                        rx.hstack(
                            rx.vstack(
                                rx.heading(f"Liste de toutes les opérations", size="5", font_family="Montserrat",
                                           color="#0d242c"),
                                mpr_table.list_every_pdf(),
                                align="center"
                            ),
                            rx.vstack(
                                rx.vstack(
                                    rx.vstack(
                                        rx.heading(f"Article selectionné :", size="5", font_family="Montserrat",
                                                   color="#0d242c"),

                                        rx.cond(
                                            MprState.selected_pdf,
                                            rx.text(
                                                f"{MprState.selected_pdf}",
                                                font_family="Open Sans",
                                            ),
                                            rx.text(
                                                "Cliquez sur un article pour le selectionner",
                                                font_family="Open Sans",
                                            ),
                                        ),
                                        rx.text(
                                            "Lien vers l'article à lier"
                                        ),
                                        rx.input(
                                            placeholder="Lien",
                                            on_change=MprState.set_link()
                                        ),
                                        rx.button(
                                            "Sauvegarder",
                                            on_click=MprState.add_article
                                        ),
                                    ),
                                    # margin="1em",
                                    # width="100%",
                                    # heigth="50%",
                                ),
                                rx.vstack(
                                    rx.heading(f"Articles liés :", size="5", font_family="Montserrat",
                                               color="#0d242c"),
                                    rx.table.root(
                                        rx.table.header(
                                            rx.table.row(
                                                rx.table.column_header_cell("Nom"),
                                                rx.table.column_header_cell("Lien"),
                                                rx.table.column_header_cell("Action"),
                                            ),
                                        ),
                                        rx.table.body(
                                            rx.foreach(
                                                MprState.all_linked_articles,
                                                display_linked_article,
                                            ),
                                        ),
                                        width="100%",
                                    ),
                                ),
                                width="60%",
                                heigth="100%",
                            ),
                            spacing="0",
                        ),
                        padding="2em",
                    ),
                    class_name="ml-100 w-full h-[100vh] overflow-y-auto",
                    align="center",
                ),
                class_name="flex bg-gray-50 h-[100vh] w-full overflow-hidden",
                on_mount=MprState.fetch_linked_articles,
            ),
            rx.center("Vous n'avez pas les permissions pour voir cette page !")
        )
    )