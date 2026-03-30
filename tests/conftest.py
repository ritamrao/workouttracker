import pytest
from app import create_app, db as _db
from app.models import User

TEST_CONFIG = {
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SECRET_KEY': 'test-secret',
    'WTF_CSRF_ENABLED': False,
    'ADMIN_PASSWORD': 'adminpass123',
}


@pytest.fixture
def app():
    app = create_app(TEST_CONFIG)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def admin_user(db):
    user = User(username='admin', is_admin=True)
    user.set_password('adminpass123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def regular_user(db):
    user = User(username='alice', is_admin=False)
    user.set_password('alicepass123')
    db.session.add(user)
    db.session.commit()
    return user


def login(client, username, password):
    return client.post('/auth/login', data={
        'username': username,
        'password': password,
    }, follow_redirects=True)
