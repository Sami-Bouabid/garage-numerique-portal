from flask import Blueprint, render_template, abort
import os
import json
import re # Importe le module 're' pour les expressions régulières (utilisé pour la "slugification")

# Importe la classe Page_Ressources depuis le même package.
# Assurez-vous que le chemin d'importation est correct selon votre structure de projet.
from .models import Page_Ressources 

# Crée le Blueprint 'portail'.
# Il regroupe les routes, les templates et les fichiers statiques de cette section de l'application.
portail = Blueprint('portail', __name__, template_folder='templates', static_folder='static')

# --- Fonction utilitaire pour "slugifier" une chaîne de caractères ---
def slugify(text):
    """
    Convertit une chaîne de caractères en un format "slug" compatible avec les URL.
    Un slug est une version du texte en minuscules, où les espaces et caractères spéciaux
    sont remplacés par des tirets, rendant le texte sûr pour les URL.
    Ex: "Mon Super Titre!" -> "mon-super-titre"
    """
    if not text:
        return ""
    text = str(text).lower()
    # Remplace les caractères non alphanumériques (sauf espaces et tirets) par rien.
    text = re.sub(r'[^\w\s-]', '', text) 
    # Remplace les espaces, tirets multiples ou combinaisons par un seul tiret.
    text = re.sub(r'[\s_-]+', '-', text) 
    # Supprime les tirets en début et fin de chaîne.
    text = text.strip('-') 
    return text

# --- Fonction pour charger les données des ressources ---
def load_resources_data():
    """
    Charge toutes les ressources depuis le fichier 'ressources.json'.
    Convertit chaque ressource en un objet Page_Ressources et les stocke dans
    un dictionnaire où la clé est le "slug" du titre de la ressource.
    Cela permet une récupération facile des ressources par leur URL conviviale.
    """
    # Construit le chemin absolu vers 'ressources.json' en fonction de l'emplacement de ce fichier.
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ressources.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            resources_dict = {}
            # Gère le cas où 'ressources.json' est une liste d'objets.
            if isinstance(data, list):
                for res in data:
                    res_title = res.get('title')
                    if res_title: # S'assure que la ressource a un titre pour pouvoir créer un slug.
                        resource_slug = slugify(res_title)
                        # Crée un objet Page_Ressources et l'ajoute au dictionnaire.
                        # Le 'packet_name' est conservé tel quel (peut être None ou vide si non présent).
                        resources_dict[resource_slug] = Page_Ressources(
                            title=res.get('title'),
                            url=res.get('url'),
                            packet_name=res.get('packet_name'), 
                            long_desc=res.get('long_desc'),
                            icon=res.get('icon'),
                            featured_image=res.get('featured_image'),
                            illustrations=res.get('illustrations', []),
                            subjects=res.get('subjects', []),
                            content_type=res.get('content_type'),
                            comments=res.get('comments')
                        )
            # Gère le cas où 'ressources.json' est un dictionnaire (où les clés sont déjà des identifiants).
            elif isinstance(data, dict):
                # Dans ce cas, la clé du dictionnaire JSON n'est pas directement utilisée comme slug.
                for key, res_data in data.items(): 
                    res_title = res_data.get('title')
                    if res_title: # S'assure que la ressource a un titre.
                        resource_slug = slugify(res_title)
                        resources_dict[resource_slug] = Page_Ressources(
                            title=res_data.get('title'),
                            url=res_data.get('url'),
                            packet_name=res_data.get('packet_name'), 
                            long_desc=res_data.get('long_desc'),
                            icon=res_data.get('icon'),
                            featured_image=res_data.get('featured_image'),
                            illustrations=res_data.get('illustrations', []),
                            subjects=res_data.get('subjects', []),
                            content_type=res_data.get('content_type'),
                            comments=res_data.get('comments')
                        )
            
            return resources_dict

    except FileNotFoundError:
        # Affiche une erreur si le fichier 'ressources.json' n'est pas trouvé.
        print(f"ERREUR: Le fichier ressources.json n'a PAS été trouvé à {json_path}")
        return {}
    except json.JSONDecodeError as e:
        # Affiche une erreur si le fichier JSON est invalide ou vide.
        print(f"ERREUR: Le fichier {json_path} n'est pas un JSON valide ou est vide. Détail: {e}")
        return {}
    except Exception as e:
        # Capture toute autre erreur inattendue lors du chargement.
        print(f"ERREUR INATTENDUE: {e}")
        return {}

# --- Route pour la page d'accueil (index.html) ---
@portail.route("/")
def index():
    """
    Affiche la page d'accueil, listant toutes les ressources disponibles.
    Toutes les ressources sont chargées et passées au template 'index.html'.
    """
    all_resources_objects_dict = load_resources_data()
    # Passe les valeurs du dictionnaire (les objets Page_Ressources) au template.
    return render_template("index.html", cartes=all_resources_objects_dict.values())

# --- Route pour la page de détail d'une ressource spécifique ---
@portail.route('/resource/<string:resource_slug>')
def resource_detail(resource_slug):
    """
    Affiche la page de détail pour une ressource spécifique, identifiée par son 'slug' dans l'URL.
    Si le slug ne correspond à aucune ressource, renvoie une erreur 404 (Page non trouvée).
    """
    all_resources_objects_dict = load_resources_data()
    
    # Récupère l'objet ressource correspondant au slug de l'URL.
    resource_obj = all_resources_objects_dict.get(resource_slug)

    if resource_obj:
        # Rend le template de détail avec l'objet ressource trouvé.
        return render_template('template.html', resource=resource_obj)
    else:
        # Si aucune ressource ne correspond au slug, déclenche une erreur 404.
        abort(404)

# --- Gestionnaire d'erreurs 404 (Page non trouvée) ---
@portail.errorhandler(404)
def page_not_found(e):
    """
    Fonction personnalisée pour gérer les erreurs 404 (Page non trouvée).
    Elle affiche un template '404.html' et renvoie le statut HTTP 404.
    """
    return render_template('404.html'), 404