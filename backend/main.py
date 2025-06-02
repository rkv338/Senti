from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from scheduler import schedule_call
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

def dummy_upload(file_path):
    # For dev use local tunnel like ngrok to serve this file
    return f"https://your-host.com/audio/{file_path}"

@app.post("/schedule")
def schedule(form: dict):
    logger.info(f"Received form data: {form["name"]}")
    schedule_call(form["name"], form["phone"], form["hour"], form["minute"], form["tone"], dummy_upload)
    return {"status": "scheduled"}
