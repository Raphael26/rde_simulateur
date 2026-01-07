import datetime

import reflex as rx
import reflex_chakra as rc

import variables
import ast
from typing import Union

from models.MprArticles import MprArticles
from prime_simulateur.chatbot import chatbot_popup
from prime_simulateur.pages import date_department, sector, typology, choice_pdf, simulator, identify, result_page, \
    results_history, profile, result_details, beneficiary_page, mpr_list_page
from prime_simulateur.admin import admin_page, mpr_page
# from prime_simulateur.pdf_export.page_functions import create_page
from prime_simulateur import function_loader
from prime_simulateur.components import popups, text_styles
from models.simulation import SimulationResult
from back.auth_class import AuthState

import os
import json
from dotenv import load_dotenv
from typing import Any
from supabase import create_client, Client

load_dotenv()

BUCKET_NAME = "fiches-operations"

# Initialize Supabase client
try:
    # Supabase connection
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY"),
    )
except Exception as e:
    print(f"Error initializing supabase clients: {e}")


def read_file_from_bucket(
    supabase_client,
    bucket_name: str,
    file_path: str,
    file_type: str = "txt",
    encoding: str = "utf-8",
) -> Any:
    # Read file from bucket
    try:
        raw = supabase_client.storage \
            .from_(bucket_name) \
            .download(file_path)
    except Exception as e:
        print(repr(e))

    if file_type == "txt":
        return raw.decode(encoding)
    elif file_type == "json":
        return json.loads(raw)

pages_url = ["/", "/options/", "/date-department/", "/sector/", "/typology/", "/choice-pdf/", "/beneficiary/", "/simulator/"]

class State(rx.State):
    @rx.var
    def current_path(self) -> str:
        return self.router.page.raw_path

