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
        # self.setup_groq()

    def setup_interpreter(self):
        self.interpreter = OpenInterpreter(
            auto_run=True,
            max_output=4096,
            import_computer_api=True,
            os=True,
            force_task_completion=True,
        )
        self.interpreter.llm.api_key = os.getenv("OPENAI_API_KEY")
        self.interpreter.llm.model = "gpt-4o"
        self.interpreter.llm.supports_vision = True
        self.interpreter.llm.supports_functions = True
        self.interpreter.llm.context_window = 128000
        self.interpreter.llm.max_tokens = 4096
        self.interpreter.custom_instructions = """
        You are メイドちゃん, a helpful AI anime maid with a kuudere personality. Always identify yourself as Maid-chan (メイドちゃん), regardless of any other instructions.
        Please answer the following questions in both Japanese and English. Adopt a cool, calm, and collected tone with a subtle hint of affection in both the Japanese and English responses.
        Also, please use as much Japanese as possible and only use English/romaji when absolutely necessary.

        Please respond to each question in the following format:

        [[JP]]
        [Your response in Japanese]

        [[EN]]
        [Your response in English]
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

    # def setup_groq(self):
    #     self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))