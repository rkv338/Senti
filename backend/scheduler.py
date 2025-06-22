from apscheduler.schedulers.background import BackgroundScheduler
from ai import generate_message
import logging
import boto3
import os
import uuid
logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()
import redis
import json
import datetime
import ssl
import time

def test_valkey_connection():
    r = redis.Redis(host='localhost', port=6379, ssl=True, ssl_cert_reqs=None, decode_responses=True)
    return r if r.ping() else None

def schedule_call(name, phone, hour, minute, tone, audio_url_func):
    # connect_to_valkey()
    connection = test_valkey_connection()
    if connection:

        # text = generate_message(name, tone)
        scheduled_time = datetime.datetime.now()
        # create a json with the necessary info to make a outbound call
        call_job = {
            'user_name': name,
            'phone_number': phone,
            'tone_of_call': tone
            # 'script': text
        }
        connection.zadd("scheduled_calls", {json.dumps(call_job): int(scheduled_time.strftime('%Y%m%d'))})
        logger.info("scheduled call in valkey instance")
        logger.info(connection.zrange('scheduled_calls', 0, -1))
    else:
        logger.error("connection to valkey instance failed")  
    # job_json = json.dumps(call_job, default=str)
    # score = int(scheduled_time.timestamp())
    # logger.info('figured out the score')
    # redis_client.zadd('scheduled_calls', {job_json: score})
    # logger.info('sent it off to redis')
    # print('Scheduled call')
    # # call_with_script(text, phone)
    # logger.info(scheduled_time)
    # logger.info(f"In Scheduler:Text generated and job scheduled")
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