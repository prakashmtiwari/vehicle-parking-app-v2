from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.beserver.models import Reservation, User, Parking_Spot as Spot
from vpa.beserver.extensions import db
from datetime import datetime
from vpa.beserver.utils.decorators import admin_required
from vpa.beserver.utils.parking_cost_calculator import parking_cost


class ReservationListResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
    # Get all reservations by all users (admin only)
        reservations = Reservation.query.all()

        result = []
        for r in reservations:
            # Calculate duration in hours and minutes
            if r.parking_timestamp and r.leaving_timestamp:
                delta = r.leaving_timestamp - r.parking_timestamp
                total_minutes = int(delta.total_seconds() // 60)
                hours = total_minutes // 60
                minutes = total_minutes % 60
                duration_str = f"{hours} hours {minutes} minutes"
            else:
                duration_str = "0 hours 0 minutes"

            res_dict = {
                "id": r.id,
                "lot_name": r.spot.lot.prime_location_name if r.spot and r.spot.lot else "N/A",
                "price": r.spot.lot.price if r.spot and r.spot.lot else "N/A",
                "duration": duration_str,
                "spot_id": r.spot_id,
                "vehicle_number": r.vehicle_number or "—",
                "user_name": r.user.username if r.user else f"User #{r.user_id}",
                "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                "amount_paid": r.amount_paid if r.amount_paid is not None else "—"
            }
            result.append(res_dict)

        return result, 200




    
   

