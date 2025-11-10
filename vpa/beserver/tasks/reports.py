import os
import logging
from datetime import datetime, date, timedelta
from jinja2 import Template
from decimal import Decimal
from sqlalchemy import func, desc

from vpa.beserver.scheduler.init_celery import celery  # your Celery instance
from vpa.beserver.models import Reservation, Parking_Lot, User  # adjust imports to your models
from vpa.beserver.extensions import db
from vpa.beserver.utils.send_alerts import send_gmail_message
from vpa.beserver.app import app    


logger = logging.getLogger(__name__)

# --- Helper: Aggregation queries (SQLAlchemy examples) ---
def get_user_Reservations_for_month(user_id: int, year: int, month: int):
    """
    Return Reservations for the user in given month.
    Assumes Reservations has: id, user_id, lot_id, start_time, end_time, amount_paid
    """
    start = date(year, month, 1)
    # compute end as first day of next month
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    # using SQLAlchemy
    q = (
        db.session.query(Reservation)
        .filter(Reservation.user_id == user_id)
        .filter(Reservation.parking_timestamp >= start)
        .filter(Reservation.parking_timestamp < end)
    )
    # print(q.all())
    return q.all()


def get_user_monthly_stats(user_id: int, year: int, month: int):
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    # total Reservations
    total_Reservations = (
        db.session.query(Reservation).filter(Reservation.user_id == user_id)
        .filter(Reservation.parking_timestamp >= start).filter(Reservation.parking_timestamp < end)
        .count()
    )

    # total amount spent
    total_amount = (
        db.session.query(Reservation)
        .with_entities(func.coalesce(func.sum(Reservation.amount_paid), 0))
        .filter(Reservation.user_id == user_id)
        .filter(Reservation.parking_timestamp >= start).filter(Reservation.parking_timestamp < end)
        .scalar() or Decimal(0)
    )

    # most used parking lot
    most_used = (
        db.session.query(Reservation.lot_id, func.count(Reservation.id).label("cnt"))
        .filter(Reservation.user_id == user_id)
        .filter(Reservation.parking_timestamp >= start)
        .filter(Reservation.parking_timestamp < end)
        .group_by(Reservation.lot_id)
        .order_by(desc("cnt"))
        .limit(1)
        .first()
    )


    if most_used:
        lot = db.session.query(Parking_Lot).filter(Parking_Lot.id == most_used.lot_id).first()
        most_used_lot = {
            "id": lot.id if lot else None,
            "name": lot.prime_location_name if lot else None,
            "count": most_used.cnt
        }
    else:
        most_used_lot = None


    return {
        "user_id": user_id,
        "total_Reservations": total_Reservations,
        "total_amount": float(total_amount),
        "most_used_lot": most_used_lot
    }


