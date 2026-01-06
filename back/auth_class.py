from collections import defaultdict
from pprint import pprint
from typing import Optional

import reflex as rx
import hashlib
import json

from models.simulation import SimulationResult
from prime_simulateur import function_loader
from prime_simulateur import prime_simulateur as ps
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import os
from models.user import User
from dotenv import load_dotenv
from sqlmodel import select
load_dotenv()
import plotly.express as px
import numpy as np

class AuthState(rx.State):
    research_input: str = ""
    show_auth_popup: bool = False
    register_mode: bool = False
    user_id: Optional[int] = None
    username: str = ""
    password: str = ""
    is_logged_in: bool = False
    confirm_password: str = ""
    register_error: str = ""
    login_error: str = ""
    connected_user: str = ""
    user_phone_number: str = ""
    user_first_name: str = ""
    user_last_name: str = ""
    user_simulations: list[dict] = []
    filtered_simulations: list[dict] = []
    number_of_simulation: int = 0
    total_euro: float = 0.00
    average_euro: float = 0.00
    total_cumacs: float = 0.00
    average_cumacs: float = 0.00
    most_sector: str = ""
    most_typology: str = ""
    most_department: str = ""
    last_simulation_order:int = 0
    to_dashboard: bool = False
    pdf_list: list[str] = []
    filter_by_sector: bool = False
    filter_by_typology: bool = False
    simulations_sorted_by_sector: list[dict] = []
    simulations_sorted_by_typology: list[dict] = []

    @rx.event
    def set_research_input_simulation_name(self, keyword):
        self.research_input = keyword
        self.filter_by_sector = False
        self.filter_by_typology = False
        self.filtered_simulations = [
            sim for sim in self.user_simulations
            if sim.get("name") and keyword.lower() in sim["name"].lower()
        ]
        #print(self.filtered_simulations)
        yield

    def clear_research_input_simulations(self):
        self.research_input = ""

    @rx.event
    def sort_by_secteur_count(self):
        self.research_input = ""
        self.filter_by_typology = False
        self.filter_by_sector = not self.filter_by_sector
        if not self.filter_by_sector:
            return
        secteur_dict = defaultdict(list)
        for sim in self.user_simulations:
            secteur = sim.get("secteur")
            secteur_dict[secteur].append(sim)
        secteurs_tries = sorted(
            secteur_dict.values(),
            key=len,
            reverse=True
        )
        sorted_flat = [sim for group in secteurs_tries for sim in group]
        self.simulations_sorted_by_sector = sorted_flat
        yield

    @rx.event
    def sort_by_typology_count(self):
        self.research_input = ""
        self.filter_by_sector = False
        self.filter_by_typology = not self.filter_by_typology
        if not self.filter_by_typology:
            return
        typology_dict = defaultdict(list)
        for sim in self.user_simulations:
            typology = sim.get("typologie")
            typology_dict[typology].append(sim)
        typologies_tries = sorted(
            typology_dict.values(),
            key=len,
            reverse=True
        )
        sorted_flat = [sim for group in typologies_tries for sim in group]
        self.simulations_sorted_by_typology = sorted_flat
        yield


    def set_to_dashboard_or_not(self, to_dashboard):
        self.to_dashboard = to_dashboard

    def is_user_logged_in(self):
        print(f"login ? {self.is_logged_in}")
        if self.is_logged_in == True:
            print("logged in")
            return True
        else:
            print("not logged")
            return False

    def on_google_success(self, id_token: dict):
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        info = verify_oauth2_token(
            id_token["credential"],
            requests.Request(),
            CLIENT_ID,
        )
        email = info["email"]
        name = info.get("name", "")
        oAuth = True
        return self.google_login(email)

    def open_login_popup(self):
        if self.connected_user != "":
            return rx.redirect("/dashboard")
        self.username = ""
        self.password = ""
        self.confirm_password = ""
        self.show_auth_popup = True
        self.register_mode = False

    def open_register_popup(self):
        self.username = ""
        self.password = ""
        self.show_auth_popup = True
        self.register_mode = True

    def close_auth_popup(self):
        self.show_auth_popup = False
        self.register_mode = False

    def set_username(self, value: str):
        self.username = value

    def set_password(self, value: str):
        self.password = value

    def set_confirm_password(self, value: str):
        self.confirm_password = value

    def google_login_api(self, email: str, name: str):
        return self.google_login(email, name)

    def login(self, to_dashboard: bool):
        hashed_password = hashlib.sha256(self.password.encode()).hexdigest()
        with rx.session() as session:
            user = session.query(User).filter_by(username=self.username).first()
            if user and user.password == hashed_password:
                self.is_logged_in = True
                self.connected_user = self.username
                self.user_first_name = user.first_name
                self.user_last_name = user.last_name
                self.user_phone_number = user.phone_number
                self.user_id = self.get_user_id
                self.login_error = ""
                self.username = ""
                self.password = ""
                self.show_auth_popup = False
                print(f"first name {self.user_first_name}, last name {self.user_last_name}, phone number {self.user_phone_number}")
                if to_dashboard == True:
                    return rx.redirect("/dashboard/")
                else:
                    return ps.MultiStepFormState.save_simulation_result(user_id=self.get_user_id)
                    #return ps.MultiStepFormState.execute_string_function()
            else:
                self.login_error = "Identifiant ou mot de passe incorrect."
                self.is_logged_in = False

    def google_login(self, email: str):
        print(f"Connexion Google de l'utilisateur : {email}")
        with rx.session() as session:
            user = session.query(User).filter_by(username=email).first()
            if not user:
                user = User(username=email, password="", oAuth=True)
                session.add(user)
                session.commit()
                session.refresh(user)
                if AuthState.to_dashboard:
                    return rx.redirect("/dashboard")
                if not AuthState.to_dashboard:
                    return ps.MultiStepFormState.execute_string_function()
            self.connected_user = email
            self.user_id = self.get_user_id
            self.user_first_name = user.first_name
            self.user_last_name = user.last_name
            self.user_phone_number = user.phone_number
            self.is_logged_in = True
            self.username = ""
            self.password = ""
            self.confirm_password = ""
            self.login_error = ""
            self.register_error = ""
            self.show_auth_popup = False
            return ps.MultiStepFormState.execute_string_function()


    def register(self, to_dashboard):
        hashed_password = hashlib.sha256(self.password.encode()).hexdigest()
        with rx.session() as session:
            existing = session.exec(
                User.select().where(User.username == self.username)
            ).first()
            if existing:
                print("existing")
                self.register_error = "Cette adresse mail est déjà utilisé."
                return
            user = User(username=self.username, password=hashed_password)
            session.add(user)
            session.commit()
            session.refresh(user)
            self.is_logged_in = True
            self.connected_user = self.username
            self.user_id = self.get_user_id
            self.username = ""
            self.password = ""
            self.confirm_password = ""
            self.register_error = ""
            self.show_auth_popup = False
            if to_dashboard:
                return rx.redirect("/dashboard/")
            else:
                return ps.MultiStepFormState.execute_string_function()

    @rx.var
    def get_user_id(self) -> Optional[int]:
        with rx.session() as session:
            result = session.exec(
                User.select().where(User.username == self.connected_user)
            ).first()
            #print(f"result is {result}")
            if result:
                #print(f"found id {result.id}")
                self.user_id = result.id
                return self.user_id
            else:
                #print("not found")
                self.user_id = None
                return None


    def disconnect(self):
        self.username = ""
        self.password = ""
        self.is_logged_in = False
        self.confirm_password = ""
        self.register_error = ""
        self.login_error = ""
        self.connected_user = ""
        self.user_first_name = ""
        self.user_last_name = ""
        self.user_phone_number = ""
        print("disconnection")
        return rx.redirect("/")

    @rx.event
    def get_next_simulation_number(self):
        with rx.session() as session:
            simulations = list(session.exec(
                SimulationResult.select().where(SimulationResult.user_id == self.user_id)
            ))
            count = len(simulations)
        self.last_simulation_order = count + 1

    def fetch_simulations_result(self):
        with rx.session() as session:
            all_simulations = list(session.exec(
                SimulationResult.select().where(SimulationResult.user_id == self.user_id)
            ))
            if all_simulations:
                sorted_simulations = sorted(all_simulations, key=lambda sim: sim.id)
                self.user_simulations = [
                    {**sim.__dict__, "order": idx + 1}
                    for idx, sim in enumerate(sorted_simulations)
                ]
                self.number_of_simulation = len(all_simulations)
                self.total_euro = sum(getattr(sim, "result_eur", 0) for sim in all_simulations)
                self.get_average_euro()
                self.get_average_cumacs()
            else:
                self.user_simulations = []

    def fetch_simulations_result_admin(self):
        with rx.session() as session:
            all_simulations = session.exec(
                select(SimulationResult)
            ).all()
            if all_simulations:
                sorted_simulations = sorted(all_simulations, key=lambda sim: sim.id)
                self.user_simulations = [
                    {**sim.__dict__, "order": idx + 1}
                    for idx, sim in enumerate(sorted_simulations)
                ]
                #print(f"simulations are : {self.user_simulations}")
                self.number_of_simulation = len(all_simulations)
                self.total_euro = sum(getattr(sim, "result_eur", 0) for sim in all_simulations)
                self.get_average_euro()
                self.get_average_cumacs()
                self.get_most_sector()
                self.get_most_typology()
                self.get_most_department()
            else:
                self.user_simulations = []



    def sort_simulations(self):
        result = [c for c in AuthState.user_simulations if self.query.lower() in c["fiche"].lower()]
        result.sort(key=lambda c: c[self.sort_by], reverse=not self.sort_asc)
        self.user_simulations = result

    def secteur_typologie_chart(self, data) -> rx.Component:
        combinaisons = [(item['secteur'], item['typologie']) for item in data]
        combinaisons_array = np.array(combinaisons)
        secteurs = combinaisons_array[:, 0]
        typologies = combinaisons_array[:, 1]
        uniques, counts = np.unique(combinaisons_array, axis=0, return_counts=True)
        secteurs_uniques = uniques[:, 0]
        typologies_uniques = uniques[:, 1]
        parents = list(secteurs_uniques)
        labels = list(typologies_uniques)
        values = list(counts)
        fig = px.sunburst(
            names=labels,
            parents=parents,
            values=values,
        )
        return rx.center(
            rx.plotly(data=fig)
        )

    def get_average_euro(self):
        values = [item["result_eur"] for item in self.user_simulations if item.get("result_eur") is not None]
        if values:
            print(sum(values))
            print(len(values))
            self.average_euro = sum(values) / len(values)
        else:
            self.average_euro = 0

    def get_average_cumacs(self):
        values = [item["result_cumacs"] for item in self.user_simulations if item.get("result_cumacs") is not None]
        if values:
            print(sum(values))
            print(len(values))
            self.average_cumacs = sum(values) / len(values)
        else:
            self.average_cumacs = 0

    def get_most_sector(self):
        sectors = [item["secteur"] for item in self.user_simulations if item.get("secteur")]
        if not sectors:
            self.most_sector = "aucun"
            return
        counts = {}
        for sector in sectors:
            counts[sector] = counts.get(sector, 0) + 1
        max_count = max(counts.values())
        if max_count == 1:
            self.most_sector = "aucun"
        else:
            self.most_sector = [k for k, v in counts.items() if v == max_count][0]

    def get_most_typology(self):
        typologies = [item["typologie"] for item in self.user_simulations if item.get("typologie")]
        if not typologies:
            self.most_typology = "aucun"
            return
        counts = {}
        for typology in typologies:
            counts[typology] = counts.get(typology, 0) + 1
        max_count = max(counts.values())
        if max_count == 1:
            self.most_typology = "aucun"
        else:
            self.most_typology = [k for k, v in counts.items() if v == max_count][0]

    def get_most_department(self):
        departments = [item["departement"] for item in self.user_simulations if item.get("departement")]
        if not departments:
            self.most_department = "aucun"
            return
        counts = {}
        for department in departments:
            counts[department] = counts.get(department, 0) + 1
        max_count = max(counts.values())
        if max_count == 1:
            self.most_department = "aucun"
        else:
            self.most_department = [k for k, v in counts.items() if v == max_count][0]

    def update_profile(self, form_data: dict):
        print(form_data)
        with rx.session() as session:
            user = session.exec(
                User.select().where(User.id == self.user_id)
            ).first()
            if user:
                user.phone_number = form_data.get("phone_number", user.phone_number)
                user.first_name = form_data.get("first_name", user.first_name)
                user.last_name = form_data.get("last_name", user.last_name)
                session.add(user)
                session.commit()
                session.refresh(user)
                self.user_phone_number = user.phone_number
                self.user_first_name = user.first_name
                self.user_last_name = user.last_name
                return rx.redirect("/dashboard")

    @rx.event
    def get_pdf_list(self, folder_path, research):
        options = ["..."]
        pdf_list = []
        if not os.path.exists(folder_path):
            print("nothing in folder_path")
            self.pdf_list = []
            return
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf") and research in filename:
                pdf_list.append(filename)
        self.pdf_list = sorted(pdf_list, key=lambda x: options.index(x) if x in options else 999)
