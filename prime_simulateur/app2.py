import json
import streamlit as st
import function_loader


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False
    

all = [
    #'AGRI-EQ-101', 'AGRI-EQ-102', 'AGRI-EQ-104', 'AGRI-EQ-105', 'AGRI-EQ-106', 'AGRI-EQ-107',
    #'AGRI-EQ-108', 'AGRI-EQ-109', 'AGRI-EQ-110', 'AGRI-EQ-111', 'AGRI-EQ-112',
    #'AGRI-SE-101'
    #'AGRI-TH-101', 'AGRI-TH-102', 'AGRI-TH-103', 'AGRI-TH-105',
    #'AGRI-TH-109', 'AGRI-TH-110', 'AGRI-TH-113', 'AGRI-TH-117', 'AGRI-TH-118', 'AGRI-TH-119'
    #'AGRI-UT-101', 'AGRI-UT-102', 'AGRI-UT-103', 'AGRI-UT-104'
    #'BAR-EN-101', 'BAR-EN-102', 'BAR-EN-103', 'BAR-EN-104', 'BAR-EN-105', 'BAR-EN-106', 'BAR-EN-107', 'BAR-EN-108', 'BAR-EN-109', 'BAR-EN-110'
    #'BAR-EQ-115',
    #'BAR-SE-104', 'BAR-SE-105', 'BAR-SE-106', 'BAR-SE-107', 'BAR-SE-108', 'BAR-SE-109',
    #'BAR-TH-101', 'BAR-TH-104', 'BAR-TH-110', 'BAR-TH-111', 'BAR-TH-112', 'BAR-TH-113', 'BAR-TH-116', 'BAR-TH-117',
    #'BAR-TH-122', 'BAR-TH-123', 'BAR-TH-124', 'BAR-TH-125', 'BAR-TH-127',

    'BAR-EQ-115.pdf', #'BAR-TH-129', 'BAR-TH-130', 'BAR-TH-135', 'BAR-TH-137', 'BAR-TH-139', 'BAR-TH-141', 'BAR-TH-143', 'BAR-TH-145',
    #'BAR-TH-148', 'BAR-TH-150', 'BAR-TH-155', 'BAR-TH-158', 'BAR-TH-159', 'BAR-TH-160', 'BAR-TH-161', 'BAR-TH-162',
    #'BAR-TH-163', 'BAR-TH-165', 'BAR-TH-166', 'BAR-TH-167',
    #'BAR-TH-168', 'BAR-TH-169', 'BAR-TH-170', 'BAR-TH-171', 'BAR-TH-172', 'BAR-TH-173', 'BAR-TH-174', 'BAR-TH-175', 'BAR-TH-176', 'BAR-TH-177'

    #'BAT-EN-101', 'BAT-EN-102', 'BAT-EN-103', 'BAT-EN-104', 'BAT-EN-106', 'BAT-EN-107', 'BAT-EN-108', 'BAT-EN-109', 'BAT-EN-110',
    #'BAT-EN-111', 'BAT-EN-112', 'BAT-EN-113',

    #'BAT-EQ-117', 'BAT-EQ-123', 'BAT-EQ-124', 'BAT-EQ-125', 'BAT-EQ-127', 'BAT-EQ-129', 'BAT-EQ-130', 'BAT-EQ-131', 'BAT-EQ-133', 'BAT-EQ-134',
    #'BAT-EQ-135',

    #'BAT-SE-103', 'BAT-SE-104', 'BAT-SE-105'
    
    #'BAT-TH-103', 'BAT-TH-104', 'BAT-TH-105', 'BAT-TH-108', 'BAT-TH-109', 'BAT-TH-110', 'BAT-TH-111', 'BAT-TH-112',
    #'BAT-TH-113', 'BAT-TH-115', 'BAT-TH-116', 'BAT-TH-121', 'BAT-TH-122', 'BAT-TH-125', 'BAT-TH-126', 'BAT-TH-127',
    #'BAT-TH-134', 'BAT-TH-135', 'BAT-TH-139', 'BAT-TH-140', 'BAT-TH-141', 'BAT-TH-142', 'BAT-TH-143', 'BAT-TH-145',
    #'BAT-TH-146', 'BAT-TH-153', 'BAT-TH-154', 'BAT-TH-155', 'BAT-TH-156', 'BAT-TH-157', 'BAT-TH-158', 'BAT-TH-159',
    #'BAT-TH-161'
]


def new_fiche():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


fiche_selected = st.selectbox(label="Fiche", options=all, on_change=new_fiche) #, key="fiche_selected")
print(fiche_selected)