class MultiStepFormState(rx.State):
    data: dict = {}
    check_result: bool = False
    show_popup: bool = False
    show_drawer_left: bool = False
    progress_page: int = 0
    progress_percent: int = 0
    date_start:str = datetime.date.today().isoformat()
    date_signature: str = datetime.date.today().isoformat()
    research_department: str = ""
    list_department: list[str] = []
    department: str = ""
    truncated_department:str = ""
    sector: str = ""
    typology: str = ""
    sector_abbreviation: str = ""
    typology_abbreviation: str = ""
    research_abbreviation: str = ""
    research_manually: str = "Non"
    research_input: str = ""
    pdf_names: list[str] = []
    pdf_mapping: dict[str, str] = {}
    is_pdf_linked: bool = False
    all_linked_articles: list[dict] = []
    keyword_search_pdf: dict[str, str] = {}
    pdf_to_check: str = ""
    selected_pdf: str = ""
    selected_pdf_description: str = ""
    truncated_pdf: str = ""
    show_preview: bool = False
    show_mpr_list : bool = False
    preview_pdf: str = ""
    simulator_choices: dict[str, dict[str, str]] = {}
    simulator_input_choices: dict[str, dict[str, str]] = {}
    simulator_var_matching: dict[str, Union[str, int, float]] = {}
    simulator_function_requirements: dict[str, dict[str, str]] = {}
    simulator_function_params: dict[str, str] = {}
    simulator_string_function: str = """def test(a, b):
                                      pass"""
    simulator_result: float = 0.00
    email:str = ""
    simulation_saved: bool = False
    simulation_name: str = "simulation"
    beneficiary: str = ""
    toast_shown: bool = False
    missing_arguments: str = ""
    error: str = ""

    @rx.event
    def show_sector_toast(self):
        mpr_alert = """Certains articles du secteur sont éligible à MaPrimeRénov'. Veuillez consulter la liste en cliquant sur 
        Articles MaPrimeRénov' (MPR) au dessus de la liste des fiches.
            """
        if self.sector == "Résidentiel" and not self.toast_shown:
            self.toast_shown = True
            yield rx.toast(
                mpr_alert,
                position="bottom-left",
                duration=30000,
                close_button=True,
            )

    @rx.event
    def init_simulator(self):
        self.list_department = []
        self.research_department = ""
        self.department = ""
        self.truncated_department = ""
        self.sector = ""
        self.typology = ""
        self.sector_abbreviation = ""
        self.typology_abbreviation = ""
        self.research_abbreviation = ""
        self.research_manually = "Non"
        self.pdf_names = []
        self.pdf_mapping = {}
        self.selected_pdf = ""
        self.selected_pdf_description = ""
        self.show_preview = False
        self.preview_pdf = ""
        self.beneficiary = ""
        self.simulator_choices = {}
        self.simulator_input_choices = {}
        self.simulator_var_matching = {}
        self.simulator_function_requirements = {}
        self.simulator_function_params = {}
        self.simulator_string_function = """def test(a, b):
                                              pass"""
        self.simulator_result = 0.00
        self.email = ""
        self.simulation_saved = False
        self.simulation_name = "simulation"
        self.beneficiary = ""
        self.error = ""

        return rx.redirect("/date-department")

    def erase_inputs(self):
        self.list_department = []
        self.research_department = ""
        self.department = ""
        self.truncated_department = ""
        self.sector = ""
        self.typology = ""
        self.sector_abbreviation = ""
        self.typology_abbreviation = ""
        self.research_abbreviation = ""
        self.research_manually = "Non"
        self.research_input = ""
        self.pdf_names = []
        self.pdf_mapping = {}
        self.pdf_to_check = ""
        self.all_linked_articles = []
        self.selected_pdf = ""
        self.selected_pdf_description = ""
        self.show_preview = False
        self.preview_pdf = ""
        self.simulator_choices = {}
        self.simulator_input_choices = {}
        self.simulator_var_matching = {}
        self.simulator_function_requirements = {}
        self.simulator_function_params = {}
        self.simulator_string_function = """def test(a, b):
                                                  pass"""
        self.simulator_result = 0.00
        self.email = ""
        self.simulation_saved = False
        self.toast_shown = False
        self.missing_arguments = ""
        self.error = ""

    @rx.event
    def set_check_result(self):
        if self.simulator_result == 0.00:
            print("result not existing")
            self.check_result = False
        else:
            print("ok")
            self.check_result = True

    @rx.event
    def redirect_to_dashboard(self):
        return rx.redirect("/dashboard")

    def open_drawer(self):
        self.show_drawer_left = not (self.show_drawer_left)
        print(self.show_drawer_left)

    def close_drawer(self):
        self.show_drawer_left = False

    def open_popup(self):
        self.show_popup = True

    def close_popup(self):
        self.show_popup = False

    def set_date_signature(self, value: str):
        self.date_signature = value

    @rx.event
    def set_research_department(self, value: str):
        self.research_department = value
        self.list_department = [
            k for k in variables.Variables.departements_france.keys() if value.lower() in k.lower()
        ]

    @rx.event
    def set_department(self, value: str):
        self.department = value

    @rx.var
    def get_list_departements(self) -> list[str]:
        sorted_list_department = [k for k in variables.Variables.departements_france.keys() if k != "..."]
        return sorted_list_department

    @rx.var
    def get_truncated_department(self) -> str:
        nom_sans_numero = " ".join(self.department.split(" ")[1:])
        return choice_pdf.truncate_text(nom_sans_numero, 10)

    def get_page_progress(self) -> int:
        return self.progress_page

    def set_page_progress(self, progress):
        self.progress_page = progress

    @rx.event
    def set_simulation_name(self, value):
        self.simulation_name = value

    @rx.event
    def set_research_manually(self, value: str):
        self.research_manually = value
        print(f"set to {value}")
        if value == "Oui":
            return rx.redirect("/choice-pdf")

    @rx.event
    def init_research_input(self):
        self.research_input = ""
        self.keyword_search_pdf = {}

    @rx.event
    def set_research_input(self, value: str):
        self.research_input = value
        # print(self.research_input)
        # print(f"for {self.pdf_mapping}")
        self.keyword_search_pdf = {}
        self.pdf_mapping = self.get_description_all()
        for k, v in self.pdf_mapping.items():
            # print(f"k is {k} and v is {v}")
            if self.research_input.lower() in v.lower():
                # print(f"research input is {v[1]}")
                self.keyword_search_pdf[k] = v
                # print(f"found for {value}: {self.keyword_search_pdf}")

    @rx.event
    def save_and_go_to_next(self, form_data: dict):
        self.data.update(form_data)
        print("next")
        current_path = self.router.page.raw_path
        print(f"current path {current_path}")
        try:
            self.progress_page = pages_url.index(current_path)
        except ValueError:
            print("ERROR")
            self.progress_page = 0

        if self.progress_page < len(pages_url) - 1:
            self.progress_page += 1
            print(f"progress after next is {self.progress_page}")
            return rx.redirect(pages_url[self.progress_page])

    @rx.event
    def go_to_previous(self):
        current_path = self.router.page.raw_path
        print("back")
        print(current_path)
        try:
            self.progress_page = pages_url.index(current_path)
        except ValueError:
            self.progress_page = 0
        if self.progress_page == 0:
            print("is 0")
            return

        self.progress_page -= 1
        print(f"progress after back is {self.progress_page}")
        return rx.redirect(pages_url[self.progress_page])

    @rx.event
    def select_sector(self, value: str, abbreviation: str):
        self.sector = value
        self.sector_abbreviation = abbreviation
        self.pdf_mapping = self.get_description(self.sector_abbreviation)
        return rx.redirect("/typology")

    @rx.event
    def select_typology(self, value: str, abbreviation: str):
        self.typology = value
        self.typology_abbreviation = abbreviation
        self.get_pdf_names(folder_path="assets/downloaded_pdfs", research=self.get_research_abbreviation())
        self.pdf_mapping = self.get_description(self.get_research_abbreviation())
        return rx.redirect("/choice-pdf")

    @rx.var
    def get_truncated_pdf(self) -> str:
        return choice_pdf.truncate_text(self.selected_pdf, 20)

    def get_research_abbreviation(self) -> str:
        return (f"{self.sector_abbreviation}-{self.typology_abbreviation}-")

    @rx.var
    def available_typologies(self) -> list[dict]:
        current_sector = self.sector
        mapping = variables.Variables.sector_with_typology_dict.get(current_sector, {})

        enriched_typologies = []
        for name, abbr in mapping.items():
            icon = variables.Variables.typology_dict_list.get(name, {}).get("icon", "circle-help")
            enriched_typologies.append(
                {
                    "name": name,
                    "abbr": abbr,
                    "icon": icon
                }
            )
        return enriched_typologies

    def extract_inner_keys(data: dict) -> list[str]:
        keys = []
        for value in data.values():
            if isinstance(value, dict):
                keys.extend(value.keys())
        return list(keys)

    @rx.event
    def get_pdf_names(self, folder_path, research):
        options = ["..."]
        pdf_names = []
        if not os.path.exists(folder_path):
            print("nothing in folder_path")
            self.pdf_names = []
            return
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf") and research in filename:
                pdf_names.append(filename)
        self.pdf_names = sorted(pdf_names, key=lambda x: options.index(x) if x in options else 999)

    @rx.event
    def get_description(self, abbreviation: str) -> dict:
        json_path = 'assets/fiche_names_mapping.json'
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            matches = {k: v for k, v in data.items() if k.startswith(abbreviation)}
            return matches if matches else {f"No match found for {abbreviation}": ""}
        except FileNotFoundError:
            return {"error": f"JSON not found at {json_path}"}
        except json.JSONDecodeError:
            return {"error": "Error decoding JSON"}

    @rx.event
    def get_description_all(self) -> dict:
        json_path = 'assets/fiche_names_mapping.json'
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            matches = {k: v for k, v in data.items()}
            return matches
        except FileNotFoundError:
            return {"error": f"JSON not found at {json_path}"}
        except json.JSONDecodeError:
            return {"error": "Error decoding JSON"}

    def update_function_params(self, variables_mapping, variables_matching, function_params):
        for label, param_name in variables_matching.items():
            if param_name in function_params and label in variables_mapping:
                function_params[param_name] = variables_mapping[label]

        mapped_param_names = set(variables_matching.values())
        for param_name in function_params:
            if param_name not in mapped_param_names:
                variables_mapping[param_name] = {}

        return function_params, variables_mapping

    def extract_parameters(self, function_str: str):
        tree = ast.parse(function_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                return {arg.arg: "" for arg in node.args.args}
        return {}

    def get_simulator_function_params(self):
        return self.simulator_function_params

    def set_typology_from_pdf(self):
        typology_abbr = self.selected_pdf.split("-")[1]
        for typology_key, value in variables.Variables.typology_dict_list.items():
            if value.get("abbr") == typology_abbr:
                self.typology = typology_key
        return None

    def get_simulator_string_function(self):
        return self.simulator_string_function

    def set_selected_pdf(self, pdf_name: str, pdf_description: str):
        self.selected_pdf = pdf_name
        self.selected_pdf_description = pdf_description
        fiche_code = self.selected_pdf.replace(".pdf", "").strip()
        self.set_typology_from_pdf()
        if self.research_manually == "Oui":
            pass
        try:
            function_param_values_labeled = read_file_from_bucket(
                supabase,
                BUCKET_NAME,
                file_path=f"/{fiche_code}/function_param_values_labeled.json",
                file_type="json"
            )
            variables_mapping = read_file_from_bucket(
                supabase,
                BUCKET_NAME,
                file_path=f"/{fiche_code}/variables_mapping.json",
                file_type="json"
            )
            variables_matching = read_file_from_bucket(
                supabase,
                BUCKET_NAME,
                file_path=f"/{fiche_code}/variables_matching.json",
                file_type="json"
            )
            string_function = read_file_from_bucket(
                supabase,
                BUCKET_NAME,
                file_path=f"/{fiche_code}/string_function.txt",
                file_type="txt"
            )
        except Exception as e:
            print(f"error is {e}")
            self.selected_pdf = ""
            self.selected_pdf_description = ""
            return rx.toast("Cette fiche n'est pas encore disponible !", duration=5000)
        # print(f"param value is : {function_param_values_labeled}")
        # print(f"mapping is : {variables_mapping}")
        # print(f"matching is : {variables_matching}")
        self.simulator_choices = function_param_values_labeled
        self.simulator_input_choices = variables_mapping
        self.simulator_var_matching = variables_matching
        self.simulator_function_params = self.extract_parameters(string_function)
        self.simulator_string_function = string_function

        print(f"string function is : {self.simulator_string_function}")
        #self.simulator_loaded_function = function_loader.FunctionLoader(self.simulator_string_function)
        #print(f"input parameters are : {self.simulator_function_params}")
        print(self.update_function_params(self.simulator_input_choices, self.simulator_var_matching, self.simulator_function_params))
        for key, value in variables_mapping.items():
            print(key)
            list_options = list(value.keys())
            print(list_options)
        func = function_loader.FunctionLoader(string_function)
        #print(f"needed params are: {func.get_parameters()}")
        self.simulator_function_requirements = func.get_parameters()
        print(f"get params: {self.simulator_function_requirements}")

        return rx.redirect("/beneficiary")

    def fetch_linked_articles(self):
        with rx.session() as session:
            all_simulations = session.exec(
                MprArticles.select()
            ).all()
            if all_simulations:
                sorted_linked_articles = sorted(all_simulations, key=lambda sim: sim.id)
                self.all_linked_articles = [
                    {**sim.__dict__, "order": idx + 1}
                    for idx, sim in enumerate(sorted_linked_articles)
                ]
                print(f"linked articles are : {self.all_linked_articles}")
            else:
                self.all_linked_articles = []

    def set_pdf_to_check(self, filename):
        self.pdf_to_check = filename
        #self.pdf_to_check = "BAR-TH-101.pdf"
        print(f"set to {self.pdf_to_check}")

    @rx.var
    def find_in_linked_articles(self) -> bool:
        print(f"pdf to check is : {self.pdf_to_check}")
        self.is_pdf_linked = any(self.pdf_to_check == d.get("pdf_file") for d in self.all_linked_articles)
        print(self.is_pdf_linked)
        return self.is_pdf_linked

    # @rx.var
    # def is_pdf_linked(self) -> bool:
    #     print(f"pdf is {self.pdf_to_check}")
    #     print(f"is pdf linked articles : {self.all_linked_articles}")
    #     result = any(self.pdf_to_check == d.get("pdf_file") for d in self.all_linked_articles)
    #     print(result)
    #     return result

    @rx.event
    def set_param(self, value_name: str, key: str, value: str):
        #self.detect_empty_items()
        try:
            cast_value = int(value)
        except ValueError:
            try:
                cast_value = float(value)
            except ValueError:
                cast_value = value
        #print(f"value name is : {value_name}")
        if value_name in self.simulator_function_params:
            print(f"choices were {self.simulator_choices}")
            if value == "Oui":
                cast_value = True
            elif value == "Non":
                cast_value = False
            self.simulator_function_params[key] = cast_value
        else:
            alt_key = self.simulator_var_matching.get(key)
            #print(f"alt_key is {self.simulator_var_matching} and key is {key}")
            if key and key in self.simulator_function_params:
                #print(f"{key} is in and we will giv it {self.simulator_input_choices[value_name].get(cast_value)}")
                self.simulator_function_params[key] = self.simulator_input_choices[value_name].get(cast_value)
            else:
                print(f"Key '{key}' not in simulator_function_params et de simulator_var_matching.")
        print(self.simulator_function_params)

    def detect_empty_items(self):
        # if self.simulator_function_params == {}:
        #     return rx.text("")
        #print(f"this is {self.simulator_var_matching}")
        empty_keys = [
            key
            for key, value in self.simulator_function_params.items()
            if value == "" or value is None or isinstance(value, dict)
        ]
        if not empty_keys:
            self.missing_arguments = ""
        else:
            print(f"missings are : {empty_keys}")
            self.missing_arguments = f"Les clés suivantes contiennent des valeurs vides : {', '.join(empty_keys)}"

    @rx.var
    def get_missing_arguments(self) -> str:
        self.detect_empty_items()
        return self.missing_arguments

    def execute_string_function(self):
        if self.selected_pdf == "":
            return rx.redirect("/dashboard")
        self.show_drawer_left = False
        print(f"function string to be executed is {self.simulator_string_function}")
        # self.detect_empty_items()
        # if self.missing_arguments != "":
        #     return rx.toast(self.missing_arguments, duration=5000)
        try:
            func = function_loader.FunctionLoader(self.simulator_string_function)
            # print(f"string function params : {dict(self.simulator_function_params)}")
            self.simulator_result = func.call_with_dict(dict(self.simulator_function_params))
        except Exception as e:
            print(f"error is {e}")
            self.error = str(e)
            return rx.toast(str(e), duration=10000)
            # if "Error calling function" in str(e):
            #     return rx.redirect("/dashboard/")
            # else:
            #     return rx.toast(str(e), duration=10000)
        # print(func.get_parameters())
        print(100 * '=')
        print(self.simulator_result)
        return rx.redirect("/result/")


    def open_preview(self):
        print("open preview")
        self.show_preview = True

    def toggle_mpr_list(self):
        print("toggle")
        self.show_mpr_list = True

    def close_preview(self):
        print("close preview")
        self.show_preview = False

    @rx.event
    def set_beneficiary(self, value):
        self.beneficiary = value

    @rx.event
    def save_simulation_result(self, user_id):
        #MultiStepFormState.execute_string_function()
        if not self.simulation_saved and self.selected_pdf_description != "" and self.selected_pdf != "":
            #print(f"user_id is {user_id}")
            with rx.session() as session:
                simulation = SimulationResult(
                    user_id=user_id,
                    name=self.simulation_name.capitalize(),
                    chosen_date=self.date_signature,
                    departement=self.department,
                    secteur=self.sector,
                    typologie=self.typology,
                    fiche=self.selected_pdf.replace(".pdf", "").strip(),
                    description=self.selected_pdf_description,
                    parameters=str(self.simulator_function_params),
                    result_eur=f"{(self.simulator_result * 0.0065):.2f}",
                    result_cumacs=f"{self.simulator_result:.2f}",
                    date_simulation=self.date_start,
                    beneficiary=self.beneficiary,
                )
                self.simulation_saved = True
                session.add(simulation)
                session.commit()
                session.refresh(simulation)
                print("simulation saved")
        return rx.redirect("/dashboard")


def show_completion_steps():
    return rx.cond(
        State.current_path != "/options/",
        rc.stepper(
            rc.step(
                rc.step_indicator(
                    rc.step_status(
                        complete="", active="1", incomplete="1"
                    ),
                ),
                rc.box(
                    rc.step_title("Données"),
                    rc.step_description(MultiStepFormState.date_signature, style={"font_size": "0.7em"}),
                    rc.step_description(
                        rx.cond(
                            MultiStepFormState.department.length() > 10,
                            MultiStepFormState.department[:10] + "...",
                            MultiStepFormState.department
                        ), style={"font_size": "0.8em"},
                    ),
                ),
                rc.step_separator(),
            ),
            rc.step(
                rc.step_indicator(
                    rc.step_status(
                        complete="", active="2", incomplete="2"
                    ),
                ),
                rc.box(
                    rc.step_title("Secteur"),
                    rc.step_description(MultiStepFormState.sector),
                ),
                rc.step_separator(),
            ),
            rc.step(
                rc.step_indicator(
                    rc.step_status(
                        complete="", active="3", incomplete="3"
                    ),
                ),
                rc.box(
                    rc.step_title("Typologie"),
                    rc.step_description(MultiStepFormState.typology),
                ),
                rc.step_separator(),
            ),
            rc.step(
                rc.step_indicator(
                    rc.step_status(
                        complete="", active="4", incomplete="4"
                    ),
                ),
                rc.box(
                    rc.step_title("Opérations"),
                    rc.step_description(MultiStepFormState.get_truncated_pdf, style={"font_size": "0.7em"}),
                ),
                rc.step_separator(),
            ),
            rc.step(
                rc.step_indicator(
                    rc.step_status(
                        complete="", active="5", incomplete="5"
                    ),
                ),
                rc.box(
                    rc.step_title("Simulateur"),
                ),
            ),
            size="lg",
            colorScheme="gray",
            orientation="horizontal",
            index=int(MultiStepFormState.progress_percent / 25),
            width="98%",
            margin_bottom="3em"
        )
    )


def menu_drawer():
    return rc.vstack(
        rc.button(
            rx.hstack(
                rx.icon("menu"),
                rx.text("Menu"),
            ),
            on_click=MultiStepFormState.open_drawer,
            style={
                "box_shadow": "0 4px 6px rgba(0,0,0,0.1)",
            },
            margin="2em",
            on_mount=MultiStepFormState.close_drawer,
        ),
        rx.cond(
            MultiStepFormState.show_drawer_left == True,
            rx.drawer.root(
                rx.drawer.overlay(),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            # Header: image à gauche, chevron à droite
                            rx.hstack(
                                rx.image(
                                    src="/RDE_consulting_icon.jpg",
                                    width="50%",
                                    on_click=rx.redirect("/"),
                                    cursor="pointer"
                                ),
                                rx.spacer(),
                                rx.drawer.close(
                                    rx.button(
                                        rx.icon("chevron-left"),
                                        on_click=MultiStepFormState.open_drawer,
                                        size="1",
                                        color_scheme="green",
                                        style={"box_shadow": "0 4px 6px rgba(0,0,0,0.1)"}
                                    )
                                ),
                                width="100%",
                                align_items="center",
                                margin_bottom="1em"
                            ),
                            text_styles.title_text("Menu"),
                            rx.box(
                                rx.text(
                                    "Accueil",
                                    on_click=rx.redirect("/"),
                                    cursor="pointer",
                                ),
                                width="100%",
                            ),
                            rx.spacer(),
                            rx.hstack(
                                popups.login_popup(True, "sidebar"),
                                width="30%",
                                heigth="5%",
                            ),
                            direction="column",
                            height="100%",
                            background_color="white",
                            width="20em",
                            padding="2em",
                        )
                    )
                ),
                open=MultiStepFormState.show_drawer_left,
                direction="left",
                modal=False,
            )
        )
    )


