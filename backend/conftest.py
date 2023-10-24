import os
from app import app, db,initialize_db,teardown
import pytest


@pytest.fixture
def client():
    """
    CREATES a mock app instance for testing purposes
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("TEST_DB_URL")
    app.config['TESTING'] = True


    # with app.app_context():
    #     db.drop_all()

    with app.app_context():
        db.create_all()
    with app.test_client() as testing_client: 
        with app.app_context():
            # db.create_all()
            yield testing_client
    with app.app_context():
        db.drop_all()
