from flask import Flask
from flask_cors import CORS

def create_app():
    print("📦 Creating Flask app")

    app = Flask(__name__)
    CORS(app)

    try:
        print("📦 Importing routes...")
        from app.routes.property_routes import property_bp
        app.register_blueprint(property_bp, url_prefix="/property")
        print("✅ Routes registered")
    except Exception as e:
        print("❌ ERROR in routes:", e)

    @app.route("/")
    def home():
        return "✅ API is running"

    return app