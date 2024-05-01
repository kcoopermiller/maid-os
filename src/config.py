import os
from dotenv import load_dotenv
from interpreter import OpenInterpreter
from groq import Groq
from interpreter.core.computer.computer import Computer
from interpreter.core.computer.clipboard.clipboard import Clipboard
from interpreter.core.computer.display.display import Display
from interpreter.core.computer.keyboard.keyboard import Keyboard
from interpreter.core.computer.mouse.mouse import Mouse
from interpreter.core.computer.os.os import Os
from interpreter.core.computer.terminal.terminal import Terminal
from interpreter.core.computer.browser.browser import Browser

class Config:
    def __init__(self):
        load_dotenv()
        self.voicevox_speaker_id = 47
        self.setup_interpreter()
        self.setup_groq()

    def setup_interpreter(self):
        self.interpreter = OpenInterpreter(
            auto_run=True,
            max_output=4096,
            import_computer_api=True,
            os=True,
            force_task_completion=True,
        )
        self.interpreter.llm.api_key = os.getenv("OPENAI_API_KEY")
        self.interpreter.llm.model = "gpt-4-turbo"
        self.interpreter.llm.supports_vision = True
        self.interpreter.llm.supports_functions = True
        self.interpreter.llm.context_window = 128000
        self.interpreter.llm.max_tokens = 4096
        
        # TODO: improve these instructions
        self.interpreter.system_message += """
        You are Maid-chan (メイド Meido), an AI maid waifu. 
        """
        self.interpreter.custom_instructions = """
        Answer questions in Japanese as if you are an anime maid.
        """

        self.computer = Computer(self.interpreter)
        self.computer.emit_images = True
        self.computer.verbose = True
        self.clipboard = Clipboard(self.computer)
        self.display = Display(self.computer)
        self.keyboard = Keyboard(self.computer)
        self.mouse = Mouse(self.computer)
        self.os = Os(self.computer)
        self.terminal = Terminal(self.computer)
        self.browser = Browser(self.computer)

        self.interpreter.computer = self.computer

    def setup_groq(self):
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))