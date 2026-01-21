import pytest
from flask import Flask
from admin.routes import admin

# Création de l'application Flask pour les tests
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(admin, url_prefix='/admin')
    return app

# Fournit un client de test Flask
@pytest.fixture
def client(app):
    return app.test_client()

# Test : installation réussie d’un paquet
def test_install_success(client, monkeypatch):
    monkeypatch.setattr("admin.routes.install_paquet", lambda pkg: True)
    response = client.post('/admin/api/install', json={"packet_name": "test-package"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] is True
    assert "installé" in data["message"]

# Test : installation échoue car aucun nom de paquet n'est fourni
def test_install_missing_name(client):
    response = client.post('/admin/api/install', json={})
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] is False

# Test : désinstallation réussie d’un paquet
def test_uninstall_success(client, monkeypatch):
    monkeypatch.setattr("admin.routes.desinstaller_paquet", lambda pkg: True)
    response = client.post('/admin/api/uninstall', json={"packet_name": "test-package"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] is True
    assert "désinstallé" in data["message"]

# Test : désinstallation échouée avec message d'erreur personnalisé
def test_uninstall_with_error_message(client, monkeypatch):
    monkeypatch.setattr("admin.routes.desinstaller_paquet", lambda pkg: (False, "Erreur personnalisée"))
    response = client.post('/admin/api/uninstall', json={"packet_name": "test-package"})
    data = response.get_json()
    assert response.status_code == 500
    assert data["success"] is False
    assert data["message"] == "Erreur personnalisée"

# Test : mise à jour réussie du système
def test_update_success(client, monkeypatch):
    monkeypatch.setattr("admin.routes.mise_a_jour", lambda: True)
    response = client.post('/admin/api/update')
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] is True

# Test : mise à jour échouée avec message d’erreur
def test_update_with_message(client, monkeypatch):
    monkeypatch.setattr("admin.routes.mise_a_jour", lambda: (False, "Mise à jour échouée"))
    response = client.post('/admin/api/update')
    data = response.get_json()
    assert response.status_code == 500
    assert data["success"] is False
    assert data["message"] == "Mise à jour échouée"

# Test : lancement d’un paquet avec succès
def test_launch_success(client, monkeypatch):
    monkeypatch.setattr("admin.routes.lancer_paquet", lambda pkg: (True, f"Le paquet '{pkg}' a été lancé"))
    response = client.post('/admin/api/launch', json={"packet_name": "test-package"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] is True
    assert "a été lancé" in data["message"]

# Test : lancement échoue car aucun nom de paquet n'est fourni
def test_launch_missing_name(client):
    response = client.post('/admin/api/launch', json={})
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] is False

# Test : vérifie que le paquet est installé (cas succès)
def test_check_package_state_true(client, monkeypatch):
    monkeypatch.setattr("admin.routes.est_installe", lambda pkg: True)
    response = client.get('/admin/api/check_package_state?packet_name=test-package')
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] is True
    assert data["is_installed"] is True

# Test : vérifie l'état d’un paquet sans fournir de nom
def test_check_package_state_missing_name(client):
    response = client.get('/admin/api/check_package_state')
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] is False
    assert data["is_installed"] == "unknown"
