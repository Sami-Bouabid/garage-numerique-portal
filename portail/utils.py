import json
import os 
from .models import Carte, Page_Ressources
from admin.functions import est_installe

# transformation json en liste
def load_json(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Fichier non trouvé : {filename}")
    with open(filename, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"Erreur de chargement du JSON : {error}")

# transformation des listes en objets "carte"
def load_carte(filename):
    data = load_json(filename)

    ressources = []
    for element in data:
        packet = element['packet_name']
        installe = est_installe(packet) if packet else False

        url = f"/admin/install/{packet}" 

        ressources.append(Carte(
            element['title'],
            element['short_desc'],
            element['icon'],
            element['subjects'],
        ))

    return ressources

def load_page(filename):
    data = load_json(filename)

    ressources = []
    for element in data:
        packet = element.get('packet_name')
        installe = est_installe(packet) if packet else False

        ressources.append(Page_Ressources(
            element['title'],
            element['url'],
            packet,
            element['long_desc'],
            element['icon'],
            element['featured_image'],
            element['illustrations'],
            element['subjects'],
            element['content_type'],
            element['comments'],
        ))

    return ressources