def header():
    """
    The header contains the company's icon, the menu button, the "prendre contact" button
    Returns:
        The landing page with the background image and its buttons
    """
    return rx.hstack(
        rx.image(
            src="/RDE_consulting_icon.jpg",
            width="13%",
            on_click=rx.redirect("/"),
            cursor="pointer"
        ),
        menu_drawer(),
        rx.spacer(),
        rx.stack(
            popups.contact_popup(),
            padding="1em",
        ),
        #height="1%",
        #position="fixed",
        style={"background": "white", "width": "100%", "height": "1%"},
    )


def sidebar():
    """
    The sidebar will only appear in the pages related to the simulator like date-department, sector or choice-pdf.
    It will list each step of it and if clicked, will take the user to the corresponding page.

    Returns:
        The sidebar with each pages as links
    """
    current_link = State.current_path
    return rx.vstack(
        rx.cond(
            ((current_link == "/date-department/") | (current_link == "/sector/") |
             (current_link == "/typology/") | (current_link == "/choice-pdf/") |
             (current_link == "/beneficiary/") | (current_link == "/simulator/")),
            rx.vstack(
                text_styles.title_text(f"Votre parcours"),
                rx.cond(
                    (State.current_path != "/date-department/"),
                    rx.link("Date et département", href="/date-department"),
                    rx.link("Date et département", href="/date-department", color="#466c82", weight="bold"),
                ),
                rx.cond(
                    (State.current_path != "/sector/"),
                    rx.link("Secteur", href="/sector"),
                    rx.link("Secteur", href="/sector", color="#466c82", weight="bold"),
                ),
                rx.cond(
                    (State.current_path != "/typology/"),
                    rx.link("Typologie", href="/typology"),
                    rx.link("Typologie", href="/typology", color="#466c82", weight="bold"),
                ),
                rx.cond(
                    (State.current_path != "/choice-pdf/"),
                    rx.link("Liste des fiches", href="/choice-pdf"),
                    rx.link("Liste des fiches", href="/choice-pdf", color="#466c82", weight="bold"),
                ),
                rx.cond(
                    (State.current_path != "/beneficiary/"),
                    rx.link("Bénéficiaire", href="/beneficiary"),
                    rx.link("Bénéficiaire", href="/beneficiary", color="#466c82", weight="bold"),
                ),
                rx.cond(
                    (State.current_path != "/simulator/"),
                    rx.link("Simulateur", href="/simulator"),
                    rx.link("Simulateur", href="/simulator", color="#466c82", weight="bold"),
                ),
            ),
        ),
        #position="fixed",
        height="86vh",
        style={"background": "white", "minWidth": "15%", "padding": "2rem 1rem"}
    )

