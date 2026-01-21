import os
from flask import Flask, render_template
from config import config_dic 
from dotenv import load_dotenv 

# Importe la fonction 'slugify' pour créer des slugs d'URL.
from portail.routes import slugify 

load_dotenv() # Charge les variables d'environnement depuis '.env'.

# Fonction factory pour créer et configurer l'application Flask.
def create_app(config_name=None):
    # Définit le nom de la configuration (ex: "development" ou "production").
    if config_name is None:
        config_name = os.environ.get("CONFIG", "development") 

    app = Flask(__name__)
    # Charge la configuration de l'application.
    app.config.from_object(config_dic[config_name])

    # Enregistre le filtre Jinja 'slug' pour utilisation dans les templates.
    app.jinja_env.filters['slug'] = slugify

    with app.app_context():
        # Importe et enregistre les Blueprints de l'application.
        from .routes import portail 
        from admin.routes import admin 

        app.register_blueprint(portail)
        app.register_blueprint(admin, url_prefix='/admin') 
        
        # Définit la page d'erreur 404 personnalisée.
        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404

        return app