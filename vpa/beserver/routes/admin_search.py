from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from vpa.beserver.models import Parking_Lot, Parking_Spot, User
from vpa.beserver.utils.decorators import admin_required

search_bp = Blueprint("search", __name__)


@search_bp.route("/search/lots", methods=["GET"])
@jwt_required()
@admin_required
def search_parking_lots():
    query = request.args.get("query", "").strip()

    lots_query = Parking_Lot.query

    if query:
        lots_query = lots_query.filter(
            (Parking_Lot.prime_location_name.ilike(f"%{query}%")) |
            (Parking_Lot.pin_code.ilike(f"%{query}%"))
        )

    lots = lots_query.all()

    return jsonify([
        {"id": lot.id, "name": lot.prime_location_name, "price": lot.price, "pincode": lot.pin_code, "address": lot.address}
        for lot in lots
    ])


@search_bp.route("/search/spots", methods=["GET"])
@jwt_required()
@admin_required
def search_parking_spots():
    status = request.args.get("status", "").lower().strip()

    spots = Parking_Spot.query

    if status == "available":
        spots = spots.filter(Parking_Spot.status == 'A')
    elif status == "occupied":
        spots = spots.filter(Parking_Spot.status == 'O')


    return jsonify([
        {"id": s.id, "lot_id": s.lot_id if s.lot_id else "None", "location": s.lot.prime_location_name, "status": s.status}
        for s in spots
    ])


@search_bp.route("/search/users", methods=["GET"])
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
