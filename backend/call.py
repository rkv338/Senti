from twilio.rest import Client
from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def make_call(to_number, audio_url):
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_PHONE_NUMBER,
        twiml=f'<Response><Play>{audio_url}</Play></Response>'
    )
    return call.sid
