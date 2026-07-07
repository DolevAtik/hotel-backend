import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from config.database import init_db
from routes.hotels import hotels_bp
from routes.reservations import reservations_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize the database connection and attach it to the app.
    init_db(app)

    app.register_blueprint(hotels_bp, url_prefix="/hotels")
    app.register_blueprint(reservations_bp, url_prefix="/reservations")

    @app.route("/")
    def index():
        return jsonify({
            "service": "hotel-backend",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "list_hotels": "GET /hotels",
                "create_reservation": "POST /reservations",
                "lookup_reservation": "GET /reservations/<id>",
                "cancel_reservation": "DELETE /reservations/<id>",
            },
        })

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
