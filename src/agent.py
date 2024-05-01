import re
from .config import Config

config = Config()

def translate(text: str) -> str:
    content = f"""
    Translate all of the Japanese in the TEXT below to English. Leave all other text or code as is. Only translate the text, do not include any other information. Do NOT mention that it is a translation, simply provide the translated text.
    
    --------------------------------------------------

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

# make it easier for maid-chan to speak
def extract_japanese(text: str) -> str:
    japanese_pattern = r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]+'
    japanese_text = re.findall(japanese_pattern, text)
    return ''.join(japanese_text)

def chat(query: str) -> tuple[str, str]:
    config.interpreter.chat(query, display=False)
    jp = config.interpreter.messages[-1]['content']
    en = translate(jp)
    jp = extract_japanese(jp)
    return jp, en