from apscheduler.schedulers.background import BackgroundScheduler
from ai import generate_message
from tts import synthesize_voice
from call import make_call
import logging
logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

def schedule_call(name, phone, hour, minute, tone, audio_url_func):
    # text = generate_message(name, tone)
    text = generate_message(name, tone)
    logger.info(f"In Scheduler:Text generated")
    audio_file = synthesize_voice(text, filename=f"{name}.mp3")
    logger.info(f"In Scheduler:Audio file generated")
    url = audio_url_func(audio_file)
    logger.info(f"In Scheduler:Audio file url: {url}")
    logger.info(f"In Scheduler:Audio file uploaded to S3")
    make_call(phone, url)
    # logger.info(f"In Scheduler:Text: {text}")
    # def job():
    #     text = generate_message(name, tone)
    #     audio_file = synthesize_voice(text)
    #     url = audio_url_func(audio_file)
    #     make_call(phone, url)
    # logger.info(f"In Scheduler:Scheduling call for {name} at {hour}:{minute}")
    # scheduler.add_job(job, 'cron', hour=int(hour), minute=int(minute))
    # scheduler.start()