# @rx.page(route="/google-callback")
# def google_callback():
#     return rx.script("""
#         const hash = window.location.hash.substring(1);
#         const params = new URLSearchParams(hash);
#         const accessToken = params.get("access_token");
#         if (accessToken) {
#             fetch("https://www.googleapis.com/oauth2/v3/userinfo", {
#                 headers: {
#                     Authorization: `Bearer ${accessToken}`
#                 }
#             })
#             .then(res => res.json())
#             .then(data => {
#                 fetch("/_state/api/auth/google_login", {
#                     method: "POST",
#                     headers: {"Content-Type": "application/json"},
#                     body: JSON.stringify({email: data.email, name: data.name})
#                 }).then(() => {
#                     window.location.href = "/dashboard/";
#                 });
#             });
#         }
#     """)


def return_button() -> rx.Component:
    return rx.hstack(
        rx.button(
            rx.flex(
                rx.icon("chevron-left", size=26),
                rx.text(
                    "Retour",
                    size="2",
                    weight="medium",
                ),
                direction="row",
                spacing="1",
                align="center",
            ),
            variant="ghost",
            type="button",
            _hover={"background": "none", "box_shadow": "none", "color": "inherit"},
            on_click=MultiStepFormState.go_to_previous,
        ),
        width="100%",
    )

