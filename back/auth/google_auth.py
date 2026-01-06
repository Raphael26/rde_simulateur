import json
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import reflex as rx
from models.user import User


CLIENT_ID = "TON_CLIENT_ID_GOOGLE"

class State(rx.State):
    id_token_json: str = rx.LocalStorage()

    def on_success(self, id_token: dict):
        self.id_token_json = json.dumps(id_token)
        # Vérification et ajout utilisateur ici
        info = verify_oauth2_token(
            id_token["credential"],
            requests.Request(),
            CLIENT_ID,
        )
        email = info["email"]
        name = info.get("name", "")
        with rx.session() as session:
            user = session.exec(
                User.select().where(User.username == email)
            ).first()
            if not user:
                user = User(username=email, password="")
                session.add(user)
                session.commit()
                session.refresh(user)
        # Connexion et autres updates d'état ici
        self.connected_user = email
        self.is_logged_in = True
        return rx.redirect("/sector/")