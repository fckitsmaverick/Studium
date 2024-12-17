import os

from dotenv import load_dotenv

from elevenlabs import play
from elevenlabs.client import ElevenLabs
from elevenlabs import save

load_dotenv()

client = ElevenLabs(
    api_key= os.getenv("ELEVENLABS_API_KEY"),
)

def tts_chinese(text):
    audio = client.text_to_speech.convert(
        voice_id="C5PqzLlJWHbCvKBwbUU3",
        model_id="eleven_multilingual_v2",
        text=f"{text}",
    )
    save(audio, "speech.mp3")

