from flask import Flask
from flask_cors import CORS

def create_app():
    print("Creating Flask app")

    app = Flask(__name__)
    CORS(app)

    print("Importing routes...")
    from app.routes.property_routes import property_bp
    app.register_blueprint(property_bp, url_prefix="/property")
    print("Routes registered")

    @app.route("/")
    def home():
        return "API is running"

    return app
