from flask import (render_template, url_for,
                    flash, redirect,
                    request, abort,
                    Blueprint)
from flask_app import db, bcrypt
from flask_app.users.forms import (RegistrationForm, LoginForm,
                                    RequestResetForm, UpdateAccountForm,
                                    ResetPasswordForm)
from flask_app.users.utils import save_user_picture, send_reset_email
from flask_app.models import User

from flask_login import login_user, current_user, logout_user, login_required


users_bp = Blueprint('users_bp', __name__)

### Register New User
# REMOVE ONCE YOUR ARTISTS + ADMIN ARE REGISTERED
@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users_bp.login'))
    return render_template('register.html', title='Register', form=form)


### Login (change the /route to conseal n00bz from trying to hack you) ###
@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            # this pushes the user to the page they were trying to click on
            # before getting force redirected to the login page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main_bp.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


### Logout ###
@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.home'))




@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_user_picture(form.picture.data)
            current_user.user_picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('users_bp.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    user_picture = url_for('static', filename='profile_pics/' + current_user.user_picture)
    return render_template('account.html', title='Account',
                           user_picture=user_picture, form=form)



@users_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users_bp.login'))
    return render_template('reset_request.html', title='Reset Password?', form=form)


@users_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users_bp.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users_bp.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
