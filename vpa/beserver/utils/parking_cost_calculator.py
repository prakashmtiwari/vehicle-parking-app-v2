from datetime import datetime
from vpa.beserver.models import Reservation, User
from flask_jwt_extended import get_jwt_identity


def compute_parking_cost(reservation_id, current_user_id=None):
    """Reusable logic to compute cost for a reservation."""
    reservation = Reservation.query.get_or_404(reservation_id)

    if current_user_id and reservation.user_id != current_user_id:
        return {"message": "Unauthorized"}, 403

    if reservation.leaving_timestamp is not None:
        return {"message": "Reservation already completed"}, 400

    reservation.leaving_timestamp = datetime.now()

    try:
        amount_paid = parking_cost(reservation)
    except Exception as e:
        return {"message": f"Error calculating parking cost: {e}"}, 500

    return {"message": "Reservation Cost Computed Successfully", "parking_cost": amount_paid}, 200



def parking_cost(reservation):
    """Calculate parking cost based on duration and lot rate."""

    if not reservation.parking_timestamp or not reservation.leaving_timestamp:
        raise ValueError("Both parking and leaving timestamps must be set to calculate cost.")
    
    if reservation.amount_paid is not None:
        return reservation.amount_paid  # Cost already calculated

    try:
        duration_hours = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
        rate_per_hour = reservation.spot.lot.price  

        amount_paid = round(duration_hours * rate_per_hour, 2)
        print(f"Calculated parking cost: {amount_paid} for duration: {duration_hours} hours at rate: {rate_per_hour}/hour")
    except Exception as e:
        print(e)
        raise ValueError(f"Error in calculating parking cost function: {e}")    

    return amount_paid