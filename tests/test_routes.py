import pytest
from portail.routes import load_resources_data

# --- Test de la route d'accueil "/" ---
def test_index_route(client):
    """
    Vérifie que la route d'accueil (/) retourne un code 200 et contient des cartes de ressources.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Ressources' in response.data  

# --- Test de la route /resource/<slug> avec un slug valide ---
def test_resource_detail_valid_slug(client):
    """
    Vérifie que la route /resource/<slug> fonctionne avec un slug valide.
    """
    resources = load_resources_data()
    if not resources:
        pytest.skip("Aucune ressource disponible pour tester.")

    valid_slug = next(iter(resources.keys()))
    response = client.get(f'/resource/{valid_slug}')
    assert response.status_code == 200
    assert resources[valid_slug].title.encode('utf-8') in response.data

# --- Test de la route /resource/<slug> avec un slug invalide ---
def test_resource_detail_invalid_slug(client):
    """
    Vérifie que la route /resource/<slug> renvoie une erreur 404 pour un slug inexistant.
    """
    response = client.get('/resource/slug-inexistant-xyz')
    assert response.status_code == 404
    assert 'Page non trouvée'.encode('utf-8') in response.data or b'404' in response.data

