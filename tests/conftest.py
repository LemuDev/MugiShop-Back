import pytest
from src import app as app_flask

@pytest.fixture
def app():
    yield app_flask
    
@pytest.fixture
def client(app):
    return app.test_client()