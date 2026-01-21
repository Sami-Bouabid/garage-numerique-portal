# 🔧 Portail de Ressources - Flask

Ce projet est une application web construite avec **Flask** côté backend et **JavaScript Vanilla** côté frontend.
Il permet de consulter des ressources classées par catégorie, avec distinction entre ressources téléchargeables et non téléchargeables.

---

## 🧩 Fonctionnalités principales

* **📁 Chargement et parsing d’un fichier `ressources.json` :** Utilisation d'une fonction Python (dans `utils.py`) pour lire et interpréter les données des ressources.
* **🎴 Affichage dynamique des ressources :** Génération et présentation des ressources sous forme d'objets Python appelés cartes via `index.html`.
* **🧠 Filtrage et tri :** Possibilité de filtrer par catégorie ou trier par ordre alphabétique, fonctionnalité implémentée dans `sort.js`.
* **🔍 Barre de recherche intégrée :** Permet aux utilisateurs de rechercher des ressources spécifiques `search.js`.
* **🧭 Séparation claire :** Distinction visuelle entre les ressources qui peuvent être téléchargées et celles qui le peuvent pas.
* **📡 Interface web fluide :** Interface utilisateur développée en HTML, JavaScript et CSS, avec l'utilisation du moteur de templating Jinja2 et du framework CSS Bulma.

---

## 🚀 Avancement

* Le Design de l'interface utilisateur est en cours d'amélioration.
* La fonctionnalité de Barre de recherche est en développement.
* Aucun Test Unitaire n'a été implémenté pour le moment.

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


    
