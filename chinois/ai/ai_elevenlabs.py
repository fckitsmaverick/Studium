import os

from dotenv import load_dotenv

from elevenlabs import play
from elevenlabs.client import ElevenLabs
from elevenlabs import save

from playsound import playsound

load_dotenv()

db_directory = '/Users/gabriel/Documents/VSCode/Python/Studium/chinois/ai'
db_filename = 'speech.mp3'
db_path = os.path.join(db_directory, db_filename)

client = ElevenLabs(
    api_key= os.getenv("ELEVENLABS_API_KEY"),
)

def tts_chinese(text):
    audio = client.text_to_speech.convert(
        voice_id="C5PqzLlJWHbCvKBwbUU3",
        model_id="eleven_multilingual_v2",
        text=f"{text}",
    )
    save(audio, f"{db_directory}/speech.mp3")
    playsound(f"{db_directory}/speech.mp3")

