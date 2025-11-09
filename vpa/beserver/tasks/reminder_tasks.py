from vpa.beserver.scheduler.init_celery import celery
from vpa.beserver.extensions import db
from vpa.beserver.models import User, Reservation, Parking_Spot, Parking_Lot
from vpa.beserver.utils.send_alerts import send_gmail_message

import logging

logger = logging.getLogger(__name__)

# #task to send gchat reminders to users who haven't visited a specific parking lot
# @celery.task
# def send_gchat_daily_reminder(parking_lot_id: int):
#     """
#     Send reminder to users who haven't visited (made reservation) in a specific parking lot.
#     """
#     users_with_reservation = (
#         db.session.query(User.id)
#         .join(Reservation)
#         .join(Parking_Spot)
#         .filter(Parking_Spot.lot_id == parking_lot_id)
#         .distinct()
#         .all()
#     )
#     users_with_reservation_ids = [u.id for u in users_with_reservation]

#     users_without_reservation = (
#         db.session.query(User)
#         .filter(User.active == True)
#         .filter(~User.id.in_(users_with_reservation_ids))
#         .all()
#     )

#     if not users_without_reservation:
#         return f"All users have already visited lot {parking_lot_id}."

#     lot = Parking_Lot.query.get(parking_lot_id)
#     for user in users_without_reservation:
#         if user.username == "admin":
#             continue  # Skip admin users
#         message = (
#             f"👋 Hi {user.first_name or user.username},\n\n"
#             f"A new parking lot is available: **{lot.prime_location_name}** 🚗\n"
#             f"You haven’t booked a spot here yet!\n\n"
#             f"👉 [Click here to view and reserve a spot]("
#             f"http://localhost:5173/parking-lot-list"
#             f")"
#         )
#         send_gchat_message(message)

#     return f"✅ Sent reminders to {len(users_without_reservation)} users for lot {parking_lot_id}."




# #task to send gmail reminders to users who haven't visited a specific parking lot
# @celery.task
# def send_gmail_daily_reminder(parking_lot_id: int):
#         """
#         Notify a user when a new parking lot is available.
#         """
#         lot = Parking_Lot.query.get(parking_lot_id)
#         if not lot:
#             return f"Parking lot with ID {parking_lot_id} not found."

#         users_with_reservation = (
#         db.session.query(User.id)
#         .join(Reservation)
#         .join(Parking_Spot)
#         .filter(Parking_Spot.lot_id == parking_lot_id)
#         .distinct()
#         .all()
#         )
#         users_with_reservation_ids = [u.id for u in users_with_reservation]

#         users_without_reservation = (
#             db.session.query(User)
#             .filter(User.active == True)
#             .filter(~User.id.in_(users_with_reservation_ids))
#             .all()
#         )

#         if not users_without_reservation:
#            return f"All users have already visited lot {parking_lot_id}."

        
#         subject = f"🚗 New Parking Lot Available: {lot.prime_location_name}"


#         for user in users_without_reservation:
#             if user.username == "admin" or not user.email:
#                 continue  # Skip admin users and users without email

#          # Craft a simple HTML email body

#             body = f"""
#             <html>
#                 <body style="font-family: Arial, sans-serif; color: #333;">
#                     <p>👋 Hi {user.first_name or user.username},</p>

#                     <p>A new parking lot is now available: 
#                     <strong>{lot.prime_location_name}</strong> 🚗</p>

#                     <p>You haven’t booked a spot here yet — don’t miss out!</p>

#                     <p>
#                         👉 <a href="http://localhost:5173/parking-lot-list" 
#                             style="background-color:#007bff; color:white; padding:10px 15px; text-decoration:none; border-radius:6px;">
#                             View and Reserve a Spot
#                         </a>
#                     </p>

#                     <br>
#                     <p>Best,<br>The Parking Assistant Team</p>
#                 </body>
#             </html>
#             """

#             send_gmail_message(
#                 to_email=user.email,
#                 subject=subject,
#                 body=body
#             )

#         return f"✅ Sent email to {len(users_without_reservation)} users for lot {parking_lot_id}."



