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
