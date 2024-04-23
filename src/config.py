import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "voicevox_speaker_id": 47
    }