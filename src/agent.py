import re
from .config import Config

def chat(query: str, config: Config) -> tuple[str, str]:
    config.interpreter.chat(query, display=False)
    text = config.interpreter.messages[-1]['content']
    jp = re.search(r'\[\[JP\]\]\n(.*?)\n', text, re.DOTALL).group(1).strip() # TODO: this only prints the first line
    en = re.search(r'\[\[EN\]\]\n(.*)', text, re.DOTALL).group(1).strip()
    return jp, en