# --- HTML Template (Jinja2 string) ---
REPORT_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Monthly Activity Report - {{ month_name }} {{ year }}</title>
  <style>
    body { font-family: Arial, sans-serif; color: #333; }
    .card { border: 1px solid #e2e2e2; padding: 16px; margin-bottom: 12px; border-radius: 6px; }
    h1 { color: #111; }
    table { width: 100%; border-collapse: collapse; margin-top: 8px;}
    th, td { text-align:left; padding:8px; border-bottom:1px solid #eee; }
  </style>
</head>
<body>
  <h1>Monthly Activity Report</h1>
  <p><strong>User:</strong> {{ user_name }} &nbsp; | &nbsp; <strong>Period:</strong> {{ month_name }} {{ year }}</p>

  <div class="card">
    <h2>Summary</h2>
    <p><strong>Total Reservations:</strong> {{ stats.total_Reservations }}</p>
    <p><strong>Total amount spent:</strong> ₹{{ "%.2f"|format(stats.total_amount) }}</p>
    {% if stats.most_used_lot %}
      <p><strong>Most used parking lot:</strong> {{ stats.most_used_lot.name }} with {{ stats.most_used_lot.count }} Reservations</p>
    {% else %}
      <p>No parking activity this month.</p>
    {% endif %}
  </div>

  <div class="card">
    <h2>All Reservations for the month</h2>
    {% if Reservations %}
      <table>
        <thead><tr><th>Date</th><th>Parking Lot</th><th>Parking Duration</th><th>Amount Paid</th></tr></thead>
        <tbody>
        {% for b in Reservations %}
          <tr>
            <td>{{ b.created_on.strftime("%Y-%m-%d %H:%M") }}</td>
            <td>{{ b.lot_name }}</td>
            <td>{{ b.duration }}</td>
            <td>₹{{ "%.2f"|format(b.amount_paid) }}</td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    {% else %}
      <p>No Reservations during this month.</p>
    {% endif %}
  </div>

  <footer>
    <p style="font-size:12px;color:#777">This is an automated report generated on {{ generated_on }}</p>
  </footer>
</body>
</html>
"""


# --- uses existing send_gmail_message ---


def send_email_via_api(to_email: str, subject: str, html_body: str) -> bool:

    try:
        response = send_gmail_message(to_email, subject, html_body)
        logger.info(f"Sent email via API to {to_email}, response: {response}")
        return True        
    
    except Exception as e:
        logger.exception("🚨 Exception while sending email: %s", e)
        return False


# # --- Alternative SMTP sender ---
# def send_email_via_smtp(to_email: str, subject: str, html_body: str) -> bool:
#     import smtplib
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText

#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT", "587"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_pass = os.getenv("SMTP_PASS")
#     from_email = os.getenv("FROM_EMAIL_ADDRESS")

#     if not all([smtp_host, smtp_user, smtp_pass, from_email]):
#         logger.error("SMTP not configured properly.")
#         return False

#     msg = MIMEMultipart("alternative")
#     msg["Subject"] = subject
#     msg["From"] = from_email
#     msg["To"] = to_email
#     part = MIMEText(html_body, "html")
#     msg.attach(part)

#     try:
#         server = smtplib.SMTP(smtp_host, smtp_port, timeout=20)
#         server.starttls()
#         server.login(smtp_user, smtp_pass)
#         server.sendmail(from_email, [to_email], msg.as_string())
#         server.quit()
#         logger.info("SMTP sent report to %s", to_email)
#         return True
#     except Exception:
#         logger.exception("SMTP send failed")
#         return False


# --- Report builder ---
def build_report_html(user, Reservations, stats, year, month):
    # enrich Reservations for template
    enriched = []
    for b in Reservations:
        lot = db.session.query(Parking_Lot).filter(Parking_Lot.id == b.lot_id).first()
        duration = ""

        if getattr(b, "parking_timestamp", None) and getattr(b, "leaving_timestamp", None):
            delta = b.leaving_timestamp - b.parking_timestamp
# Convert timedelta to hours, minutes, seconds
            total_seconds = int(delta.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            duration = f"{hours} hours {minutes} minutes {seconds} seconds"
            logger.info(f"Computed duration for reservation {b.id}: {duration}")

        enriched.append({
            "created_on": b.parking_timestamp,
            "lot_name": lot.prime_location_name if lot else "Unknown",
            "duration": duration if duration else "—",
            "amount_paid": float(getattr(b, "amount_paid", 0)) if getattr(b, "amount_paid", None) is not None else 0.0  
        })

    template = Template(REPORT_TEMPLATE)
    month_name = datetime(year, month, 1).strftime("%B")
    html = template.render(
        user_name=f"{user.first_name} {user.last_name}" if user else "User",
        month_name=month_name,
        year=year,
        Reservations=enriched,
        stats=stats,
        generated_on=datetime.now().strftime("%Y-%m-%d %H:%M IST"),
    )
    return html


# --- Celery task to create and send report to all users (or specific users) ---
@celery.task(bind=True, name="vpa.beserver.tasks.reports.send_monthly_activity_report")
def send_monthly_activity_report(self):
    """
    Runs on 1st of every month, sends activity report for the *previous month*.
    """
    logger.info("Starting monthly activity report job")
    # Determine the month to report on: previous month
    today = date.today()
    first_of_this_month = date(today.year, today.month, 1)
    # prev_month_last_day = first_of_this_month - timedelta(days=1)
    prev_month_last_day = first_of_this_month
    report_year = prev_month_last_day.year
    report_month = prev_month_last_day.month

    # get all users you want to send reports to
    users = db.session.query(User).filter(User.active == True).all()

    for user in users:
        if user.username == "admin":
            continue  # skip admin users    
        
        Reservations = get_user_Reservations_for_month(user.id, report_year, report_month)
        stats = get_user_monthly_stats(user.id, report_year, report_month)

        print(f"User {user.username} - Reservations: {len(Reservations)} - Stats: {stats}")
        if Reservations and stats:
            try:
                html = build_report_html(user, Reservations, stats, report_year, report_month)
                subject = f"Your Activity Report — {datetime(report_year, report_month, 1).strftime('%B %Y')}"
            
                sent = send_email_via_api(user.email, subject, html)
                print(f"Email sent to {user.email}: {sent}")

                #if not sent:
            #     send_email_via_smtp(user.email, subject, html)

                if sent:
                    logger.info("Monthly activity report sent to user %s", user.username)


            except Exception as e:
            # don't crash the whole job — log and continue
               logger.exception("Failed to build/send report for user %s: %s", user.username, e)
               continue    

        else:
            logger.info("No Reservations or stats for user %s, skipping report", user.username)



    logger.info("Monthly activity report job completed")




if __name__ == "__main__":
    today = date.today()
    first_of_this_month = date(today.year, today.month, 1)
    prev_month_last_day = first_of_this_month - timedelta(days=1)
    report_year = prev_month_last_day.year
    report_month = prev_month_last_day.month

    with app.app_context():
        users = db.session.query(User).filter(User.active == True).all()

    # for local testing
    
        for user in users:
            get_user_Reservations_for_month(user.id, report_year, report_month)