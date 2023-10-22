import pytest
from app import app, db


@pytest.fixture(scope='module')
def test_app():
    """
    CREATES a mock app instance for testing purposes
    """
    app.config['TESTING'] = True
    with app.app_context():
        yield app  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database():
    """
    Creates a new database for the test and destroys it after the test is done.
    """
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
