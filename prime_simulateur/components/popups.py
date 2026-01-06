#import reflex as rx
#import reflex_chakra as rc
#import variables
#from prime_simulateur import prime_simulateur as ps
#from back.auth_class import AuthState
#from prime_simulateur.components import text_styles as ts
#from back.auth.react_auth_google import GoogleOAuthProvider, GoogleLogin
#from dotenv import load_dotenv
#import os
#
#load_dotenv()
#
#def execute_simulation(to_dashboard: bool):
#    button_text = "Calculer ma prime CEE"
#    return rx.dialog.root(
#        rx.dialog.trigger(
#            rx.button(
#                rx.hstack(
#                    rx.text(
#                        button_text,
#                        weight="bold",
#                    )
#                ),
#                type="button",
#                size="4",
#                on_click=rx.cond(
#                    (ps.MultiStepFormState.get_missing_arguments != ""),
#                    rx.toast(ps.MultiStepFormState.get_missing_arguments, duration=5000),
#                    rx.redirect("/result")
#                ),
#                cursor="pointer",
#                weight="bold",
#                style={"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",},
#                on_mount=ps.MultiStepFormState.detect_empty_items()
#            ),
#            on_mount=AuthState.set_to_dashboard_or_not(to_dashboard)
#        ),
#    )
#
#def save_simulation(to_dashboard: bool):
#    button_text = "Sauvegarder"
#    return rx.dialog.root(
#        rx.dialog.trigger(
#            rx.button(
#                rx.hstack(rx.text(
#                    button_text,
#                    weight="bold",
#                )
#                ),
#                type="button",
#                size="4",
#                on_click=rx.cond(
#                    ((AuthState.is_logged_in) & to_dashboard),
#                    ps.MultiStepFormState.save_simulation_result(user_id=AuthState.get_user_id),
#                    AuthState.open_login_popup,
#                    # rx.cond(
#                    #     (ps.MultiStepFormState.get_missing_arguments != ""),
#                    #     rx.toast(ps.MultiStepFormState.get_missing_arguments, duration=5000),
#                    #     rx.cond(
#                    #         (AuthState.is_logged_in) & (ps.MultiStepFormState.execute_string_function()),
#                    #         rx.redirect("/result"),
#                    #         AuthState.open_login_popup,
#                    #     ),
#                    # ),
#                ),
#                cursor="pointer",
#                weight="bold",
#                style={"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",},
#                on_mount=ps.MultiStepFormState.detect_empty_items()
#            ),
#            on_mount=AuthState.set_to_dashboard_or_not(to_dashboard)
#        ),
#        rx.cond(
#            (AuthState.show_auth_popup == True),
#            rx.dialog.content(
#                rx.cond(
#                    AuthState.register_mode,
#                    rx.vstack(
#                        rx.dialog.title("Créer un compte"),
#                        rx.input(
#                            placeholder="Adresse mail",
#                            width="60%",
#                            on_change=AuthState.set_username,
#                            value=AuthState.username,
#                        ),
#                        rx.input(
#                            placeholder="Mot de passe",
#                            type="password",
#                            width="60%",
#                            on_change=AuthState.set_password,
#                            value=AuthState.password,
#                        ),
#                        rx.input(
#                            placeholder="Confirmer le mot de passe",
#                            type="password",
#                            width="60%",
#                            on_change=AuthState.set_confirm_password,
#                            value=AuthState.confirm_password,
#                        ),
#                        rx.button(
#                            "S'inscrire",
#                            width="60%",
#                            bg="#27566B",
#                            color="white",
#                            on_click=AuthState.register(to_dashboard),
#                        ),
#                        # GoogleOAuthProvider.create(
#                        #     GoogleLogin.create(on_success=AuthState.on_google_success),
#                        #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#                        # ),
#                        rx.cond(
#                            (AuthState.register_error != ""),
#                            rx.text(
#                                AuthState.register_error,
#                                color="red",
#                                font_size="0.9em",
#                                margin_top="8px",
#                            ),
#                        ),
#                        rx.link(
#                            rx.text("Déjà un compte ? Se connecter", font_size="0.8em", color="gray"),
#                            on_click=AuthState.open_login_popup,
#                        ),
#                        spacing="5",
#                        align_items="center",
#                    ),
#                    rx.vstack(
#                        rx.dialog.title("Veuillez saisir vos identifiants"),
#                        rx.input(
#                            placeholder="Adresse mail",
#                            width="60%",
#                            on_change=AuthState.set_username,
#                            value=AuthState.username,
#                        ),
#                        rx.input(
#                            placeholder="Mot de passe",
#                            type="password",
#                            width="60%",
#                            on_change=AuthState.set_password,
#                            value=AuthState.password,
#                        ),
#                        rx.button(
#                            "Se connecter",
#                            width="60%",
#                            bg="#27566B",
#                            color="white",
#                            on_click=AuthState.login(False),
#                        ),
#                        # GoogleOAuthProvider.create(
#                        #     GoogleLogin.create(on_success=AuthState.on_google_success),
#                        #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#                        #     #to_dashboard=to_dashboard
#                        # ),
#                        rx.cond(
#                            (AuthState.login_error != "Cette adresse mail est déjà utilisé."),
#                            rx.text(AuthState.login_error, color="red", font_size="0.8em"),
#                        ),
#                        rx.link(
#                            rx.text("Mot de passe oublié ?", font_size="0.8em", color="gray"),
#                            href="/"
#                        ),
#                        rx.link(
#                            rx.text("Créer un compte", font_size="0.8em", color="gray"),
#                            on_click=AuthState.open_register_popup,
#                        ),
#                        spacing="5",
#                        align_items="center",
#                    ),
#                ),
#                rx.dialog.close(
#                    rx.button(
#                    "Fermer",
#                    on_click=AuthState.close_auth_popup,
#                    )
#                ),
#                z_index="1000",
#                padding="2rem",
#                border_radius="lg",
#            ),
#        ),
#    )
#
#def login_popup(to_dashboard: bool, location: str):
#    if to_dashboard:
#        button_text = "Espace client"
#    else:
#        button_text = "Calculer ma prime CEE"
#    return rx.dialog.root(
#        rx.dialog.trigger(
#            rx.button(
#                rx.hstack(rx.text(
#                    button_text,
#                    weight="bold",
#                )
#                ),
#                type="button",
#                size="4",
#                on_click=rx.cond(
#                    ((AuthState.is_logged_in) & AuthState.to_dashboard),
#                    rx.redirect("/dashboard"),
#                    AuthState.open_login_popup,
#                    # rx.cond(
#                    #     (ps.MultiStepFormState.get_missing_arguments != ""),
#                    #     rx.toast(ps.MultiStepFormState.get_missing_arguments, duration=5000),
#                    #     rx.cond(
#                    #         (AuthState.is_logged_in) & (ps.MultiStepFormState.execute_string_function()),
#                    #         rx.redirect("/result"),
#                    #         AuthState.open_login_popup,
#                    #     ),
#                    # ),
#                ),
#                cursor="pointer",
#                weight="bold",
#                style={"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",},
#                on_mount=ps.MultiStepFormState.detect_empty_items()
#            ),
#            on_mount=AuthState.set_to_dashboard_or_not(to_dashboard)
#        ),
#        rx.cond(
#            (AuthState.show_auth_popup == True),
#            rx.dialog.content(
#                rx.cond(
#                    AuthState.register_mode,
#                    rx.vstack(
#                        rx.dialog.title("Créer un compte"),
#                        rx.input(
#                            placeholder="Adresse mail",
#                            width="60%",
#                            on_change=AuthState.set_username,
#                            value=AuthState.username,
#                        ),
#                        rx.input(
#                            placeholder="Mot de passe",
#                            type="password",
#                            width="60%",
#                            on_change=AuthState.set_password,
#                            value=AuthState.password,
#                        ),
#                        rx.input(
#                            placeholder="Confirmer le mot de passe",
#                            type="password",
#                            width="60%",
#                            on_change=AuthState.set_confirm_password,
#                            value=AuthState.confirm_password,
#                        ),
#                        rx.button(
#                            "S'inscrire",
#                            width="60%",
#                            bg="#27566B",
#                            color="white",
#                            on_click=AuthState.register(to_dashboard),
#                        ),
#                        # GoogleOAuthProvider.create(
#                        #     GoogleLogin.create(on_success=AuthState.on_google_success),
#                        #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#                        # ),
#                        rx.cond(
#                            (AuthState.register_error != ""),
#                            rx.text(
#                                AuthState.register_error,
#                                color="red",
#                                font_size="0.9em",
#                                margin_top="8px",
#                            ),
#                        ),
#                        rx.link(
#                            rx.text("Déjà un compte ? Se connecter", font_size="0.8em", color="gray"),
#                            on_click=AuthState.open_login_popup,
#                        ),
#                        spacing="5",
#                        align_items="center",
#                    ),
#                    rx.vstack(
#                        rx.dialog.title("Veuillez saisir vos identifiants"),
#                        rx.input(
#                            placeholder="Adresse mail",
#                            width="60%",
#                            on_change=AuthState.set_username,
#                            value=AuthState.username,
#                        ),
#                        rx.input(
#                            placeholder="Mot de passe",
#                            type="password",
#                            width="60%",
#                            on_change=AuthState.set_password,
#                            value=AuthState.password,
#                        ),
#                        rx.button(
#                            "Se connecter",
#                            width="60%",
#                            bg="#27566B",
#                            color="white",
#                            on_click=AuthState.login(to_dashboard=to_dashboard),
#                        ),
#                        # GoogleOAuthProvider.create(
#                        #     GoogleLogin.create(on_success=AuthState.on_google_success),
#                        #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
#                        #     #to_dashboard=to_dashboard
#                        # ),
#                        rx.cond(
#                            (AuthState.login_error != "Cette adresse mail est déjà utilisé."),
#                            rx.text(AuthState.login_error, color="red", font_size="0.8em"),
#                        ),
#                        rx.link(
#                            rx.text("Mot de passe oublié ?", font_size="0.8em", color="gray"),
#                            href="/"
#                        ),
#                        rx.link(
#                            rx.text("Créer un compte", font_size="0.8em", color="gray"),
#                            on_click=AuthState.open_register_popup,
#                        ),
#                        spacing="5",
#                        align_items="center",
#                    ),
#                ),
#                rx.dialog.close(
#                    rx.button(
#                    "Fermer",
#                    on_click=AuthState.close_auth_popup,
#                    )
#                ),
#                z_index="1000",
#                padding="2rem",
#                border_radius="lg",
#            ),
#        ),
#    )
#
#def contact_popup():
#    return rx.dialog.root(
#        rx.dialog.trigger(
#            rx.button(
#                rx.hstack(
#                    rx.icon("mail", size=24),
#                    rx.text("Prendre contact", size="3"),
#                    align="center",
#                ),
#                size="3",
#                padding="1em",
#                variant="solid",
#                style={
#                    "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
#                },
#                _hover={
#                    "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
#                    "transform": "scale(1.05)",
#                    "transition": "all 0.2s ease-in-out"
#                },
#                transition="all 0.2s ease-in-out",
#            )
#        ),
#        rx.dialog.content(
#            rx.dialog.title("Prendre contact avec un conseiller"),
#            rx.dialog.description(
#                "Cliquez sur le lien ci-dessous pour sélectionner un créneau.",
#            ),
#            rx.vstack(
#                ts.button_text("prendre rdv", "album"),
#                padding="2em", align_items="center"
#            ),
#            rx.dialog.close(
#                ts.button_text("Fermer", "x"),
#            ),
#        ),
#    )
#

