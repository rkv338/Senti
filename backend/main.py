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
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

def upload_to_s3(file_path):
    # For dev use local tunnel like ngrok to serve this file
    session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"]
    )
    s3 = session.client('s3')
    s3.upload_file(file_path, 
                   os.environ["S3_BUCKET_NAME"], 
                   f"audio/{os.path.basename(file_path)}")
    logger.info(f"Uploaded file to S3: {file_path}")
    # generate presigned url
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': os.environ["S3_BUCKET_NAME"],
            'Key': f"audio/{os.path.basename(file_path)}"
        },
        ExpiresIn=1800
    )
    return presigned_url
    

@app.post("/schedule")
def schedule(form: dict):
    # logger.info(f"Received form data: {form["name"]}")
    schedule_call(form["name"], form["phone"], form["hour"], form["minute"], form["tone"], upload_to_s3)
    return {"status": "scheduled"}
