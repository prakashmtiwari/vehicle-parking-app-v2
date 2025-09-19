from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.backend.models import Reservation, User
from vpa.backend.extensions import db
from datetime import datetime
from vpa.backend.utils.decorators import user_required

class UserReservationListResource(Resource):
    @jwt_required()
    @user_required
    def get(self):
        """Get all reservations of the logged-in user"""
        current_user = User.query.get(get_jwt_identity()["id"])
        reservations = Reservation.query.filter_by(user_id=current_user.id).all()
        return [
            {
                "id": r.id,
                "spot_id": r.spot_id,
                "vehicle_number": r.vehicle_number,
                "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                "amount_paid": r.amount_paid
            } for r in reservations
        ], 200

    @jwt_required()
    @user_required
    def post(self):
        """User books a reservation"""
        current_user = User.query.get(get_jwt_identity()["id"])
        data = request.get_json()

        reservation = Reservation(
            spot_id=data["spot_id"],
            vehicle_number=data["vehicle_number"],
            user_id=current_user.id,   # <-- linked to logged-in user
            parking_timestamp=datetime.now(),
            leaving_timestamp=None,
            amount_paid=data.get("amount_paid")
        )
        db.session.add(reservation)
        db.session.commit()
        return {"message": "Reservation created", "id": reservation.id}, 201


class UserReservationResource(Resource):
    @jwt_required()
    @user_required
    def delete(self, reservation_id):
        """User can cancel their own reservation"""
        current_user = User.query.get(get_jwt_identity()["id"])
        reservation = Reservation.query.get_or_404(reservation_id)

        if reservation.user_id != current_user.id:
            return {"message": "Forbidden"}, 403

        db.session.delete(reservation)
        db.session.commit()
        return {"message": "Reservation cancelled"}, 200
