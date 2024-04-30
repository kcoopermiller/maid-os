import os
from dotenv import load_dotenv
from interpreter import interpreter
from groq import Groq

class Config:
    def __init__(self):
        load_dotenv()
        self.voicevox_speaker_id = 47
        self.setup_interpreter()
        self.setup_groq()

    def setup_interpreter(self):
        interpreter.llm.api_key = os.getenv("OPENAI_API_KEY")
        interpreter.llm.model = "gpt-4-vision-preview"

        interpreter.llm.llm_supports_vision = True
        interpreter.vision = True
        interpreter.computer.emit_images = True
        interpreter.computer.verbose = True

        interpreter.llm.context_window = 128000
        interpreter.llm.max_tokens = 3000

        interpreter.system_message += """
        You are Maid-chan (メイド Meido), an AI maid waifu. 
        """
        interpreter.custom_instructions = """
        Answer questions in Japanese as if you are an anime maid.
        """

    def setup_groq(self):
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))