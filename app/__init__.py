from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from app.config import config_by_name

# ── Extensions (initialisées sans app) ──
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app(config_name='development'):
    """
    Factory pattern — crée et configure l'application Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # ── Initialisation des extensions ──
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # ── Enregistrement des routes (blueprints via RESTX) ──
    from app.routes import register_routes
    register_routes(app)

    # ── Création des tables ──
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app