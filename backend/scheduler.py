from apscheduler.schedulers.background import BackgroundScheduler
from ai import generate_message
from tts import synthesize_voice
from call import make_call
import logging
import boto3
import os
import uuid
logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

def schedule_call(name, phone, hour, minute, tone, audio_url_func):
    # text = generate_message(name, tone)
    text = generate_message(name, tone)
    call_with_script(text, phone, )
    logger.info(f"In Scheduler:Text generated")
    # audio_file = synthesize_voice(text, filename=f"{name}.mp3")
    # logger.info(f"In Scheduler:Audio file generated")
    # url = audio_url_func(audio_file)
    # logger.info(f"In Scheduler:Audio file url: {url}")
    # logger.info(f"In Scheduler:Audio file uploaded to S3")
    # make_call(phone, url)
    # logger.info(f"In Scheduler:Text: {text}")
    # def job():
    #     text = generate_message(name, tone)
    #     audio_file = synthesize_voice(text)
    #     url = audio_url_func(audio_file)
    #     make_call(phone, url)
    # logger.info(f"In Scheduler:Scheduling call for {name} at {hour}:{minute}")
    # scheduler.add_job(job, 'cron', hour=int(hour), minute=int(minute))
    # scheduler.start()
def call_with_script(script_text, phone_number):
    """
    Initiates an outbound call using Amazon Connect and passes in a script to be spoken via Amazon Polly.

    Parameters:
    - script_text (str): The message to be spoken in the call.
    - phone_number (str): The destination phone number in E.164 format (e.g., '+1234567890').
    - instance_id (str): The ID of your Amazon Connect instance.
    - contact_flow_id (str): The ID of the contact flow configured to use $.Attributes.ScriptText.
    - source_number (str): The outbound caller ID (must be claimed in Connect).
    """
    session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"]
    )
    connect_client = session.client('connect')

    # Add a random token to avoid caching if you're testing
    unique_script = f"{script_text} (ref: {uuid.uuid4().hex[:6]})"

    try:
        response = connect_client.start_outbound_voice_contact(
            DestinationPhoneNumber=phone_number,
            ContactFlowId=os.environ["CONTACT_FLOW_ID"],
            InstanceId=os.environ["INSTANCE_ID"],
            SourcePhoneNumber=os.environ["SOURCE_PHONE_NUMBER"],
            Attributes={
                'script': unique_script
            }
        )
        print(f"Call started successfully. Contact ID: {response['ContactId']}")
        return response['ContactId']

    except connect_client.exceptions.InvalidParameterException as e:
        print("Invalid parameters. Check your phone number or contact flow ID.")
        print(e)
    except Exception as e:
        print("An error occurred:", e)