import requests
from config import OPENAI_API_KEY

def synthesize_voice(text, filename="audio.mp3"):
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"model": "tts-1", "input": text, "voice": "nova"},
    )
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename
