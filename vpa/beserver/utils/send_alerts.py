import os
import requests

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