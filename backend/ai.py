import openai
from config import OPENAI_API_KEY



def generate_message(name, tone="gentle"):
    openai.api_key = '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'
    prompt = f"""
    You're an empathetic life coach calling {name}, who is feeling low.
    Give a 60-second {tone} motivational message encouraging them to get out of bed.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
