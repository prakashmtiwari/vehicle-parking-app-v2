import csv, os
from datetime import datetime
from vpa.beserver.scheduler.init_celery import celery
from vpa.beserver.extensions import db
from vpa.beserver.models import Reservation, User
from vpa.beserver.utils.send_alerts import send_gmail_message  #  Mailersend email function


EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


@celery.task(bind=True)
def export_parking_history(self, user_id):
    
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "User not found"}

    reservations = Reservation.query.filter_by(user_id=user_id).all()
    if not reservations:
        return {"message": "No reservations found."}

    file_name = f"parking_export_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.join(EXPORT_DIR, file_name)
    download_url = f"/static/exports/{file_name}"

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Reservation ID", "Lot ID", "Spot ID", "Vehicle", "Start Time", "End Time", "Amount Paid"])
        for r in reservations:
            writer.writerow([
                r.id, r.lot_id, r.spot_id, r.vehicle_number,
                r.parking_timestamp, r.leaving_timestamp, r.amount_paid or 0
            ])

    # Send an email with the download link
    subject = "Your Parking History Export is Ready 🚗"
    html_body = f"""
    <p>Hi {user.first_name or user.username},</p>
    <p>Your parking history export is complete. You can download your report using the link below:</p>
    <p><a href="{download_url}" target="_blank">Download CSV Report</a></p>
    <br>
    <p>Thanks,<br>Vehicle Parking App Team</p>
    """
    send_gmail_message(user.email, subject, html_body)

    return {"download_url": download_url}

   