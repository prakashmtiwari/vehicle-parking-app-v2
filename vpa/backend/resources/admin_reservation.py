from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.backend.models import Reservation, User
from vpa.backend.extensions import db
from datetime import datetime

def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

class ReservationListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        reservations = Reservation.query.all()
        return [
            {
                "id": r.id,
                "spot_id": r.spot_id,
                "vehicle_number": r.vehicle_number,
                "user_id": r.user_id,
                "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                "amount_paid": r.amount_paid
            } for r in reservations
        ], 200

    @jwt_required()
    def post(self):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        data = request.get_json()
        reservation = Reservation(
            spot_id=data["spot_id"],
            vehicle_number=data["vehicle_number"],
            user_id=data.get("user_id"),
            parking_timestamp=datetime.now(),
            leaving_timestamp=None,
            amount_paid=data.get("amount_paid")
        )
        db.session.add(reservation)
        db.session.commit()
        return {"message": "Reservation created", "id": reservation.id}, 201


class ReservationResource(Resource):
    @jwt_required()
    def put(self, reservation_id):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        reservation = Reservation.query.get_or_404(reservation_id)
        data = request.get_json()
        reservation.spot_id = data.get("spot_id", reservation.spot_id)
        reservation.vehicle_number = data.get("vehicle_number", reservation.vehicle_number)
        reservation.user_id = data.get("user_id", reservation.user_id)
        reservation.parking_timestamp = data.get("parking_timestamp", reservation.parking_timestamp)
        reservation.leaving_timestamp = data.get("leaving_timestamp", reservation.leaving_timestamp)
        reservation.amount_paid = data.get("amount_paid", reservation.amount_paid)

        db.session.commit()
        return {"message": "Reservation updated"}, 200

    @jwt_required()
    def delete(self, reservation_id):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        reservation = Reservation.query.get_or_404(reservation_id)
        db.session.delete(reservation)
        db.session.commit()
        return {"message": "Reservation deleted"}, 200
