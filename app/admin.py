from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User

admin = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            return render_template('403.html'), 403
        return f(*args, **kwargs)
    return decorated


@admin.route('/users')
@admin_required
def users():
    all_users = User.query.order_by(User.created_at).all()
    return render_template('admin/users.html', users=all_users)


@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.users'))
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User {username} deleted.', 'success')
    return redirect(url_for('admin.users'))


@admin.route('/users/<int:user_id>/reset-password', methods=['GET', 'POST'])
@admin_required
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.set_password(request.form['password'])
        db.session.commit()
        flash(f'Password reset for {user.username}.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/reset_password.html', user=user)
