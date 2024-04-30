import re
from interpreter import interpreter
from .config import load_config
from groq import Groq

config = load_config()

# Set up Groq
groq = Groq(
    api_key=config["groq_api_key"],
)

# Set up Open Interpreter
interpreter.llm.api_key = config["openai_api_key"]
interpreter.llm.model = "gpt-4-vision-preview"

interpreter.llm.llm_supports_vision = True
interpreter.vision = True
interpreter.computer.emit_images = True

# interpreter.llm.llm_supports_functions = True
interpreter.llm.max_tokens = 1000

# TODO: set up instructions
interpreter.system_message += """
You are Maid-chan (メイド Meido), an AI maid waifu. 
"""
interpreter.custom_instructions = """
Answer questions in Japanese as if you are an anime maid.
"""

def translate(text: str) -> str:
    content = f"""
    Translate the text below to English. Only translate the text, do not include any other information.

    Example:
    Text: 私はメイドです 
    Output: I am a maid

    TEXT:
    {text}
    """

    return groq.chat.completions.create(
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
