import os
import asyncio
from src.audio_utils import play_audio
from src.agent import chat
from src.config import Config

async def main():
    os.system('clear')
    config = Config()
    print("いらっしゃいませ\nType 'exit' to exit")
    await play_audio("いらっしゃいませ", config.voicevox_speaker_id)

    while True:
        query = input("\nQuery: ")
        if query == "exit":
            break
        jp, en = chat(query, config)
        audio_task = asyncio.create_task(play_audio(jp, config.voicevox_speaker_id))
        print(f"{en}\n")
        await audio_task

if __name__ == "__main__":
    asyncio.run(main())