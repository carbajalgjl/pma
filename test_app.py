import pytest

# Mock Flask app
from my_flask_app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_registration(client):
    response = client.post('/register', data={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 201  # Check if registration is successful


def test_login(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 200  # Check if login is successful
    
    # Add more assertions based on your application's response
    