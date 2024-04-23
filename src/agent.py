import re
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
Answer questions in Japanese and English in the following format:

Example:
[[JA]]
こんにちは
[[EN]]
Hello
"""

def extract(text: str) -> tuple:
    match = re.search(r'\[\[JA\]\](.*?)\[\[EN\]\](.*)', text, re.DOTALL)
    if match:
        japanese_text = match.group(1).strip()
        english_text = match.group(2).strip()
        return japanese_text, english_text
    return "", ""

def chat(query: str) -> str:
    interpreter.chat(query, display=False)
    response = interpreter.messages[-1]['content']
    jp, en = extract(response)
    return jp, en
