import pytest
from app.models import User


def test_user_set_and_check_password(app):
    with app.app_context():
        user = User(username='bob')
        user.set_password('secret123')
        assert user.check_password('secret123') is True
        assert user.check_password('wrongpass') is False


def test_user_is_not_admin_by_default(app):
    with app.app_context():
        user = User(username='bob')
        user.set_password('secret123')
        assert user.is_admin is False


def test_user_username_must_be_unique(db, app):
    with app.app_context():
        u1 = User(username='bob')
        u1.set_password('pass1')
        u2 = User(username='bob')
        u2.set_password('pass2')
        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)
        with pytest.raises(Exception):
            db.session.commit()


from tests.conftest import login


# ── Register ──────────────────────────────────────────────────────────────────

def test_register_success(client, app):
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'password': 'newpass123',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Account created' in response.data
    with app.app_context():
        from app.models import User
        assert User.query.filter_by(username='newuser').first() is not None


def test_register_duplicate_username(client, regular_user):
    response = client.post('/auth/register', data={
        'username': 'alice',
        'password': 'anotherpass',
    }, follow_redirects=True)
    assert b'already taken' in response.data


def test_register_page_loads(client):
    response = client.get('/auth/register')
    assert response.status_code == 200


# ── Login / Logout ─────────────────────────────────────────────────────────────

def test_login_success(client, regular_user):
    response = login(client, 'alice', 'alicepass123')
    assert response.status_code == 200
    assert b'alice' in response.data


def test_login_wrong_password(client, regular_user):
    response = login(client, 'alice', 'wrongpass')
    assert b'Invalid username or password' in response.data


def test_login_unknown_user(client):
    response = login(client, 'nobody', 'somepass')
    assert b'Invalid username or password' in response.data


def test_logout_redirects_to_login(client, regular_user):
    login(client, 'alice', 'alicepass123')
    response = client.get('/auth/logout', follow_redirects=True)
    assert b'Log In' in response.data
