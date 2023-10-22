from app import create_app,db, initialize_db,teardown
import pytest




@pytest.fixture
def client():
    """
    CREATES a mock app instance for testing purposes
    """
    app = create_app(testing=True)
    initialize_db(app)
    with app.test_client() as testing_client: 
        with app.app_context():
            yield testing_client
    teardown(app)

@pytest.fixture
def init_database():
    """
    Creates a new database for the test and destroys it after the test is done.
    """
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
