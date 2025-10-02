from datetime import datetime
from vpa.models import Reservation, db

def release_spot(reservation_id):
    """Release a parking spot by setting its reservation's leaving_timestamp"""
    reservation = Reservation.query.filter_by(id=reservation_id).first()
    if reservation:
        reservation.leaving_timestamp = datetime.now()
        db.session.commit()
        return True
    return False
