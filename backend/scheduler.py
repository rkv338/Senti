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

def connect_to_valkey():
    """Initialize connection to Valkey/Redis"""
    pass  # This function seems to be called but not defined

def test_valkey_connection():
    logger.info("Testing Valkey connection")
    r = redis.Redis(host='localhost', port=6379, ssl=True, ssl_cert_reqs=None, decode_responses=True)
    if not r.ping():
        logger.error("Valkey connection failed")
        return None
    else:
        logger.info("Valkey connection successful")
        return r
def fire_calls(redis_client):
    """Check Redis for scheduled calls and execute them if it's time"""
    now = int(time.time())

    # Get all calls due up to now
    jobs = redis_client.zrange('scheduled_calls', 0, -1, withscores=True)
    logger.info(f"Found {len(jobs)} scheduled calls")
    
    for job_json, scheduled_timestamp in jobs:
        try:
            job = json.loads(job_json)
            
            # Check if it's time for this call
            if scheduled_timestamp <= now:
                logger.info(f"Executing call for {job['user_name']} at {job['phone_number']} (scheduled for {job.get('scheduled_time', 'unknown time')})")
                
                # Execute the call
                call_with_script(job['script'], job['phone_number'])
                
                # Remove the completed job from Redis
                redis_client.zrem("scheduled_calls", job_json)
                logger.info(f"Call executed and removed from queue for {job['user_name']}")
            else:
                from datetime import datetime
                scheduled_dt = datetime.fromtimestamp(scheduled_timestamp)
                logger.info(f"Call for {job['user_name']} scheduled for later: {scheduled_dt} (current time: {datetime.fromtimestamp(now)})")
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse job JSON: {e}")
            # Remove malformed job
            redis_client.zrem("scheduled_calls", job_json)
        except Exception as e:
            logger.error(f"Error executing call: {e}")

def start_call_monitor():
    """Start the background scheduler to monitor Redis for scheduled calls"""
    redis_client = test_valkey_connection()
    if not redis_client:
        logger.error("Cannot start call monitor - Redis connection failed")
        return
    
    # Add job to check for calls every 30 seconds
    scheduler.add_job(
        func=lambda: fire_calls(redis_client),
        trigger="interval",
        seconds=60,
        id='call_monitor',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Call monitor started - checking for scheduled calls every 30 seconds")

def stop_call_monitor():
    """Stop the background scheduler"""
    scheduler.shutdown()
    logger.info("Call monitor stopped")
def schedule_call(name, phone, tone, timestamp):
    print("scheduling call")
    text = generate_message(name, tone)
    
    # Convert timestamp string to datetime object and then to Unix timestamp
    try:
        # Parse the datetime-local format from frontend (YYYY-MM-DDTHH:MM)
        from datetime import datetime
        scheduled_datetime = datetime.fromisoformat(timestamp)
        scheduled_timestamp = int(scheduled_datetime.timestamp())
        
        logger.info(f"Scheduling call for {name} at {scheduled_datetime} (timestamp: {scheduled_timestamp})")
        
    except ValueError as e:
        logger.error(f"Invalid timestamp format: {timestamp}, error: {e}")
        return
    
    connect_to_valkey()
    connection = test_valkey_connection()
    if connection:
        # Create a json with the necessary info to make an outbound call
        call_job = {
            'user_name': name,
            'phone_number': phone,
            'tone_of_call': tone,
            'script': text,
            'scheduled_time': timestamp,  # Keep original timestamp for reference
            'scheduled_timestamp': scheduled_timestamp  # Unix timestamp for easy comparison
        }
        
        # Use the Unix timestamp as the score for the sorted set
        connection.zadd("scheduled_calls", {json.dumps(call_job): scheduled_timestamp})
        logger.info(f"Scheduled call in valkey instance for {name} at {scheduled_datetime}")
        
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
    session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"]
    )
    connect_client = session.client('connect')

    # Add a random token to avoid caching if you're testing
    unique_script = f"{script_text}"

    try:
        logger.info("About to make the call")
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

# def call_with_conversation(user_name, phone_number, tone="gentle"):
#     """
#     Initiates an outbound call using Amazon Connect for two-way conversation.
    
#     Parameters:
#     - user_name (str): The user's name for personalization
#     - phone_number (str): The destination phone number in E.164 format (e.g., '+1234567890')
#     - tone (str): The tone for the conversation ('gentle', 'tough love', 'spiritual')
#     """
#     session = boto3.Session(
#         aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
#         aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
#         region_name=os.environ["AWS_REGION"]
#     )
#     connect_client = session.client('connect')

#     try:
#         logger.info(f"About to start conversation call for {user_name}")
        
#         # Use conversation contact flow instead of script-based flow
#         contact_flow_id = os.environ.get("CONVERSATION_CONTACT_FLOW_ID", os.environ["CONTACT_FLOW_ID"])
        
#         response = connect_client.start_outbound_voice_contact(
#             DestinationPhoneNumber=phone_number,
#             ContactFlowId=contact_flow_id,
#             InstanceId=os.environ["INSTANCE_ID"],
#             SourcePhoneNumber=os.environ["SOURCE_PHONE_NUMBER"],
#             Attributes={
#                 'userName': user_name,
#                 'tone': tone,
#                 'callType': 'conversation'
#             }
#         )
#         print(f"Conversation call started successfully. Contact ID: {response['ContactId']}")
#         logger.info(f"Conversation call started for {user_name}, Contact ID: {response['ContactId']}")
#         return response['ContactId']

#     except connect_client.exceptions.InvalidParameterException as e:
#         logger.error("Invalid parameters. Check your phone number or contact flow ID.")
#         logger.error(e)
#     except Exception as e:
#         logger.error(f"An error occurred starting conversation call: {e}")