def multi_step_layout(content, progress):
    """
    This function acts like a template for each page of our simulator. It will display the content beneath the header and
    the progress bar, and on the right of the sidebar

    Parameters :
        content : the content to be displayed. For example input for the date and the department
        progress: the progress of the page in the simulator
    Returns:
        Returning a component is the same as displaying it. So here it will display a formatted page for the simulator
        with it intended content (choices between yes and no for example)
    """
    current_page = State.current_path
    MultiStepFormState.progress_percent = progress
    return rx.vstack(
        header(),
        rx.hstack(
            sidebar(),
            rx.center(
                rx.form(
                    rx.vstack(
                        return_button(),
                        show_completion_steps(),
                        content,
                        rx.box(
                            rx.cond(
                                (current_page != "/options/") & (current_page != "/sector/") &
                                (current_page != "/typology/") & (current_page != "/choice-pdf/") & (current_page != "/mpr-list/"),
                                rx.center(
                                    rx.cond(
                                        (current_page == "/simulator/"),
                                        popups.execute_simulation(False),
                                        rx.button(
                                            rx.flex(
                                                rx.text(
                                                    "Continuer",
                                                    size="5",
                                                    weight="medium",
                                                ),
                                                rx.icon("chevron-right", size=28),
                                                direction="row",
                                                spacing="1",
                                                align="center",
                                            ),
                                            type="submit",
                                            size="2",
                                            style={
                                                "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
                                            },
                                            _hover={
                                                "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
                                                "transform": "scale(1.05)",
                                                "transition": "all 0.2s ease-in-out"
                                            },
                                            transition="all 0.2s ease-in-out",
                                            padding="2em",
                                        ),
                                    ),
                                    width="100%",
                                )
                            ),
                        ),

                        width="100%",
                        height="80%",
                        align_items="center",
                    ),
                    on_submit=MultiStepFormState.save_and_go_to_next,
                    reset_on_submit=False,
                    width="100%",
                    height="100%",
                    padding="1rem",
                    border_radius="xl",
                    box_shadow="md",
                    #bg="#f1f6fe"
                ),
                height="100%",
                width="100%",
                align_items="center",
                justify_content="center",
                bg="#fcfcfd",
                #bg="#f1f6fe",
                style={
                    "background_image": "url('/assets/monochrome-urban.jpg')",
                    "background_size": "cover",
                    "background_position": "center",
                    "background_repeat": "no-repeat",
                }
            ),
            spacing="0",
            width="100%",
            height="80%",
            align="start",
            bg="#fcfcfd", # gris fond
        ),
        chatbot_popup.floating_chat_button(),
        #bg="#f1f6fe",
        spacing="0",
        width="100%",
    )

