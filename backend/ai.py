import openai
from config import set_vars
import os



def generate_message(name, tone="gentle"):
    set_vars()
    
    openai.api_key = os.environ["OPENAI_API_KEY"]
    prompt = f"""
    You're an empathetic life coach calling {name}, who is feeling low.
    Give a 60-second {tone} motivational good morning message encouraging them to get out of bed and take control of their lives. Emphasize how in control of their lives they really are.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
