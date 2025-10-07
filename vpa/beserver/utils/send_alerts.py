import os
import requests
import dotenv
import logging

dotenv.load_dotenv()  # Load .env file if present   

logger = logging.getLogger(__name__)


def send_gchat_message(text: str, webhook_url: str | None = None) -> bool:
    """
    Send a message to a Google Chat space via webhook.
    """
    webhook_url = webhook_url or os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ GChat webhook URL not configured.")
        return False

    headers = {"Content-Type": "application/json; charset=UTF-8"}
    payload = {"text": text}

    try:
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ Sent message to GChat: {text}")
            return True
        else:
            print(f"❌ GChat error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"🚨 Error sending GChat message: {e}")
 
        return False


def send_gmail_message(to_email: str, subject: str, body: str) -> bool:
    """
    Send an email using the MailerSend API.
    """
    email_api_url = os.getenv("EMAIL_API_URL", "https://api.mailersend.com/v1/email")
    email_api_key = os.getenv("EMAIL_API_KEY")
    from_email = os.getenv("FROM_EMAIL_ADDRESS")
    print(f"Sending email to {to_email} from {from_email} via {email_api_url}")

    if not to_email:
        print("⚠️ No recipient email provided.")
        return False
    
    if not all([email_api_url, email_api_key, from_email]):
        print("⚠️ Email service not properly configured.")
        return False

    headers = {
        "Authorization": f"Bearer {email_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": {"email": from_email},   
        "to": [{"email": to_email}],     
        "subject": subject,
        "html": body                    
    }

    try:
        response = requests.post(email_api_url, json=payload, headers=headers, timeout=20)
        if response.status_code in [200, 202]:
            logger.info(f"✅ Sent email to {to_email}: {subject}")
            return True
        else:
            logger.error(f"❌ Email error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.exception(f"🚨 Error sending email: {e}")
        return False

    
def send_sms_message(to_number: str, message: str) -> bool: 
    """
    Send an SMS using a third-party SMS service.
    """
    sms_api_url = os.getenv("SMS_API_URL")
    sms_api_key = os.getenv("SMS_API_KEY")
    from_number = os.getenv("FROM_PHONE_NUMBER")

    if not all([sms_api_url, sms_api_key, from_number]):
        print("⚠️ SMS service not properly configured.")
        return False

    headers = {
        "Authorization": f"Bearer {sms_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": from_number,
        "to": to_number,
        "message": message
    }

    try:
        response = requests.post(sms_api_url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ Sent SMS to {to_number}: {message}")
            return True
        else:
            print(f"❌ SMS error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"🚨 Error sending SMS: {e}")
        return False