def multi_step_layout_no_stepper(content, progress):
    """
        This function acts like multi_step_layout but without displaying the progressbar

        Parameters :
            content : the content to be displayed. For example input for the date and the department
            progress: the progress of the page in the simulator. Still needed here eventhough we don't display it
        Returns:
            The same as multi_step_layout but without displaying the progressbar
        """
    current_page = State.current_path
    MultiStepFormState.progress_percent = progress
    return rx.vstack(
        header(),
        rx.hstack(
            sidebar(),
            rx.center(
                rx.form(
                    rx.vstack(
                        return_button(),
                        content,
                        width="100%",
                        height="80%",
                        align_items="center",
                    ),
                    on_submit=MultiStepFormState.save_and_go_to_next,
                    reset_on_submit=False,
                    width="100%",
                    height="100%",
                    padding="1rem",
                    border_radius="xl",
                    box_shadow="md",
                    #bg="#f1f6fe"
                ),
                height="100%",
                width="100%",
                align_items="center",
                justify_content="center",
                bg="#fcfcfd",
                #bg="#f1f6fe",
                style={
                    "background_image": "url('/assets/monochrome-urban.jpg')",
                    "background_size": "cover",
                    "background_position": "center",
                    "background_repeat": "no-repeat",
                }
            ),
            spacing="0",
            width="100%",
            height="80%",
            align="start",
            bg="#fcfcfd",
        ),
        chatbot_popup.floating_chat_button(),
        #bg="#f1f6fe",
        spacing="0",
        width="100%",
    )

