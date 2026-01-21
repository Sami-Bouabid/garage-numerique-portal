import os

# Classe de base contenant configuration commune, que ce soit pour production ou développement
class Config:
    #Sert à obtenir la clé secrète depuis le fichier .env, ou en génère une par défaut si .env vide par exemple
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")

class Dev(Config):
    DEBUG = True # Active le mode debug

class Prod(Config):
    DEBUG = False # Désactive le mode debug

# Dictionnaire permettant de récupérer dynamiquement la classe de configuration dans le __init__.py
config_dic = {
    "development": Dev,
    "production": Prod
} 