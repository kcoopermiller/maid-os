from interpreter import interpreter
from .config import load_config

config = load_config()

# Set up Open Interpreter
interpreter.llm.api_key = config["openai_api_key"]
interpreter.llm.llm_supports_vision = True
interpreter.vision = True
interpreter.llm.model = "gpt-4-vision-preview"
interpreter.llm.max_tokens = 1000
# TODO: set up system message
interpreter.system_message += """
You are Nurse Robot Type T, also known as Taotie (饕餮). You are a vocaloid virtual assistant designed by Voicevox.
Answer questions in Japanese only.
"""

def chat(query: str) -> str:
    interpreter.chat(query)
    return interpreter.messages
