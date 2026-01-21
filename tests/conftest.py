import pytest
from portail import create_app

# Cette fixture crée une instance de l'application Flask pour les tests
@pytest.fixture
def app():
    # On crée l'application avec la factory
    app = create_app()
    # On applique une configuration spéciale pour les tests
    app.config.update({
        "TESTING": True,                # Active le mode test (Flask ne gère pas les erreurs comme en prod)
        "PROPAGATE_EXCEPTIONS": False, # Empêche la propagation des exceptions (utile pour tester les erreurs HTTP)
    })
    # On "yield" l'application, ce qui permet de l'utiliser dans les tests
    yield app

# Cette fixture fournit un client de test pour simuler des requêtes HTTP (GET, POST, etc.)
@pytest.fixture
def client(app):
    return app.test_client()

# Cette fixture fournit un runner pour exécuter des commandes CLI personnalisées Flask
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
