from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from app.models import db, User, Profile
from .forms import ProfileForm

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def view_profile():
    profile = current_user.profile
    return render_template('profile_view.html', user=current_user, profile=profile)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile = current_user.profile or Profile(user_id=current_user.id)
    form = ProfileForm(obj=profile)

    if form.validate_on_submit():
        form.populate_obj(profile)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('profile.view_profile'))

    return render_template('profile_edit.html', form=form)