import reflex as rx
import variables
from prime_simulateur import prime_simulateur as ps
from back.auth_class import AuthState
from prime_simulateur.components import text_styles as ts
from back.auth.react_auth_google import GoogleOAuthProvider, GoogleLogin
from dotenv import load_dotenv

load_dotenv()

def execute_simulation(to_dashboard: bool):
    button_text = "Calculer ma prime CEE"
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(
                    rx.text(
                        button_text,
                        weight="bold",
                    )
                ),
                type="button",
                size="4",
                on_click=rx.cond(
                    (ps.MultiStepFormState.get_missing_arguments != ""),
                    rx.toast(ps.MultiStepFormState.get_missing_arguments, duration=5000),
                    rx.redirect("/result")
                ),
                cursor="pointer",
                weight="bold",
                style={"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",},
                on_mount=ps.MultiStepFormState.detect_empty_items()
            ),
            on_mount=AuthState.set_to_dashboard_or_not(to_dashboard)
        ),
    )

def save_simulation(to_dashboard: bool):
    button_text = "Sauvegarder"
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(rx.text(
                    button_text,
                    weight="bold",
                )
                ),
                type="button",
                size="4",
                on_click=rx.cond(
                    ((AuthState.is_logged_in) & to_dashboard),
                    # FIXED: Changed from AuthState.get_user_id to AuthState.user_id
                    ps.MultiStepFormState.save_simulation_result(user_id=AuthState.user_id),
                    AuthState.open_login_popup,
                    # rx.cond(
                    #     (ps.MultiStepFormState.get_missing_arguments != ""),
                    #     rx.toast(ps.MultiStepFormState.get_missing_arguments, duration=5000),
                    #     rx.cond(
                    #         (AuthState.is_logged_in) & (ps.MultiStepFormState.execute_string_function()),
                    #         rx.redirect("/result"),
                    #         AuthState.open_login_popup,
                    #     ),
                    # ),
                ),
                cursor="pointer",
                weight="bold",
                style={"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",},
                on_mount=ps.MultiStepFormState.detect_empty_items()
            ),
            on_mount=AuthState.set_to_dashboard_or_not(to_dashboard)
        ),
        rx.cond(
            (AuthState.show_auth_popup == True),
            rx.dialog.content(
                rx.cond(
                    AuthState.register_mode,
                    rx.vstack(
                        rx.dialog.title("Créer un compte"),
                        rx.input(
                            placeholder="Adresse mail",
                            width="60%",
                            on_change=AuthState.set_username,
                            value=AuthState.username,
                        ),
                        rx.input(
                            placeholder="Mot de passe",
                            type="password",
                            width="60%",
                            on_change=AuthState.set_password,
                            value=AuthState.password,
                        ),
                        rx.input(
                            placeholder="Confirmer le mot de passe",
                            type="password",
                            width="60%",
                            on_change=AuthState.set_confirm_password,
                            value=AuthState.confirm_password,
                        ),
                        rx.button(
                            "S'inscrire",
                            width="60%",
                            bg="#27566B",
                            color="white",
                            on_click=AuthState.register(to_dashboard),
                        ),
                        # GoogleOAuthProvider.create(
                        #     GoogleLogin.create(on_success=AuthState.on_google_success),
                        #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
                        # ),
                        rx.cond(
                            (AuthState.register_error != ""),
                            rx.text(
                                AuthState.register_error,
                                color="red",
                                font_size="0.9em",
                                margin_top="8px",
                            ),
                        ),
                        rx.link(
                            rx.text("Déjà un compte ? Se connecter", font_size="0.8em", color="gray"),
                            on_click=AuthState.open_login_popup,
                        ),
                        spacing="5",
                        align_items="center",
                    ),
                    rx.vstack(
                        rx.dialog.title("Veuillez saisir vos identifiants"),
                        rx.input(
                            placeholder="Adresse mail",
                            width="60%",
                            on_change=AuthState.set_username,
                            value=AuthState.username,
                        ),
                        rx.input(
                            placeholder="Mot de passe",
                            type="password",
                            width="60%",
                            on_change=AuthState.set_password,
                            value=AuthState.password,
                        ),
                        rx.button(
                            "Se connecter",
                            width="60%",
                            bg="#27566B",
                            color="white",
                            on_click=AuthState.login(False),
                        ),
                        # GoogleOAuthProvider.create(
                        #     GoogleLogin.create(on_success=AuthState.on_google_success),
                        #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
                        #     #to_dashboard=to_dashboard
                        # ),
                        rx.cond(
                            (AuthState.login_error != "Cette adresse mail est déjà utilisé."),
                            rx.text(AuthState.login_error, color="red", font_size="0.8em"),
                        ),
                        rx.link(
                            rx.text("Mot de passe oublié ?", font_size="0.8em", color="gray"),
                            href="/"
                        ),
                        rx.link(
                            rx.text("Créer un compte", font_size="0.8em", color="gray"),
                            on_click=AuthState.open_register_popup,
                        ),
                        spacing="5",
                        align_items="center",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                    "Fermer",
                    on_click=AuthState.close_auth_popup,
                    )
                ),
                z_index="1000",
                padding="2rem",
                border_radius="lg",
            ),
        ),
    )

