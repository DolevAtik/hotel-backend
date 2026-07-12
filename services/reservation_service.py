import re
from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId

from config.database import get_collection

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ReservationError(Exception):
    """Raised when a reservation is invalid or violates a business rule."""


def _reservations():
    return get_collection("reservations")


def _hotels():
    return get_collection("hotels")


def _serialize(reservation):
    """Shape a stored document into the response format (Reservation ID = _id)."""
    return {
        "reservation_id": str(reservation["_id"]),
        "full_name": reservation["full_name"],
        "email": reservation["email"],
        "check_in_date": reservation["check_in_date"],
        "check_out_date": reservation["check_out_date"],
        "hotel_id": reservation["hotel_id"],
    }


def _parse_date(value, field):
    if not value:
        raise ReservationError(f"{field} is required")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ReservationError(f"{field} must be a valid date (YYYY-MM-DD)")


# Function 1 – Create Reservation
def create_reservation(data):
    full_name = (data.get("full_name") or "").strip()
    email = (data.get("email") or "").strip()
    hotel_id = (data.get("hotel_id") or "").strip()

    # --- Validate reservation details ---
    if not full_name:
        raise ReservationError("full_name is required")
    if not email:
        raise ReservationError("email is required")
    if not EMAIL_RE.match(email):
        raise ReservationError("email is not a valid email address")
    if not hotel_id:
        raise ReservationError("hotel_id is required")

    check_in = _parse_date(data.get("check_in_date"), "check_in_date")
    check_out = _parse_date(data.get("check_out_date"), "check_out_date")

    # --- Verify business rules ---
    if check_out <= check_in:
        raise ReservationError("check_out_date must be after check_in_date")

    try:
        hotel_oid = ObjectId(hotel_id)
    except InvalidId:
        raise ReservationError("hotel_id is not valid")
    if _hotels().find_one({"_id": hotel_oid}) is None:
        raise ReservationError("hotel does not exist")

    # --- Store reservation data ---
    reservation = {
        "full_name": full_name,
        "email": email,
        "check_in_date": check_in.isoformat(),
        "check_out_date": check_out.isoformat(),
        "hotel_id": hotel_id,
    }
    result = _reservations().insert_one(reservation)
    reservation["_id"] = result.inserted_id
    return _serialize(reservation)


# Function 2 – Reservation Lookup
def get_reservation(reservation_id):
    try:
        oid = ObjectId(reservation_id)
    except InvalidId:
        return None
    reservation = _reservations().find_one({"_id": oid})
    return _serialize(reservation) if reservation else None


# Function 3 – Cancel Reservation
def cancel_reservation(reservation_id):
    try:
        oid = ObjectId(reservation_id)
    except InvalidId:
        return False
    result = _reservations().delete_one({"_id": oid})
    return result.deleted_count > 0
