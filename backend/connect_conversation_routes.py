"""
Amazon Connect Conversation Routes
These endpoints handle webhook calls from Amazon Connect for two-way conversations.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
import json
from conversation_handler import conversation_handler
from typing import Dict, Any
from ai import generate_message_for_conversation

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/webhook/conversation")
async def handle_conversation_webhook(request: Request):
    """
    Main webhook endpoint for Amazon Connect conversation processing.
    
    Amazon Connect will send user speech-to-text here, and we'll return
    the AI response for text-to-speech.
    """
    try:
        # Parse the incoming request from Amazon Connect
        body = await request.json()
        logger.info(f"Received conversation webhook: {body}")
        
        user_input = body.get("userInput", "hi this is a fake input")
        print(f"session attributes: {body.get('sessionAttributes', {})}")
        # Extract key information from Amazon Connect
        
        # Handle empty or no input
        if not user_input or user_input.strip() == "":
            response_text = "I didn't catch that. Could you please repeat what you'd like to talk about?"
        # else:
            # Generate AI response
            # response_text = conversation_handler.generate_empathetic_response(
            #     user_input=user_input.strip(),
            #     contact_id=contact_id,
            #     user_name=user_name
            # )
        response_text = generate_message_for_conversation(tone="gentle", user_input=user_input)
        
        # Return response in format expected by Amazon Connect
        return {
            "aiResponse": response_text
            # "aiResponse": response_text
        }
        
    except Exception as e:
        logger.error(f"Error in conversation webhook: {e}")
        return {
            "aiResponse": "I'm having a small technical difficulty. Let's take a moment and try again.",
            "continueConversation": True,
            "success": False
        }

# @router.post("/webhook/conversation-start")
# async def handle_conversation_start(request: Request):
#     """
#     Webhook called when a conversation starts.
#     Sets up the initial conversation context.
#     """
#     try:
#         body = await request.json()
#         logger.info(f"Conversation started: {body}")
        
#         contact_id = body.get("Details", {}).get("ContactData", {}).get("ContactId", "unknown")
#         user_name = body.get("Details", {}).get("Parameters", {}).get("userName", "friend")
#         tone = body.get("Details", {}).get("Parameters", {}).get("tone", "gentle")
        
#         # Generate initial greeting with motivational message
#         initial_prompt = f"""
#         You're starting a phone conversation with {user_name} who scheduled a motivational call. 
#         The tone should be {tone}. Start with a warm greeting, deliver a brief motivational message, 
#         then ask how they're doing today to begin the conversation. Keep it under 30 seconds when spoken.
#         """
        
#         # Use OpenAI to generate the opening
#         from openai import OpenAI
#         client = OpenAI()
        
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[{"role": "user", "content": initial_prompt}],
#             max_tokens=150,
#             temperature=0.7
#         )
        
#         opening_message = response.choices[0].message.content.strip()
        
#         # Store the opening in conversation memory
#         conversation_handler.add_to_conversation(contact_id, "assistant", opening_message)
        
#         return {
#             "openingMessage": opening_message,
#             "success": True
#         }
        
#     except Exception as e:
#         logger.error(f"Error in conversation start: {e}")
#         # Fallback opening message
#         return {
#             "openingMessage": f"Hello {user_name}! I'm so glad you scheduled this call today. You've taken a positive step by reaching out, and that shows real strength. How are you feeling right now?",
#             "success": True
#         }

# @router.post("/webhook/conversation-end")
# async def handle_conversation_end(request: Request):
#     """
#     Webhook called when conversation ends.
#     Cleans up conversation memory and provides closing message.
#     """
#     try:
#         body = await request.json()
#         contact_id = body.get("Details", {}).get("ContactData", {}).get("ContactId", "unknown")
        
#         # Generate closing message
#         closing_message = conversation_handler.end_conversation(contact_id)
        
#         # Clean up conversation memory
#         conversation_handler.cleanup_conversation(contact_id)
        
#         logger.info(f"Conversation ended for contact: {contact_id}")
        
#         return {
#             "closingMessage": closing_message,
#             "success": True
#         }
        
#     except Exception as e:
#         logger.error(f"Error in conversation end: {e}")
#         return {
#             "closingMessage": "Thank you for this conversation. Take care!",
#             "success": True
#         }

# @router.post("/webhook/no-input")
# async def handle_no_input(request: Request):
#     """
#     Webhook called when user doesn't provide input (silence).
#     """
#     try:
#         body = await request.json()
#         user_name = body.get("Details", {}).get("Parameters", {}).get("userName", "friend")
        
#         responses = [
#             f"Take your time, {user_name}. I'm here to listen whenever you're ready to share.",
#             f"No pressure, {user_name}. Sometimes it's good to just take a moment to breathe.",
#             f"I'm still here with you, {user_name}. What's on your mind today?"
#         ]
        
#         # You could make this more sophisticated by tracking how many times this happens
#         import random
#         response_text = random.choice(responses)
        
#         return {
#             "aiResponse": response_text,
#             "continueConversation": True,
#             "success": True
#         }
        
#     except Exception as e:
#         logger.error(f"Error handling no input: {e}")
#         return {
#             "aiResponse": "I'm here when you're ready to talk.",
#             "continueConversation": True,
#             "success": True
#         }

@router.get("/webhook/health")
async def webhook_health_check():
    """Health check endpoint for Amazon Connect webhooks."""
    return {"status": "healthy", "service": "conversation_webhooks"}

# Optional: Endpoint to test conversation without Amazon Connect
# @router.post("/test/conversation")
# async def test_conversation(request: Request):
#     """Test endpoint for conversation without Amazon Connect."""
#     try:
#         body = await request.json()
#         user_input = body.get("message", "")
#         user_name = body.get("name", "friend")
#         contact_id = body.get("contact_id", "test_123")
        
#         response_text = conversation_handler.generate_empathetic_response(
#             user_input=user_input,
#             contact_id=contact_id,
#             user_name=user_name
#         )
        
#         return {
#             "response": response_text,
#             "success": True
#         }
        
#     except Exception as e:
#         logger.error(f"Error in test conversation: {e}")
#         return {"error": str(e), "success": False}
