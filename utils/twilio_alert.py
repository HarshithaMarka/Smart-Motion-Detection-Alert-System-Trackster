import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_from = os.getenv("TWILIO_FROM")
twilio_to = os.getenv("TWILIO_TO")

client = Client(account_sid, auth_token)

def send_alert_with_image(image_url):
    try:
        client.messages.create(
            body="🚨 Motion detected! Screenshot attached.",
            from_=twilio_from,
            to=twilio_to,
            media_url=[image_url]
        )
        print("Alert sent successfully ✅")
    except Exception as e:
        print("Twilio Error:", e)
