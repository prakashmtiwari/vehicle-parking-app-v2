from vpa.beserver.scheduler.init_celery import celery
from vpa.beserver.extensions import db
from vpa.beserver.models import User, Reservation, Parking_Spot, Parking_Lot
from vpa.beserver.utils.send_alerts import send_gchat_message, send_gmail_message, send_sms_message

import logging

logger = logging.getLogger(__name__)

#task to send gchat reminders to users who haven't visited a specific parking lot
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



#task to send gmail reminders to users who haven't visited a specific parking lot
@celery.task
def send_gmail_daily_reminder(parking_lot_id: int):
        """
        Notify a user when a new parking lot is available.
        """
        lot = Parking_Lot.query.get(parking_lot_id)
        if not lot:
            return f"Parking lot with ID {parking_lot_id} not found."

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

        
        subject = f"🚗 New Parking Lot Available: {lot.prime_location_name}"


        for user in users_without_reservation:
            if user.username == "admin" or not user.email:
                continue  # Skip admin users and users without email

         # Craft a simple HTML email body

            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <p>👋 Hi {user.first_name or user.username},</p>

                    <p>A new parking lot is now available: 
                    <strong>{lot.prime_location_name}</strong> 🚗</p>

                    <p>You haven’t booked a spot here yet — don’t miss out!</p>

                    <p>
                        👉 <a href="http://localhost:5173/parking-lot-list" 
                            style="background-color:#007bff; color:white; padding:10px 15px; text-decoration:none; border-radius:6px;">
                            View and Reserve a Spot
                        </a>
                    </p>

                    <br>
                    <p>Best,<br>The Parking Assistant Team</p>
                </body>
            </html>
            """

            send_gmail_message(
                to_email=user.email,
                subject=subject,
                body=body
            )

        return f"✅ Sent email to {len(users_without_reservation)} users for lot {parking_lot_id}."


@celery.task
def send_gmail_daily_reminders_for_all_lots():
    """
    Runs once daily.
    Iterates through parking lots and calls each reminder task sequentially.
    """
    lots = Parking_Lot.query.all()
    if not lots:
        return "No parking lots found."

    for lot in lots:
        print(f"🚗 Processing email reminders for lot: {lot.prime_location_name}")
        # Run synchronously so one finishes before next begins
        send_gmail_daily_reminder.apply(args=(lot.id,))
        print(f"✅ Completed sending emails lot: {lot.id}")

    return f"✅ Sequentially processed {len(lots)} parking lots."


# send reminder sms to users who haven't visited a specific parking lot
@celery.task
def send_sms_daily_reminder(parking_lot_id: int):
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
        send_sms_message(message) 
    return f"✅ Sent reminders to {len(users_without_reservation)} users for lot {parking_lot_id}."


@celery.task
def send_sms_daily_reminders_for_all_lots():
    """
    Runs once daily.
    Iterates through parking lots and calls each reminder task sequentially.
    """
    lots = Parking_Lot.query.all()
    if not lots:
        return "No parking lots found."

    for lot in lots:
        print(f"🚗 Processing SMS reminders for lot: {lot.prime_location_name}")
        # Run synchronously so one finishes before next begins
        send_sms_daily_reminder.apply(args=(lot.id,))
        print(f"✅ Completed lot: {lot.id}")

    return f"✅ Sequentially processed {len(lots)} parking lots."