def login_popup(to_dashboard: bool, location: str):
    if to_dashboard:
        button_text = "Espace client"
    else:
        button_text = "Calculer ma prime CEE"
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(rx.text(
                    button_text,
                    weight="bold",
                )
                ),
                type="button",
                size="4",
                on_click=rx.cond(
                    ((AuthState.is_logged_in) & AuthState.to_dashboard),
                    rx.redirect("/dashboard"),
                    AuthState.open_login_popup,
                    # rx.cond(
                    #     (ps.MultiStepFormState.get_missing_arguments != ""),
                    #     rx.toast(ps.MultiStepFormState.get_missing_arguments, duration=5000),
                    #     rx.cond(
                    #         (AuthState.is_logged_in) & (ps.MultiStepFormState.execute_string_function()),
                    #         rx.redirect("/result"),
                    #         AuthState.open_login_popup,
                    #     ),
                    # ),
                ),
                cursor="pointer",
                weight="bold",
                style={"box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",},
                on_mount=ps.MultiStepFormState.detect_empty_items()
            ),
            on_mount=AuthState.set_to_dashboard_or_not(to_dashboard)
        ),
        rx.cond(
            (AuthState.show_auth_popup == True),
            rx.dialog.content(
                rx.cond(
                    AuthState.register_mode,
                    rx.vstack(
                        rx.dialog.title("Créer un compte"),
                        rx.input(
                            placeholder="Adresse mail",
                            width="60%",
                            on_change=AuthState.set_username,
                            value=AuthState.username,
                        ),
                        rx.input(
                            placeholder="Mot de passe",
                            type="password",
                            width="60%",
                            on_change=AuthState.set_password,
                            value=AuthState.password,
                        ),
                        rx.input(
                            placeholder="Confirmer le mot de passe",
                            type="password",
                            width="60%",
                            on_change=AuthState.set_confirm_password,
                            value=AuthState.confirm_password,
                        ),
                        rx.button(
                            "S'inscrire",
                            width="60%",
                            bg="#27566B",
                            color="white",
                            on_click=AuthState.register(to_dashboard),
                        ),
                        # GoogleOAuthProvider.create(
                        #     GoogleLogin.create(on_success=AuthState.on_google_success),
                        #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
                        # ),
                        rx.cond(
                            (AuthState.register_error != ""),
                            rx.text(
                                AuthState.register_error,
                                color="red",
                                font_size="0.9em",
                                margin_top="8px",
                            ),
                        ),
                        rx.link(
                            rx.text("Déjà un compte ? Se connecter", font_size="0.8em", color="gray"),
                            on_click=AuthState.open_login_popup,
                        ),
                        spacing="5",
                        align_items="center",
                    ),
                    rx.vstack(
                        rx.dialog.title("Veuillez saisir vos identifiants"),
                        rx.input(
                            placeholder="Adresse mail",
                            width="60%",
                            on_change=AuthState.set_username,
                            value=AuthState.username,
                        ),
                        rx.input(
                            placeholder="Mot de passe",
                            type="password",
                            width="60%",
                            on_change=AuthState.set_password,
                            value=AuthState.password,
                        ),
                        rx.button(
                            "Se connecter",
                            width="60%",
                            bg="#27566B",
                            color="white",
                            on_click=AuthState.login(to_dashboard=to_dashboard),
                        ),
                        # GoogleOAuthProvider.create(
                        #     GoogleLogin.create(on_success=AuthState.on_google_success),
                        #     client_id=os.getenv("GOOGLE_CLIENT_ID"),
                        #     #to_dashboard=to_dashboard
                        # ),
                        rx.cond(
                            (AuthState.login_error != "Cette adresse mail est déjà utilisé."),
                            rx.text(AuthState.login_error, color="red", font_size="0.8em"),
                        ),
                        rx.link(
                            rx.text("Mot de passe oublié ?", font_size="0.8em", color="gray"),
                            href="/"
                        ),
                        rx.link(
                            rx.text("Créer un compte", font_size="0.8em", color="gray"),
                            on_click=AuthState.open_register_popup,
                        ),
                        spacing="5",
                        align_items="center",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                    "Fermer",
                    on_click=AuthState.close_auth_popup,
                    )
                ),
                z_index="1000",
                padding="2rem",
                border_radius="lg",
            ),
        ),
    )

def contact_popup():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.hstack(
                    rx.icon("mail", size=24),
                    rx.text("Prendre contact", size="3"),
                    align="center",
                ),
                size="3",
                padding="1em",
                variant="solid",
                style={
                    "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                },
                _hover={
                    "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
                    "transform": "scale(1.05)",
                    "transition": "all 0.2s ease-in-out"
                },
                transition="all 0.2s ease-in-out",
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Prendre contact avec un conseiller"),
            rx.dialog.description(
                "Cliquez sur le lien ci-dessous pour sélectionner un créneau.",
            ),
            rx.vstack(
                ts.button_text("prendre rdv", "album"),
                padding="2em", align_items="center"
            ),
            rx.dialog.close(
                ts.button_text("Fermer", "x"),
            ),
        ),
    )