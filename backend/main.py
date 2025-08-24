from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from scheduler import schedule_call
import logging
import boto3
import os
from botocore.exceptions import ClientError
from config import set_vars

set_vars()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = FastAPI(title="RiseUp - AI Life Coach", description="Conversational AI Life Coach System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Include Amazon Connect conversation routes
from connect_conversation_routes import router as connect_router
app.include_router(connect_router, prefix="/api", tags=["conversation"])


@app.post("/schedule")
def schedule(form: dict):
    # logger.info(f"Received form data: {form["name"]}")
    schedule_call(form["name"], form["phone"], form["tone"])
    return {"status": "scheduled"}
