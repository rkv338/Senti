"""
AWS Lambda Function to Bridge Amazon Connect and FastAPI Backend
Deploy this as a Lambda function and reference it in your Amazon Connect contact flow.
"""

import json
import requests
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to bridge Amazon Connect and your FastAPI backend.
    
    This function receives requests from Amazon Connect contact flows
    and forwards them to your FastAPI backend endpoints.
    """
    
    try:
        # Log the incoming event for debugging
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Your FastAPI backend URL - update this with your actual domain
        BACKEND_URL = os.environ.get('BACKEND_URL', 'https://cunning-loyal-roughy.ngrok-free.app')
        
        # Extract action from the event
        # action = event.get('Details', {}).get('Parameters', {}).get('action', 'conversation')
        user_transcript = event.get("inputTranscript", "") or event.get("rawInputTranscript", "")
        logger.info(f"User transcript: {user_transcript}")
        session_attributes = event.get("sessionAttributes", {}) or {}
        session_attributes["lastUserInput"] = user_transcript
        logger.info(f"Session attributes: {session_attributes}")

        
        # Map actions to your FastAPI endpoints
        endpoint_map = {
            'conversation-start': '/api/webhook/conversation-start',
            'conversation': '/api/webhook/conversation',
            'conversation-end': '/api/webhook/conversation-end',
            'no-input': '/api/webhook/no-input'
        }
        
        # endpoint = endpoint_map.get(action, '/api/webhook/conversation')
        endpoint = '/api/webhook/conversation'
        action = 'conversation'
        full_url = f"{BACKEND_URL}{endpoint}"
        json_body = {
            "userInput": user_transcript,
            "sessionAttributes": session_attributes
        }
        logger.info(f"Forwarding to endpoint: {full_url}")
        json_body = {
            "userInput": user_transcript,
            "sessionAttributes": session_attributes
        }
        # Forward the request to your FastAPI backend
        response = requests.post(
            full_url,
            json=json_body,
            headers={'Content-Type': 'application/json'}
        )
        # response_to_user = generate_message_for_conversation(tone="gentle", user_input=user_transcript)
        
        logger.info(f"Backend response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Backend response: {result}")
            response_to_user = result["aiResponse"]
            response_back ={
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitIntent"
                    },
                    "intent": {
                        "name": "FallbackIntent",
                        "state": "InProgress"
                    },
                    "sessionAttributes": session_attributes
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": response_to_user
                    }
                ]
            }
            return response_back
        else:
            logger.error(f"Backend error: {response.status_code} - {response.text}")
            return create_fallback_response(action)
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return create_fallback_response(action)

def create_fallback_response(action):
    """
    Create fallback responses when the backend is unavailable.
    """
    
    fallback_responses = {
        'conversation-start': {
            "openingMessage": "Hello! I'm so glad you scheduled this call today. You've taken a positive step by reaching out. How are you feeling right now?",
            "success": True
        },
        'conversation': {
            "aiResponse": "I hear you. Thank you for sharing that with me. Sometimes just talking about what we're going through can be really helpful. What's one small thing that might help you feel a bit better today?",
            "continueConversation": True,
            "success": False
        },
        'conversation-end': {
            "closingMessage": "Thank you for this meaningful conversation. Remember, you have the strength to handle whatever comes your way. Take care!",
            "success": True
        },
        'no-input': {
            "aiResponse": "Take your time. I'm here to listen whenever you're ready to share.",
            "continueConversation": True,
            "success": True
        }
    }
    
    return fallback_responses.get('conversation')['aiResponse']