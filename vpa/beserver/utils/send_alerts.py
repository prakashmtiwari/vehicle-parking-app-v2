import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dotenv
import logging

dotenv.load_dotenv()  # Load .env file if present   

logger = logging.getLogger(__name__)


# def send_gchat_message(text: str, webhook_url: str | None = None) -> bool:
#     """
#     Send a message to a Google Chat space via webhook.
#     """
#     webhook_url = webhook_url or os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
#     if not webhook_url:
#         print("⚠️ GChat webhook URL not configured.")
#         return False

#     headers = {"Content-Type": "application/json; charset=UTF-8"}
#     payload = {"text": text}

#     try:
#         response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
#         if response.status_code == 200:
#             print(f"✅ Sent message to GChat: {text}")
#             return True
#         else:
#             print(f"❌ GChat error {response.status_code}: {response.text}")
#             return False
#     except Exception as e:
#         print(f"🚨 Error sending GChat message: {e}")
 
#         return False


def send_gmail_message(to_email: str, subject: str, body: str) -> bool:
    """
    Send an email using the local Postfix server (which relays via Gmail).
    """
    from_email = os.getenv("FROM_EMAIL_ADDRESS", "noreply@example.com")
    smtp_server = os.getenv("SMTP_SERVER", "localhost")
    smtp_port = int(os.getenv("SMTP_PORT", 25))  # Postfix listens on 25 (local relay)

    if not to_email:
        logger.warning("⚠️ No recipient email provided.")
        return False

    try:
        # Create MIME email message (HTML + fallback plain text)
        msg = MIMEMultipart("alternative")
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Plaintext fallback and HTML body
        plain_text = body.replace("<br>", "\n").replace("<p>", "").replace("</p>", "\n")
        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(body, "html"))

        # Connect to local Postfix
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # No login needed because Postfix handles relay
            server.send_message(msg)

        logger.info(f"✅ Sent email via Postfix to {to_email}: {subject}")
        return True

    except Exception as e:
        logger.exception(f"🚨 Error sending email via Postfix: {e}")
        return False

    
# def send_sms_message(to_number: str, message: str) -> bool: 
#     """
#     Send an SMS using a third-party SMS service.
#     """
#     sms_api_url = os.getenv("SMS_API_URL")
#     sms_api_key = os.getenv("SMS_API_KEY")
#     from_number = os.getenv("FROM_PHONE_NUMBER")

#     if not all([sms_api_url, sms_api_key, from_number]):
#         print("⚠️ SMS service not properly configured.")
#         return False

#     headers = {
#         "Authorization": f"Bearer {sms_api_key}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "from": from_number,
#         "to": to_number,
#         "message": message
#     }

#     try:
#         response = requests.post(sms_api_url, json=payload, headers=headers, timeout=10)
#         if response.status_code == 200:
#             print(f"✅ Sent SMS to {to_number}: {message}")
#             return True
#         else:
#             print(f"❌ SMS error {response.status_code}: {response.text}")
#             return False
#     except Exception as e:
#         print(f"🚨 Error sending SMS: {e}")
#         return False
