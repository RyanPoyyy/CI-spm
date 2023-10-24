import os
from app import app,db, initialize_db,teardown, create_app
import pytest


@pytest.fixture
def client():
    """
    CREATES a mock app instance for testing purposes
    """
    app = create_app(test_db=True)

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("TEST_DB_URL")
    # print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.config['TESTING'] = True

    with app.test_client() as testing_client: 
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture
def init_database():
    """
    Creates a new database for the test and destroys it after the test is done.
    """
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
