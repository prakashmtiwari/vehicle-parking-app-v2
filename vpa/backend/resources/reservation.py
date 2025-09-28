from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.backend.models import Reservation, User, Parking_Spot as Spot
from vpa.backend.extensions import db
from datetime import datetime
from vpa.backend.utils.decorators import admin_required, user_required


def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

class ReservationListResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        #Get all reservations by all users (admin only)
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

class UserReservationListResource(Resource):
    @jwt_required()
    @user_required
    def get(self):
        """Get all reservations of the logged-in user"""
        current_user = User.query.get(int(get_jwt_identity()))
        reservations = Reservation.query.filter_by(user_id=current_user.id).all()
        return [
            {
                "id": r.id,
                "spot_id": r.spot_id,
                "vehicle_number": r.vehicle_number,
                "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                "amount_paid": r.amount_paid,
                "spot": {
                    "id": r.spot.id,
                    "status": r.spot.status,
                    "lot": {
                        "id": r.spot.lot.id,
                        "prime_location_name": r.spot.lot.prime_location_name
                    }
                 } if r.spot else None
            } for r in reservations
        ], 200
    
    @jwt_required()
    @user_required
    def post(self):
        """User books a reservation"""
        
        current_user = User.query.get(int(get_jwt_identity()))
        data = request.get_json()

        try:
            reservation = Reservation(
                spot_id=data["spot_id"],
                vehicle_number=data["vehicle_number"],
                user_id=current_user.id,   # <-- linked to logged-in user
                parking_timestamp=datetime.now(),
                leaving_timestamp=None,
                amount_paid=None
            )

            #Update spot status to 'O' (Occupied)
            spot = Spot.query.get_or_404(data["spot_id"])
            if spot.status != 'A':  # A for Available
                return {"message": "Spot is not available"}, 400
            spot.status = 'O'  # O for Occupied     

            db.session.add(reservation)
            db.session.commit()
            return {"message": "Reservation created", "id": reservation.id}, 201
        except Exception as e:
            return {"message": f"Error creating reservation: {e}"}, 500
        
    @jwt_required()
    @user_required
    def put(self, reservation_id):
        """User can update their own reservation"""
        current_user = User.query.get(int(get_jwt_identity()))
        reservation = Reservation.query.get_or_404(reservation_id)

        if reservation.user_id != current_user.id:
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        reservation.spot_id = data.get("spot_id", reservation.spot_id)
        reservation.vehicle_number = data.get("vehicle_number", reservation.vehicle_number)
        reservation.parking_timestamp = data.get("parking_timestamp", reservation.parking_timestamp)
        reservation.leaving_timestamp = data.get("leaving_timestamp", reservation.leaving_timestamp)
        reservation.amount_paid = data.get("amount_paid", reservation.amount_paid)

        db.session.commit()
        return {"message": "Reservation updated"}, 200              
    
class ReservationResource(Resource):
    
    @jwt_required()
    @admin_required
    def put(self, reservation_id):
        # Admin can update any reservation
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
    
   

#Not needed normally, better to let users cancel their own reservations
    # @jwt_required()
    # @admin_required
    # def delete(self, reservation_id):
    #     reservation = Reservation.query.get_or_404(reservation_id)
    #     db.session.delete(reservation)
    #     db.session.commit()
    #     return {"message": "Reservation deleted"}, 200
