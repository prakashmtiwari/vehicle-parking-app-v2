import datetime


def parking_cost(reservation):
    """Calculate parking cost based on duration and lot rate."""

    if not reservation.parking_timestamp or not reservation.leaving_timestamp:
        raise ValueError("Both parking and leaving timestamps must be set to calculate cost.")
    
    if reservation.amount_paid is not None:
        return reservation.amount_paid  # Cost already calculated

    try:
        duration_hours = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
        rate_per_hour = reservation.spot.lot.price  

        reservation.amount_paid = round(duration_hours * rate_per_hour, 2)
        print(f"Calculated parking cost: {reservation.amount_paid} for duration: {duration_hours} hours at rate: {rate_per_hour}/hour")
    except Exception as e:
        raise ValueError(f"Error in calculating parking cost function: {e}")    
   
    return reservation.amount_paid