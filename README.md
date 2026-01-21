## 🛠️ Le Garage Numérique - Portail de Ressources

Un catalogue de ressources numériques dédié à l'association Le Garage Numérique, qui milite depuis 2012 pour l'innovation sociale et l'usage des logiciels libres.

## 💡 Le Contexte

Le Garage Numérique avait besoin d'une plateforme centralisée pour partager ses outils pédagogiques. En accord avec les valeurs d'Éducation Populaire de l'association, ce portail a été conçu pour être léger, modulaire et facile à naviguer.

## 🏗️ Architecture Technique

Ce projet utilise le pattern Application Factory, garantissant une application scalable et testable.

Application Factory (create_app) : Centralise la création de l'instance Flask et gère les environnements via un dictionnaire de configuration.

Modularité par Blueprints : Séparation stricte entre le portail (public) et l'interface admin (gestion), accessible via le préfixe /admin.

Filtres Jinja2 Personnalisés : Intégration d'un filtre slug pour générer des URLs propres et optimisées pour le SEO.

Gestion Sécurisée : Utilisation de python-dotenv pour isoler les variables sensibles (SECRET_KEY). 

## 🛠 Stack Technique
🚀 Fonctionnalités Clés

Recherche Dynamique : Filtrage en temps réel des ressources via JavaScript.

Interface Responsive : Design moderne incluant un Mode Sombre (Dark Mode).

Gestion Admin : Routes sécurisées pour l'administration des contenus.

Portabilité : Stockage des données structuré en JSON pour une légèreté maximale.

## 🧪 Suite de Tests

La fiabilité du code est assurée par une suite de tests complète :

test_admin_routes.py : Validation des accès et fonctions administratifs.

test_routes.py : Tests d'intégration des vues publiques.

test_fonctions.py : Tests unitaires de la logique métier.

Exécuter les tests : pytest
📥 Installation

    Cloner le projet : git clone <url-du-repo>

    Installer les dépendances : pip install -r requirements.txt

    Configuration : Copier .env.example vers .env et remplir la SECRET_KEY.

    Lancer : python app.py

## 🧠 Expérience Collaborative (Équipe de 5)

Ce projet a été développé en équipe, ce qui a permis de mettre en pratique :

GitFlow : Utilisation rigoureuse de branches et de Pull Requests pour éviter les conflits.

Communication Technique : Coordination sur l'architecture des Blueprints pour permettre un développement parallèle.

📄 Licence

Distribué sous licence MIT. En soutien aux Logiciels Libres.

## ⚙ Lancer l'application

1.  **Cloner le projet Git :**
    ```bash
    git clone git@git.legaragenumerique.fr:gauthier/LGN_Portal.git
    ```
2.  **Entrer dans le répertoire du projet :**
    ```bash
    cd LGN_Portal/
    ```
3.  **Créer un environnement virtuel :** (Remplacez `NOM_DE_VOTRE_CHOIX` par le nom souhaité pour votre environnement)
    ```bash
    python3 -m venv NOM_DE_VOTRE_CHOIX
    ```
4.  **Activer l'environnement virtuel :**
    ```bash
    source NOM_DE_VOTRE_CHOIX/bin/activate
    ```
5.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Lancer l'application Flask :**
    ```bash
    python3 app.py
    ```
7. **Rendez-vous sur l'URL:** 
    `http://127.0.0.1:5000/` pour visualiser l'application dans votre navigateur.


    
