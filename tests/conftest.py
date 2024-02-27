import pytest
from main import get_app


@pytest.fixture()
def app():
    app = get_app({
        'TESTING': True
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
