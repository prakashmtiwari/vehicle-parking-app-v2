from vpa.beserver.scheduler.init_celery import celery
from vpa.beserver.extensions import db
from vpa.beserver.models import User, Reservation, Parking_Spot, Parking_Lot
from vpa.beserver.utils.send_alerts import send_gchat_message

import logging

logger = logging.getLogger(__name__)

@celery.task
def send_gchat_daily_reminder(parking_lot_id: int):
    """
    Send reminder to users who haven't visited (made reservation) in a specific parking lot.
    """
    users_with_reservation = (
        db.session.query(User.id)
        .join(Reservation)
        .join(Parking_Spot)
        .filter(Parking_Spot.lot_id == parking_lot_id)
        .distinct()
        .all()
    )
    users_with_reservation_ids = [u.id for u in users_with_reservation]

    users_without_reservation = (
        db.session.query(User)
        .filter(User.active == True)
        .filter(~User.id.in_(users_with_reservation_ids))
        .all()
    )

    if not users_without_reservation:
        return f"All users have already visited lot {parking_lot_id}."

    lot = Parking_Lot.query.get(parking_lot_id)
    for user in users_without_reservation:
        if user.username == "admin":
            continue  # Skip admin users
        message = (
            f"👋 Hi {user.first_name or user.username},\n\n"
            f"A new parking lot is available: **{lot.prime_location_name}** 🚗\n"
            f"You haven’t booked a spot here yet!\n\n"
            f"👉 [Click here to view and reserve a spot]("
            f"http://localhost:5173/parking-lot-list"
            f")"
        )
        send_gchat_message(message)

    return f"✅ Sent reminders to {len(users_without_reservation)} users for lot {parking_lot_id}."


@celery.task
def send_gchat_daily_reminders_for_all_lots():
    """
    Runs once daily.
    Iterates through parking lots and calls each reminder task sequentially.
    """
    lots = Parking_Lot.query.all()
    if not lots:
        return "No parking lots found."

    for lot in lots:
        print(f"🚗 Processing reminders for lot: {lot.prime_location_name}")
        # Run synchronously so one finishes before next begins
        send_gchat_daily_reminder.apply(args=(lot.id,))
        print(f"✅ Completed lot: {lot.id}")

    return f"✅ Sequentially processed {len(lots)} parking lots."