@rx.page(route="/", title="RDE Simulateur")
def page_landing():
    """
    The landing page is the first page in the website. When the user click on the link, it will be redirected here.
    It can be seen as the cover page.

    Returns:
        The landing page with the background image and its buttons
    """
    content = rx.vstack(
        rx.box(
            style={
                "backgroundImage": "url('/thumbnail_image.jpg')",
                "backgroundSize": "cover",
                "backgroundPosition": "center",
                "width": "100%",
                "height": "100vh",
                "position": "absolute",
                "top": "0",
                "left": "0",
                #"opacity": "0.2",
                "zIndex": "-1",
            }
        ),
        rx.hstack(
            rx.image(
                src="/thumbnail_RDE_consulting_icon-removebg.jpg",
                width="20%",
                on_click=rx.redirect("/"),
                cursor="pointer",
            ),
            rx.spacer(),
            rx.hstack(
                popups.login_popup(True, "index"),
                padding="2em"
            ),
            width="100%",
        ),
        rx.vstack(
            rx.heading(
                "Calculez votre\nprime CEE",
                size="9",
                color="white",
                white_space="pre-line",
                #style={"color": "white"},
            ),
            rx.text(
                """Faites facilement des économies sur vos travaux 
                et rénovations énergétiques !""",
                size="6",
                color="white",
                weight="bold",
                margin_top="5em",
                style={"white_space": "pre-line"},
            ),
            padding="2em",
        ),
        rx.spacer(min_height="4em"),
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.text(
                        "Je calcule mes aides",
                        weight="bold",
                    ),
                    rx.icon("arrow-big-right"),
                    align="center"
                ),
                on_click=rx.redirect("/options"),
                size="4",
                style={
                    "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
                },
            ),
            padding="2em",
            spacing="6",
            transition="all 0.2s ease-in-out",
            width="100%",
        ),
        align_items="start",
        height="100vh",
        width="100%",
    )
    return content


