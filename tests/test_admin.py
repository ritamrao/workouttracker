import pytest
from tests.conftest import login
from app.models import User


# ── Access control ─────────────────────────────────────────────────────────────

def test_admin_users_requires_login(client):
    response = client.get('/admin/users', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_admin_users_requires_admin_role(client, regular_user):
    login(client, 'alice', 'alicepass123')
    response = client.get('/admin/users')
    assert response.status_code == 403


def test_admin_users_accessible_to_admin(client, admin_user):
    login(client, 'admin', 'adminpass123')
    response = client.get('/admin/users')
    assert response.status_code == 200
    assert b'admin' in response.data


# ── Delete user ────────────────────────────────────────────────────────────────

def test_admin_delete_user(client, admin_user, regular_user, db, app):
    login(client, 'admin', 'adminpass123')
    response = client.post(f'/admin/users/{regular_user.id}/delete',
                           follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert User.query.filter_by(username='alice').first() is None


def test_admin_cannot_delete_self(client, admin_user):
    login(client, 'admin', 'adminpass123')
    response = client.post(f'/admin/users/{admin_user.id}/delete',
                           follow_redirects=True)
    assert b'cannot delete your own account' in response.data.lower()
    with client.application.app_context():
        assert User.query.filter_by(username='admin').first() is not None


# ── Reset password ─────────────────────────────────────────────────────────────

def test_admin_reset_password(client, admin_user, regular_user, app):
    login(client, 'admin', 'adminpass123')
    response = client.post(
        f'/admin/users/{regular_user.id}/reset-password',
        data={'password': 'newpass999'},
        follow_redirects=True
    )
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username='alice').first()
        assert user.check_password('newpass999') is True
