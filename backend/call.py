from twilio.rest import Client
import os
# from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH_TOKEN"])

def make_call(to_number, audio_url):
    call = client.calls.create(
        to=to_number,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        twiml=f'<Response><Play>{audio_url}</Play></Response>'
    )
    return call.sid
