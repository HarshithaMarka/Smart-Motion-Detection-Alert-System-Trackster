from twilio.rest import Client

client = Client(" TWILIO_ACCOUNT_SID", " TWILIO_AUTH_TOKEN")

def send_alert_with_image(image_url):
    client.messages.create(
        body="Motion detected! Screenshot attached.",
        from_="whatsapp: ",
        to="whatsapp:",
        media_url=[image_url]
    )
