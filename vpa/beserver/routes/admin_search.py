from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from vpa.beserver.models import Parking_Lot, Parking_Spot, User
from vpa.beserver.utils.decorators import admin_required

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/lots", methods=["GET"])
@jwt_required()
@admin_required
def search_parking_lots():
    query = request.args.get("query", "").strip()

    if query:
        lots = lots.filter(
            (Parking_Lot.name.ilike(f"%{query}%")) |
            (Parking_Lot.pincode.ilike(f"%{query}%"))
        )

    return jsonify([
        {"id": lot.id, "name": lot.prime_location_name, "price": lot.price, "pincode": lot.pincode, "address": lot.address}
        for lot in lots
    ])


@search_bp.route("/spots", methods=["GET"])
@jwt_required()
@admin_required
def search_parking_spots():
    status = request.args.get("status", "").lower().strip()

    spots = Parking_Spot.query
    if status == "available":
        spots = spots.filter(Parking_Spot.is_occupied == False)
    elif status == "occupied":
        spots = spots.filter(Parking_Spot.is_occupied == True)


    return jsonify([
        {"id": s.id, "lot_id": s.lot_id, "status": s.status}
        for s in spots
    ])


@search_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def search_users():
    query = request.args.get("query", "").strip()

    users = User.query
    if query:
        users = users.filter(
            (User.username.ilike(f"%{query}%")) |
            (User.email.ilike(f"%{query}%"))
        )

    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email, "first_name": u.first_name, "last_name": u.last_name}
        for u in users
    ])
