import pytest

from auth.infrastructure.database import db


@pytest.fixture(scope='function')
def database(request):
    db.metadata.create_all(db.engine)

    def teardown():
        db.session.close()
        db.metadata.drop_all(db.engine)

    request.addfinalizer(teardown)