#@st.cache_data
def load_function_parameters(fiche_selected):
    #with open(f"/data/fiches/{fiche_selected}/function_param_values_labeled.json", "r") as file:
        #function_params = json.load(file)
    function_params = {'Zone climatique': ['H3', 'H1', 'H2'], 'Type de logement 4': ['appartement', 'maison']}
    
    #with open(f"/data/fiches/{fiche_selected}/variables_mapping.json", "r") as file:
        #variables_mapping = json.load(file)
    variables_mapping = {'Zone climatique': {'H3': 'H3', 'H1': 'H1', 'H2': 'H2'}, 'Type de logement 4': {'Appartement': 'appartement', 'Maison': 'maison'}}
    
    #with open(f"/data/fiches/{fiche_selected}/variables_matching.json", "r") as file:
        #variables_matching = json.load(file)
    variables_matching = {'Zone climatique': 'zone_climatique', 'Type de logement 4': 'type_logement'}
    
    #with open(f"/data/fiches/{fiche_selected}/string_function.txt", encoding="utf-8") as f:
        # Load the string extracted from the image using the LLM
        #string_function = f.read()
    string_function = """def calculer_montant_certificats_en_kwh_cumac(
    zone_climatique: str,
    option_suivi_du_confort: bool,
    surface_habitable_en_m2: float,
    type_logement: str
) -> float:
    base_maison = {'H1': 4400, 'H2': 3700, 'H3': 2700}
    base_appartement = {'H1': 2600, 'H2': 2200, 'H3': 1700}
    fixe_par_type = {'maison': 650, 'appartement': 410}
    confort_coef = 1 if option_suivi_du_confort else 0.8

    if type_logement == 'maison':
        base = base_maison[zone_climatique]
        if surface_habitable_en_m2 < 35:
            facteur_correctif = 0.3
        elif surface_habitable_en_m2 < 60:
            facteur_correctif = 0.5
        elif surface_habitable_en_m2 < 70:
            facteur_correctif = 0.6
        elif surface_habitable_en_m2 < 90:
            facteur_correctif = 0.7
        elif surface_habitable_en_m2 < 110:
            facteur_correctif = 1.0
        elif surface_habitable_en_m2 <= 130:
            facteur_correctif = 1.1
        else:
            facteur_correctif = 1.6
    else:
        base = base_appartement[zone_climatique]
        if surface_habitable_en_m2 < 35:
            facteur_correctif = 0.5
        elif surface_habitable_en_m2 < 60:
            facteur_correctif = 0.7
        elif surface_habitable_en_m2 < 70:
            facteur_correctif = 1.0
        elif surface_habitable_en_m2 < 90:
            facteur_correctif = 1.2
        elif surface_habitable_en_m2 < 110:
            facteur_correctif = 1.5
        elif surface_habitable_en_m2 <= 130:
            facteur_correctif = 1.9
        else:
            facteur_correctif = 2.5

    return base * confort_coef * facteur_correctif + fixe_par_type[type_logement]"""

    return string_function, function_params, variables_mapping, variables_matching


string_function, function_params, variables_mapping, variables_matching = load_function_parameters(
    fiche_selected
)

# Convert into a real function
func = function_loader.FunctionLoader(string_function)

# Create user input for the function
for key, value in variables_mapping.items():
    list_options = list(value.keys())

    # Special case for zone climatique
    if 'H1' in list_options:
        list_options.sort()
    # Special case for durée garantie
    elif ('9' in list_options) and ('10' in list_options):
        list_options = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    st.selectbox(
        label=key, options=list_options, key=key,
    )
    
# Numerical inputs
KEYWORDS = (
    'surface', 'puissance', 'resistance', 'nombre', 'percent',
    'pourcentage', 'superficie', 'longueur', 'indice', 'valeur',
    'm2', 'besoin', 'efficacite', 'temperature', 'chaleur', 'seer',
    'etas', 'usage_pac', 'volume', 'scop',
)
for k, v in func.get_parameters().items():
    # skip the one specific key
    if 'Puissance frigorifique' not in k:

        # fast substring test:
        if any(keyword in k for keyword in KEYWORDS):
            label = k.replace('_', ' ').capitalize().strip()
            st.number_input(label=label, key=k)

# Boolean inputs
for k,v in func.get_parameters().items():
    if v['annotation'] != None:
        if 'bool' in v['annotation']:
            label = k.replace("_", " ").capitalize().strip()
            radio_bool = st.radio(label=label, options=["Oui", "Non"], horizontal=True)

            # Properly convert to real boolean values
            if radio_bool == "Oui":
                st.session_state[k] = True
            else:
                st.session_state[k] = False


# Compute calculation
function_call_dict = {}
for k,v in st.session_state.items():
    if k in variables_mapping:

        function_call_dict[variables_matching[k]] = variables_mapping[k][str(v)]
        
        # Special case for durée de garantie as the function parameter need an integer
        if str(v).isdigit():
            function_call_dict[variables_matching[k]] = int(variables_mapping[k][str(v)])
        elif is_float(v):
            function_call_dict[variables_matching[k]] = float(variables_mapping[k][str(v)])
    else:
        function_call_dict[k] = v

print("function_call_dict:", function_call_dict)

try:
    result = func.call_with_dict(function_call_dict)
    result = round(result, 2)

    st.metric(label="RESULT", value=result, border=True)
except Exception as e:
    st.error(repr(e))


print(100*"=")