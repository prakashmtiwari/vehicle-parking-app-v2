from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.beserver.models import Reservation, User, Parking_Spot as Spot
from vpa.beserver.extensions import db
from datetime import datetime
from vpa.beserver.utils.decorators import user_required


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
        parking_timestamp = datetime.strptime(data["parking_timestamp"], "%Y-%m-%dT%H:%M")


        try:
            reservation = Reservation(
                spot_id=data["spot_id"],
                vehicle_number=data["vehicle_number"],
                user_id=current_user.id,   # <-- linked to logged-in user
                parking_timestamp=parking_timestamp,
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
        

class UserReservationResource(Resource):
    @jwt_required()
    @user_required  
    def post(self, reservation_id):
        """User completes their own reservation by paying and freeing the spot"""
        current_user = User.query.get(int(get_jwt_identity()))
        reservation = Reservation.query.get_or_404(reservation_id)

        if reservation.user_id != current_user.id:
            return {"message": "Unauthorized"}, 403

        if reservation.leaving_timestamp is not None:
            return {"message": "Reservation already completed"}, 400

        # Set leaving timestamp to now and calculate amount paid
        reservation.leaving_timestamp = datetime.now()
        duration_hours = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
        rate_per_hour = reservation.spot.lot.price  # Example fixed rate, could be dynamic based on lot/spot
        reservation.amount_paid = round(duration_hours * rate_per_hour, 2)

        # Update spot status back to 'A' (Available)
        spot = Spot.query.get(reservation.spot_id)
        if spot and spot.status == 'O':  # O for Occupied
            spot.status = 'A'  # A for Available     

        db.session.commit()
        return {
            "message": "Reservation completed",
            "amount_paid": reservation.amount_paid,
            "leaving_timestamp": reservation.leaving_timestamp.isoformat()
        }, 200



    @jwt_required()
    @user_required
    def delete(self, reservation_id):
        """User can cancel their own reservation"""
        current_user = User.query.get(int(get_jwt_identity()))
        reservation = Reservation.query.get_or_404(reservation_id)

        if reservation.user_id != current_user.id:
            return {"message": "Unauthorized"}, 403

        #Update spot status back to 'A' (Available) if reservation is active
        spot = Spot.query.get(reservation.spot_id)
        if spot and spot.status == 'O':  # O for Occupied
            spot.status = 'A'  # A for Available     

        db.session.delete(reservation)
        db.session.commit()
        return {"message": "Reservation cancelled"}, 200  
    