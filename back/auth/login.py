import reflex as rx
from fastapi import FastAPI, Request
from models.user import User
from back.auth_class import AuthState

from fastapi import Request

fastapi_app = FastAPI()

@fastapi_app.post("/api/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    state = AuthState(username=username, password=password)
    state.login()
    if getattr(state, "is_logged_in", False):
        return {"success": True, "message": "Connexion réussie"}
    else:
        return {"success": False, "message": getattr(state, "login_error", "Erreur inconnue")}