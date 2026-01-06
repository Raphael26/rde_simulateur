import reflex as rx
from fastapi import FastAPI, Request
from models.user import User
from back.auth_class import AuthState
fastapi_app = FastAPI()

@fastapi_app.post("/api/register")
async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    state = AuthState(username=username, password=password)
    state.register()
    if getattr(state, "is_logged_in", False):
        return {"success": True, "message": "Inscription réussie"}
    else:
        return {"success": False, "message": getattr(state, "login_error", "Erreur inconnue")}

# Intégration avec Reflex
app = rx.App(api_transformer=fastapi_app)