import asyncio
from src.audio_utils import play_audio
from src.agent import chat
from src.config import load_config
# import subprocess

async def main():
    config = load_config()
    await play_audio("いらっしゃいませ", config["voicevox_speaker_id"])

    while True:
        query = input("Query: ")
        if query == "exit":
            break
        query = chat(query)[1]['content']
        await play_audio(query, config["voicevox_speaker_id"])

if __name__ == "__main__":
    # subprocess.run("vis")
    asyncio.run(main())