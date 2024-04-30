import re
from .config import Config
from interpreter import interpreter

config = Config()

def translate(text: str) -> str:
    content = f"""
    Translate the text below to English. Only translate the text, do not include any other information.
    If the text is already in English, print the text as is.

    Example:
    Text: 私はメイドです 
    Output: I am a maid

    TEXT:
    {text}
    """

    return config.groq.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-70b-8192",
        stream=True,
    )
    
def chat(query: str) -> tuple[str, str]:
    interpreter.chat(query, display=False)
    jp = interpreter.messages[-1]['content']
    en = translate(jp)
    return jp, en