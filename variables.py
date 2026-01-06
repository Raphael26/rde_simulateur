class Variables():
    departements_france = {
        "Ain (01)": "ain",
        "Aisne (02)": "aisne",
        "Allier (03)": "allier",
        "Alpes-de-Haute-Provence (04)": "alpes-de-haute-provence",
        "Hautes-Alpes (05)": "hautes-alpes",
        "Alpes-Maritimes (06)": "alpes-maritimes",
        "Ardèche (07)": "ardeche",
        "Ardennes (08)": "ardennes",
        "Ariège (09)": "ariege",
        "Aube (10)": "aube",
        "Aude (11)": "aude",
        "Aveyron (12)": "aveyron",
        "Bouches-du-Rhône (13)": "bouches-du-rhone",
        "Calvados (14)": "calvados",
        "Cantal (15)": "cantal",
        "Charente (16)": "charente",
        "Charente-Maritime (17)": "charente-maritime",
        "Cher (18)": "cher",
        "Corrèze (19)": "correze",
        "Corse-du-Sud (2A)": "corse-du-sud",
        "Haute-Corse (2B)": "haute-corse",
        "Côte-d'Or (21)": "cote-d-or",
        "Côtes-d'Armor (22)": "cotes-d-armor",
        "Creuse (23)": "creuse",
        "Dordogne (24)": "dordogne",
        "Doubs (25)": "doubs",
        "Drôme (26)": "drome",
        "Eure (27)": "eure",
        "Eure-et-Loir (28)": "eure-et-loir",
        "Finistère (29)": "finistere",
        "Gard (30)": "gard",
        "Haute-Garonne (31)": "haute-garonne",
        "Gers (32)": "gers",
        "Gironde (33)": "gironde",
        "Hérault (34)": "herault",
        "Ille-et-Vilaine (35)": "ille-et-vilaine",
        "Indre (36)": "indre",
        "Indre-et-Loire (37)": "indre-et-loire",
        "Isère (38)": "isere",
        "Jura (39)": "jura",
        "Landes (40)": "landes",
        "Loir-et-Cher (41)": "loir-et-cher",
        "Loire (42)": "loire",
        "Haute-Loire (43)": "haute-loire",
        "Loire-Atlantique (44)": "loire-atlantique",
        "Loiret (45)": "loiret",
        "Lot (46)": "lot",
        "Lot-et-Garonne (47)": "lot-et-garonne",
        "Lozère (48)": "lozere",
        "Maine-et-Loire (49)": "maine-et-loire",
        "Manche (50)": "manche",
        "Marne (51)": "marne",
        "Haute-Marne (52)": "haute-marne",
        "Mayenne (53)": "mayenne",
        "Meurthe-et-Moselle (54)": "meurthe-et-moselle",
        "Meuse (55)": "meuse",
        "Morbihan (56)": "morbihan",
        "Moselle (57)": "moselle",
        "Nièvre (58)": "nievre",
        "Nord (59)": "nord",
        "Oise (60)": "oise",
        "Orne (61)": "orne",
        "Pas-de-Calais (62)": "pas-de-calais",
        "Puy-de-Dôme (63)": "puy-de-dome",
        "Pyrénées-Atlantiques (64)": "pyrenees-atlantiques",
        "Hautes-Pyrénées (65)": "hautes-pyrenees",
        "Pyrénées-Orientales (66)": "pyrenees-orientales",
        "Bas-Rhin (67)": "bas-rhin",
        "Haut-Rhin (68)": "haut-rhin",
        "Rhône (69)": "rhone",
        "Haute-Saône (70)": "haute-saone",
        "Saône-et-Loire (71)": "saone-et-loire",
        "Sarthe (72)": "sarthe",
        "Savoie (73)": "savoie",
        "Haute-Savoie (74)": "haute-savoie",
        "Paris (75)": "paris",
        "Seine-Maritime (76)": "seine-maritime",
        "Seine-et-Marne (77)": "seine-et-marne",
        "Yvelines (78)": "yvelines",
        "Deux-Sèvres (79)": "deux-sevres",
        "Somme (80)": "somme",
        "Tarn (81)": "tarn",
        "Tarn-et-Garonne (82)": "tarn-et-garonne",
        "Var (83)": "var",
        "Vaucluse (84)": "vaucluse",
        "Vendée (85)": "vendee",
        "Vienne (86)": "vienne",
        "Haute-Vienne (87)": "haute-vienne",
        "Vosges (88)": "vosges",
        "Yonne (89)": "yonne",
        "Territoire de Belfort (90)": "territoire-de-belfort",
        "Essonne (91)": "essonne",
        "Hauts-de-Seine (92)": "hauts-de-seine",
        "Seine-Saint-Denis (93)": "seine-saint-denis",
        "Val-de-Marne (94)": "val-de-marne",
        "Val-d'Oise (95)": "val-d-oise",
        "Guadeloupe (971)": "guadeloupe",
        "Martinique (972)": "martinique",
        "Guyane (973)": "guyane",
        "La Réunion (974)": "la-reunion",
        "Mayotte (976)": "mayotte"
    }

    sector_dict_list = [
        {"label": "Industrie", "icon": "factory", "value": "Industrie", "abbr": "IND"},
        {"label": "Résidentiel", "icon": "house", "value": "Résidentiel", "abbr": "BAR"},
        {"label": "Tertiaire", "icon": "building-2", "value": "Tertiaire", "abbr": "BAT"},
        {"label": "Réseaux", "icon": "network", "value": "Réseaux", "abbr": "RES"},
        {"label": "Agriculture", "icon": "carrot", "value": "Agriculture", "abbr": "AGRI"},
        {"label": "Transport", "icon": "bus", "value": "Transport", "abbr": "TRA"},
    ]

    sector_with_typology_dict = \
        {
            'Industrie': {'Utilité': 'UT', 'Bâtiment': 'BA'},
            'Résidentiel': {'Enveloppe': 'EN', 'Thermique': 'TH', 'Équipement': 'EQ', 'Service': 'SE'},
            'Tertiaire': {'Enveloppe': 'EN', 'Thermique': 'TH', 'Équipement': 'EQ', 'Service': 'SE'},
            'Réseaux': {'Eclairage': 'EC', 'Chaleur': 'CH'},
            'Agriculture': {'Utilité': 'UT', 'Thermique': 'TH', 'Équipement': 'EQ', 'Service': 'SE'},
            'Transport': {'Équipement': 'EQ', 'Service': 'SE'},
        }

    typology_dict_list = {
        "Utilité": {"icon": "plug", "value": "Utilité", "abbr": "UT"},
        "Batiment": {"icon": "building", "value": "Bâtiment", "abbr": "BA"},
        "Enveloppe": {"icon": "building", "value": "Enveloppe", "abbr": "EN"},
        "Thermique": {"icon": "flame", "value": "Thermique", "abbr": "MPR"},
        "Équipement": {"icon": "cpu", "value": "Équipement", "abbr": "EQ"},
        "Service": {"icon": "briefcase", "value": "Service", "abbr": "SE"},
        "Eclairage": {"icon": "lightbulb", "value": "Eclairage", "abbr": "EC"},
        "Chaleur": {"icon": "thermometer", "value": "Chaleur", "abbr": "CH"},
    }

    sector_abreviation_mapping = \
        {
            'Industrie': 'IND','Résidentiel': 'BAR','Tertiaire': 'BAT','Réseaux': 'RES','Agriculture': 'AGRI','Transport': 'TRA'
        }

    typology_abreviation_mapping = \
        {
            'Utilité': 'UT', 'Bâtiment': 'BA', 'Enveloppe': 'EN', 'Thermique': 'MPR', 'Équipement': 'EQ', 'Service': 'SE', 'Chaleur': 'CH'
        }

    input_choices = \
        {
            'usage': {'procédé': 'procédés', 'chauffage': 'chauffages'},
            'mode': {'3x8h_sans_we': '3x8h_sans_we',
                     '2x8h': '2x8h', '1x8h': '1x8h', '3x8h_avec_we': '3x8h_avec_we'},
            'zone_climatique': {'H2': 'H2', 'H3': 'H3', 'H1': 'H1'},
        }

    mapping_types = \
        {
        'usage': 'usage',
        'mode': 'mode',
        'zone': 'zone_climatique',
        'puissance_kW': None
        }

    icon_map = {
        'Utilité': "material/build",
        'Bâtiment': "material/domain",
        'Enveloppe': "material/roofing",
        'Thermique': "material/thermostat",
        'Équipement': "material/engineering",
        'Service': "material/support_agent",
        'Eclairage': "material/lightbulb",
        'Chaleur': "material/whatshot",
    }

    def get_abreviation(self, sector: str, typology: str) -> str:
        sector_abbr = self.sector_abreviation_mapping.get(sector)
        typology_dict = self.sector_with_typology_dict.get(sector, {})
        typology_abbr = typology_dict.get(typology)

        if sector_abbr and typology_abbr:
            return f"{sector_abbr}-{typology_abbr}-"
        else:
            return "..."