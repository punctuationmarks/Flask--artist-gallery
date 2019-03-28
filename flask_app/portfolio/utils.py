import os
import secrets
from PIL import Image
from flask import url_for, current_app

def save_portfolio_picture(form_picture):
    random_hex = secrets.token_hex(2)
    name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = name + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/portfolio_pics', picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
