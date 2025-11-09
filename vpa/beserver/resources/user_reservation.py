from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.beserver.models import Reservation, User, Parking_Spot as Spot
from vpa.beserver.extensions import db
from datetime import datetime
from vpa.beserver.utils.decorators import user_required
from vpa.beserver.utils.parking_cost_calculator import parking_cost, compute_parking_cost
from vpa.beserver.utils.cache_manager import cached_response, clear_cache

    

class UserReservationListResource(Resource):
    @jwt_required()
    @user_required
    @cached_response(timeout=240, key_prefix="all_user_reservations")
    def get(self):
   # """Get all reservations of the logged-in user"""
        current_user = User.query.get(int(get_jwt_identity()))
        print(current_user)
        reservations = Reservation.query.filter_by(user_id=current_user.id).all()

        result = []
        for r in reservations:
            # calculate duration in hours and minutes
            if r.parking_timestamp and r.leaving_timestamp:
                total_seconds = (r.leaving_timestamp - r.parking_timestamp).total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                duration_str = f"{hours} hours {minutes} minutes"
            else:
                duration_str = "—"

            res_data = {
                "id": r.id,
                "vehicle_number": r.vehicle_number,
                "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                "amount_paid": r.amount_paid,
                "duration": duration_str,
                "spot": {
                    "id": r.spot.id,
                    "status": r.spot.status,
                    "lot": {
                        "id": r.spot.lot.id,
                        "prime_location_name": r.spot.lot.prime_location_name,
                        "price": r.spot.lot.price  # Hourly rate
                    }
                } if r.spot else None
            }
            result.append(res_data)

        return result, 200

    
    @jwt_required()
    @user_required
    def post(self):
        """User books a reservation"""
        
        current_user = User.query.get(int(get_jwt_identity()))
        data = request.get_json()
        parking_timestamp = datetime.strptime(data["parking_timestamp"], "%Y-%m-%dT%H:%M")
        spot = Spot.query.get(data["spot_id"])
        lot_id = spot.lot_id if spot else None  

        try:
            reservation = Reservation(
                spot_id=data["spot_id"],
                vehicle_number=data["vehicle_number"],
                user_id=current_user.id,   # <-- linked to logged-in user
                lot_id=lot_id,
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

            clear_cache("all_user_reservations")

            return {"message": "Reservation created", "id": reservation.id}, 201
        except Exception as e:
            return {"message": f"Error creating reservation: {e}"}, 500
        

class UserReservationResource(Resource):
    @user_required
    def get(self, reservation_id):
        """ Calculates the parking amount of the reservation"""
        current_user_id = int(get_jwt_identity())
        return compute_parking_cost(reservation_id, current_user_id)


    @jwt_required()
    @user_required  
    def post(self, reservation_id):
        """User completes their own reservation by paying and freeing the spot"""
        # make get api call to get the parking cost
        current_user_id = int(get_jwt_identity())
        
        try:
          parking_cost_response = compute_parking_cost(reservation_id, current_user_id)


          parking_cost = parking_cost_response[0]["parking_cost"]

          amount_paid = parking_cost
        
        except Exception as e:
            return {"message": f"Error calculating parking cost: {e}"}, 500   

     
        reservation = Reservation.query.get_or_404(reservation_id)

        # Update spot status back to 'A' (Available)
        spot = Spot.query.get(reservation.spot_id)
        if spot and spot.status == 'O':  # O for Occupied
            spot.status = 'A'  # A for Available     
        
        reservation.amount_paid = amount_paid


        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": f"DB commit failed: {e}"}, 500
        
        clear_cache("all_user_reservations")

        return {
            "message": "Reservation completed",
            "amount_paid": reservation.amount_paid,
            "leaving_timestamp": reservation.leaving_timestamp.isoformat()
        }, 200



# Cancel Reservation by the user
    @jwt_required()
    @user_required
    def delete(self, reservation_id):
        """User can cancel their own reservation"""
        current_user = User.query.get(int(get_jwt_identity()))
        reservation = Reservation.query.get_or_404(reservation_id)

        if reservation.user_id != current_user.id:
            return {"message": "Unauthorized"}, 403

        try:
            #Update spot status back to 'A' (Available) if reservation is active
            spot = Spot.query.get(reservation.spot_id)
            if spot and spot.status == 'O':  # O for Occupied
                spot.status = 'A'  # A for Available     

            db.session.delete(reservation)
            db.session.commit()
            clear_cache("all_user_reservations")

            return {"message": "Reservation cancelled"}, 200  
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error cancelling reservation: {e}"}, 500