@rx.page(route="/options", title="RDE Simulateur")
def page_options():
    """
    First step of our simulator. We let the user choose between options. For now, there is only one of it.

    Returns:
        A Reflex component by calling multi_step_layout_no_stepper. We give it the content of this page and it will display
        with the same elements as the other pages from the simulator (with the header and sidebar but without the stepper).
    """
    MultiStepFormState.set_page_progress(1)
    content = rx.vstack(
        text_styles.title_text("Je veux :"),
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.icon(tag="calculator", size=40, color="#368278"),
                    rx.text(
                        "Calculer mes aides et primes",
                        font_weight="bold",
                        text_align="center",
                        font_size="1.1em",
                        wrap="wrap",
                    ),
                    padding="0.5rem",
                    align_items="center",
                ),
                align_items="center",
                cursor="pointer",
                on_click=MultiStepFormState.init_simulator,
                width="30%",
                height="100%",
                items_align="center",
                border="2px solid",
                border_radius="16px",
                border_color="#ccc",
                bg="white",
                style={
                    "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
                },
                _hover={
                    "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
                    "transform": "scale(1.05)",
                    "transition": "all 0.2s ease-in-out"
                },
            ),
            justify="center",
            wrap="wrap",
            width="60%",
            height="30%",
        ),
        # rx.vstack(
        #     # rx.vstack(
        #     #     rx.text("Je préfère appeler un conseiller",
        #     #             font_weight="bold", ),
        #     #     rx.text("Du lundi au vendredi - 9h à 19h"),
        #     # ),
        #     width="30%",
        #     height="20%",
        #     justify="center",
        #     padding="2em",
        #     bg="white",
        #     style={
        #         "box_shadow": "0 8px 20px rgba(0, 0, 0, 0.25)",
        #     },
        # ),
        width="100%",
        height="70vh",
        align_items="center",
        spacing="9",
    )
    return multi_step_layout_no_stepper(content, 0)


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="teal"
    )
)

app.add_page(page_landing, title="RDE Simulateur")
app.add_page(page_options)
app.add_page(date_department.page_date_departement)
app.add_page(sector.page_sector)
app.add_page(typology.page_typology)
app.add_page(beneficiary_page.page_beneficiary)
app.add_page(choice_pdf.page_pdf)
app.add_page(simulator.page_simulator)
app.add_page(identify.page_identify)
# app.add_page(results_history.page_results_history)
app.add_page(mpr_list_page.page_mpr_list)
app.add_page(result_page.result_page)
app.add_page(result_details.details_page)
app.add_page(profile.profile_page)
app.add_page(admin_page.page_admin_results_history)
app.add_page(mpr_page.page_admin_mpr_link)

