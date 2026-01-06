import reflex as rx

def _on_success_signature(data: rx.Var[dict]) -> tuple[rx.Var[dict]]:
    return (data, )

class GoogleOAuthProvider(rx.Component):
    library = "@react-oauth/google"
    tag = "GoogleOAuthProvider"
    client_id: rx.Var[str]

class GoogleLogin(rx.Component):
    library = "@react-oauth/google"
    tag = "GoogleLogin"
    on_success: rx.EventHandler[_on_success_signature]