@celery.task
def send_gmail_daily_reminders_for_all_lots():
    """
    Send reminder emails to active users who haven't visited certain parking lots.
    If only one new parking lot is unvisited, send a single-lot email.
    If multiple lots are unvisited, send a multi-lot email.
    """

    # Fetch all active parking lots
    all_lots = Parking_Lot.query.all()
    if not all_lots:
        return "⚠️ No parking lots found in the system."

    # Fetch all active users
    active_users = db.session.query(User).filter(User.active == True).all()
    if not active_users:
        return "⚠️ No active users found."

    total_sent = 0
    total_users = 0

    # Iterate over each active user
    for user in active_users:
        if user.username == "admin" or not user.email:
            continue  # Skip admins or users without email

        total_users += 1

        # Find lots this user has already visited (through reservations)
        visited_lot_ids = (
            db.session.query(Parking_Spot.lot_id)
            .join(Reservation)
            .filter(Reservation.user_id == user.id)
            .distinct()
            .all()
        )
        visited_lot_ids = [lot_id for (lot_id,) in visited_lot_ids]

        # Determine which lots the user hasn't visited yet
        unvisited_lots = [lot for lot in all_lots if lot.id not in visited_lot_ids]

        # Skip if user has already visited all lots
        if not unvisited_lots:
            continue

        # Conditional subject and email body
        if len(unvisited_lots) == 1:
            lot = unvisited_lots[0]
            subject = f"🚗 New Parking Lot Available: {lot.prime_location_name}"
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <p>👋 Hi {user.first_name or user.username},</p>

                    <p>A new parking lot is now available at 
                    <strong>{lot.prime_location_name}</strong> 🚗</p>

                    <p>You haven’t booked a spot here yet — don’t miss out!</p>

                    <p>
                        👉 <a href="http://localhost:5173/login" 
                            style="background-color:#007bff; color:white; padding:10px 15px; text-decoration:none; border-radius:6px;">
                            View and Reserve a Spot
                        </a>
                    </p>

                    <br>
                    <p>Best,<br>The Parking Assistant Team</p>
                </body>
            </html>
            """
        else:
            subject = f"🅿️ {len(unvisited_lots)} New Parking Lots Waiting for You!"
            lot_list_html = "".join(
                f"<li><strong>{lot.prime_location_name}</strong> — {lot.address or 'View details online'}</li>"
                for lot in unvisited_lots
            )

            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <p>👋 Hi {user.first_name or user.username},</p>

                    <p>You’ve got <strong>{len(unvisited_lots)}</strong> parking lots you haven’t explored yet:</p>
                    <ul>
                        {lot_list_html}
                    </ul>

                    <p>Find a convenient spot now before it fills up!</p>

                    <p>
                        👉 <a href="http://localhost:5173/parking-lot-list"
                            style="background-color:#28a745; color:white; padding:10px 15px; text-decoration:none; border-radius:6px;">
                            Explore Parking Lots
                        </a>
                    </p>

                    <br>
                    <p>Best,<br>The Parking Assistant Team</p>
                </body>
            </html>
            """

        # Send email via Postfix relay
        if send_gmail_message(to_email=user.email, subject=subject, body=body):
            total_sent += 1

    return f"✅ Sent {total_sent} reminder emails out of {total_users} active users."



# # send reminder sms to users who haven't visited a specific parking lot
# @celery.task
# def send_sms_daily_reminder(parking_lot_id: int):
#     """
#     Send reminder to users who haven't visited (made reservation) in a specific parking lot.
#     """
#     users_with_reservation = (
#         db.session.query(User.id)
#         .join(Reservation)
#         .join(Parking_Spot)
#         .filter(Parking_Spot.lot_id == parking_lot_id)
#         .distinct()
#         .all()
#     )
#     users_with_reservation_ids = [u.id for u in users_with_reservation]     

#     users_without_reservation = (
#         db.session.query(User)
#         .filter(User.active == True)
#         .filter(~User.id.in_(users_with_reservation_ids))
#         .all()
#     )

#     if not users_without_reservation:
#         return f"All users have already visited lot {parking_lot_id}."
    
#     lot = Parking_Lot.query.get(parking_lot_id)
#     for user in users_without_reservation:      
#         if user.username == "admin":
#             continue  # Skip admin users
#         message = (
#             f"👋 Hi {user.first_name or user.username},\n\n"
#             f"A new parking lot is available: **{lot.prime_location_name}** 🚗\n"
#             f"You haven’t booked a spot here yet!\n\n"
#             f"👉 [Click here to view and reserve a spot]("
#             f"http://localhost:5173/parking-lot-list"
#             f")"
#         )
#         send_sms_message(message) 
#     return f"✅ Sent reminders to {len(users_without_reservation)} users for lot {parking_lot_id}."

