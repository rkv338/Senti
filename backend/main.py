from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from scheduler import schedule_call, start_call_monitor, stop_call_monitor
import logging
import boto3
import os
from botocore.exceptions import ClientError
from config import set_vars
import atexit

set_vars()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = FastAPI(title="Senti - AI Life Coach", description="Conversational AI Life Coach System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Include Amazon Connect conversation routes
from connect_conversation_routes import router as connect_router
app.include_router(connect_router, prefix="/api", tags=["conversation"])


@app.on_event("startup")
async def startup_event():
    """Start the call monitor when the FastAPI app starts"""
    logger.info("Starting call monitor...")
    start_call_monitor()

@app.on_event("shutdown") 
async def shutdown_event():
    """Stop the call monitor when the FastAPI app shuts down"""
    logger.info("Stopping call monitor...")
    stop_call_monitor()

@app.post("/schedule")
def schedule(form: dict):
    logger.info(f"Received form data: {form}")
    
    # Extract timestamp from form data
    timestamp = form.get("timestamp")
    if not timestamp:
        return {"status": "error", "message": "Timestamp is required"}
    
    schedule_call(form["name"], form["phone"], form["tone"], timestamp)
    return {"status": "scheduled"}
