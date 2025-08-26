from flask import Flask
from .routes_main import bp as main_bp
from .routes_resume import bp as resume_bp
from auth import auth_bp
from config import CONFIG


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="../static")
    app.config.from_object(CONFIG)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(resume_bp, url_prefix="/resume")

    @app.errorhandler(413)
    def too_large(e):
        return ("Payload too large", 413)

    return app