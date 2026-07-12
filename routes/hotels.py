from flask import Blueprint, jsonify

from config.database import get_collection

hotels_bp = Blueprint("hotels", __name__)


def _serialize(hotel):
    """Shape a hotel document for the response (Hotel ID = _id)."""
    return {
        "hotel_id": str(hotel["_id"]),
        "name": hotel.get("name"),
        "description": hotel.get("description"),
        "location": hotel.get("location"),
        "price_per_night": hotel.get("price_per_night"),
    }


# GET /hotels – list all hotels
@hotels_bp.route("", methods=["GET"])
def list_hotels():
    hotels = get_collection("hotels").find()
    return jsonify([_serialize(h) for h in hotels])
