import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_app import db, mail
from flask_mail import Message


def save_user_picture(form_picture):
    random_hex = secrets.token_hex(3)
    name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = name + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@artist_portfolio.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users_bp.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
Also, hit John up, because that means someone might be messing with your account
'''
    mail.send(msg)
