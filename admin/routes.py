from flask import Blueprint, request, jsonify
from admin.functions import install_paquet, desinstaller_paquet, mise_a_jour, lancer_paquet, est_installe # Importez est_installe
import json
import os

# Définition du Blueprint 'admin'
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/api/install', methods=['POST'])
def api_install():
    data = request.get_json()
    packet_name = data.get('packet_name')
    print(f"DEBUG: Requête /api/install reçue pour le paquet: '{packet_name}'")

    if not packet_name:
        return jsonify({"success": False, "message": "Nom de paquet système manquant."}), 400

    resultat = install_paquet(packet_name)
    return jsonify({"success": resultat is True, "message": f"'{packet_name}' {'installé' if resultat is True else resultat}."}), (200 if resultat is True else 500)

@admin.route('/api/uninstall', methods=['POST'])
def api_uninstall():
    data = request.get_json()
    packet_name = data.get('packet_name')
    print(f"DEBUG: Requête /api/uninstall reçue pour le paquet: '{packet_name}'")

    if not packet_name:
        return jsonify({"success": False, "message": "Nom de paquet système manquant."}), 400

    resultat = desinstaller_paquet(packet_name)
    # Adaptez la logique ici si desinstaller_paquet retourne un tuple (False, message)
    if isinstance(resultat, tuple):
        success = resultat[0]
        message = resultat[1]
    else:
        success = resultat
        message = f"'{packet_name}' {'désinstallé' if resultat is True else 'échec de la désinstallation'}."
        
    return jsonify({"success": success, "message": message}), (200 if success is True else 500)

@admin.route('/api/update', methods=['POST'])
def api_update():
    print("DEBUG: Requête /api/update reçue.")
    resultat = mise_a_jour()
    # Adaptez la logique ici si mise_a_jour retourne un tuple (False, message)
    if isinstance(resultat, tuple):
        success = resultat[0]
        message = resultat[1]
    else:
        success = resultat
        message = f"Système {'mis à jour' if resultat is True else 'échec de la mise à jour'}."
    return jsonify({"success": success, "message": message}), (200 if success is True else 500)

@admin.route('/api/launch', methods=['POST'])
def api_launch():
    data = request.get_json()
    packet_name = data.get('packet_name')
    print(f"DEBUG: Requête /api/launch reçue pour le paquet: '{packet_name}'")

    if not packet_name:
        return jsonify({"success": False, "message": "Nom de paquet système manquant."}), 400

    resultat, message = lancer_paquet(packet_name)
    
    return jsonify({"success": resultat, "message": message}), (200 if resultat is True else 500)

# Nouvelle route API pour vérifier l'état d'installation d'un paquet
@admin.route('/api/check_package_state', methods=['GET'])
def api_check_package_state():
    packet_name = request.args.get('packet_name')
    print(f"DEBUG: Requête /api/check_package_state reçue pour le paquet: '{packet_name}'")

    if not packet_name:
        return jsonify({"success": False, "message": "Nom de paquet manquant.", "is_installed": "unknown"}), 400

    is_installed = est_installe(packet_name) # Appel à la fonction est_installe
    return jsonify({"success": True, "is_installed": is_installed}), 200