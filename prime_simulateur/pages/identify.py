import reflex as rx
from prime_simulateur import prime_simulateur as ps
from back.auth_class import AuthState
from back.auth.react_auth_google import GoogleOAuthProvider, GoogleLogin
import os


@rx.page(route="/identify", title="RDE Simulateur")
def page_identify():
    ps.MultiStepFormState.set_page_progress(6)
    #ps.MultiStepFormState.execute_string_function()
    #ps.MultiStepFormState.save_simulation_result()
    content = rx.vstack(
        rx.text("")
    ),
    return ps.multi_step_layout(content, 0)
