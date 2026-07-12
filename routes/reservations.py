from flask import Blueprint, jsonify, request

from services.reservation_service import (
    ReservationError,
    cancel_reservation,
    create_reservation,
    get_reservation,
)

reservations_bp = Blueprint("reservations", __name__)


# Function 1 – Create Reservation
@reservations_bp.route("", methods=["POST"])
def create():
    data = request.get_json(silent=True) or {}
    try:
        reservation = create_reservation(data)
    except ReservationError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({
        "message": "Reservation created successfully",
        "reservation": reservation,
    }), 201


# Function 2 – Reservation Lookup
@reservations_bp.route("/<reservation_id>", methods=["GET"])
def lookup(reservation_id):
    reservation = get_reservation(reservation_id)
    if reservation is None:
        return jsonify({"error": "reservation not found"}), 404
    return jsonify(reservation)


# Function 3 – Cancel Reservation
@reservations_bp.route("/<reservation_id>", methods=["DELETE"])
def cancel(reservation_id):
    if get_reservation(reservation_id) is None:
        return jsonify({"error": "reservation not found"}), 404
    cancel_reservation(reservation_id)
    return jsonify({
        "message": "Reservation cancelled successfully",
        "reservation_id": reservation_id,
    })
