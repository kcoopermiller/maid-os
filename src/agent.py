import re
from .config import Config

config = Config()

def translate(text: str) -> str:
    content = f"""
    Translate any of the Japanese in the TEXT below to English. Leave all other text or code as is. Only translate the text, do not include any other information. Do not mention that it is a translation.

    --------------------------------------------------
    Example 1:
    - Input:
    私はメイドです
    - Output:
    I am a maid

    Example 2:
    - Input:
    <!-- これはHTMLコメントの中の日本語です --> <div>これはHTMLタグの中の日本語のテキストです</div>
    - Output:
    <!-- This is Japanese inside an HTML comment --> <div>This is Japanese text inside an HTML tag</div>
    
    Example 3:
    - Input:
    はい、もちろんです。Pythonで短いFizzBuzzプログラムを生成しますね。
    ```
    for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
    ```
    このようにして、FizzBuzzプログラムを簡潔に実装することができます。コードはシンプルで読みやすく、Pythonの基本的な構文を使用しています。
    
    - Output:
    Yes, of course. I will generate a short FizzBuzz program in Python.
    ```
    for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
    ```
    This is how you can implement the FizzBuzz program concisely. The code is simple, readable, and uses basic Python syntax.
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