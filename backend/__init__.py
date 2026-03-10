from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__,
                template_folder='../frontend/templates',
                static_folder='../frontend/static')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'isro-secret-dev-key-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///isro.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    CORS(app)

    from backend.routes.auth    import auth_bp
    from backend.routes.api     import api_bp
    from backend.routes.pages   import pages_bp

    app.register_blueprint(auth_bp,  url_prefix='/auth')
    app.register_blueprint(api_bp,   url_prefix='/api')
    app.register_blueprint(pages_bp)

    with app.app_context():
        db.create_all()

    return app
