import openai
import os
from config import set_vars
set_vars()
openai.api_key = os.environ.get('OPENAI_API_KEY')
def generate_message(name, tone="gentle"):

    prompt = f"""
    You're an empathetic life coach calling {name}, who is feeling low.
    Give a 30-second {tone} motivational good morning message encouraging them to get out of bed and take control of their lives. Emphasize how in control of their lives they really are.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_message_for_conversation(tone="gentle", user_input=""):
    prompt = f"""
    You're an empathetic, yet constructive life coach calling a person, who is feeling low.
    Provide a 1-3 sentences response to the user and their story, almost like a human friend would.
    Always end with a question to the user to continue the conversation.
    User's story: {user_input}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()