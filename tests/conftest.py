import pytest
from app import create_app, db


@pytest.fixture(scope='function')
def app():
    """Crée une instance de l'app en mode test."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Client de test Flask."""
    return app.test_client()


@pytest.fixture
def auth_header(client):
    """
    Crée un utilisateur, se connecte, et retourne
    le header Authorization prêt à l'emploi.
    """
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'password123'
    })

    response = client.post('/auth/login', json={
        'email': 'test@test.com',
        'password': 'password123'
    })

    token = response.get_json()['token']
    return {'Authorization': f'Bearer {token}'}