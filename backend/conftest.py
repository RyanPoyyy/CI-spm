import os
from app import app,db, initialize_db,teardown
import pytest


@pytest.fixture
def client():
    """
    CREATES a mock app instance for testing purposes
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("TEST_DB_URL")
    app.config['TESTING'] = True
    # with app.app_context():
    #     app.create_all()
    # initialize_db()
    teardown(app)
    with app.test_client() as testing_client: 
        with app.app_context():
            initialize_db(app)
            yield testing_client
    # teardown(app)

    


# @pytest.fixture
# def setup(client):
#     """
#     Creates a new database for the test and destroys it after the test is done.
#     """
#     with client.app_context():
#         db.create_all()

# @pytest.fixture
# def teardown(client):

