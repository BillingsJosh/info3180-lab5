from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from .config import Config
from .models import Movie  # Optional, if needed elsewhere

from .models import db

migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    from .views import main
    app.register_blueprint(main)

    from app import views
    return app

