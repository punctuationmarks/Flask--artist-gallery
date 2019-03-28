import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_googlemaps import GoogleMaps
from flask_app.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
googlemap = GoogleMaps()
login_manager = LoginManager()
login_manager.login_view = 'users_bp.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    googlemap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from flask_app.users.routes import users_bp
    from flask_app.main.routes import main_bp
    from flask_app.portfolio.routes import portfolio_bp
    from flask_app.gallery.routes import gallery_bp
    from flask_app.blog.routes import blog_bp
    from flask_app.errors.handlers import errors_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(errors_bp)

    return app
