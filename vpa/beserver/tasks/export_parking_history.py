import csv, os
from datetime import datetime
from vpa.beserver.scheduler.init_celery import celery
from vpa.beserver.extensions import db
from vpa.beserver.models import Reservation, User
from vpa.beserver.utils.send_alerts import send_gmail_message  #  Mailersend email function


EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")


@celery.task
def export_parking_history(user_id):
    os.makedirs(EXPORT_DIR, exist_ok=True)

    user = User.query.get(user_id)
    print(user.email, user_id)

    # Fetch data
    reservations = (
        db.session.query(Reservation)
        .filter(Reservation.user_id == user_id)
        .order_by(Reservation.parking_timestamp)
        .all()
    )

    if not reservations:
        send_gmail_message(
            to_email="user@example.com",
            subject="Your Parking Export",
            body="<p>No parking history found.</p>"
        )
        return

    # Prepare CSV
    file_name = f"parking_export_user_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.join(EXPORT_DIR, file_name)

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Reservation ID", "Lot Location", "Spot ID", "Vehicle", "Start Time", "End Time", "Amount Paid"])

        for r in reservations:
            writer.writerow([
                r.id, r.lot_id, r.spot_id, r.vehicle_number,
                r.parking_timestamp, r.leaving_timestamp, r.amount_paid or 0
            ])

    # Send email or dashboard notification
    send_gmail_message(
        to_email=user.email,
        subject="✅ Your Parking History Export is Ready",
        body=f"<p>Your parking history is complete. Download it here:</p><p><a href='http://localhost:5000/{file_path}'>Download CSV</a></p>"
    )
