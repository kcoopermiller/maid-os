from voicevox import Client
import asyncio
from IPython.display import Audio
import torchaudio
import torchaudio.transforms as transforms
import sounddevice as sd
from io import BytesIO
import torch

output_path = "voice.wav"

# Play the audio using sounddevice
def play_audio(wav_file):
    # load wave file or file-like object
    data, sr = torchaudio.load(wav_file)
    # play audio
    sd.play(data[0].numpy(), sr)
    # wait until finish playing
    sd.wait()

async def main():
    async with Client() as client:
        audio_query = await client.create_audio_query("こんにちは！", speaker=1)
        result = await audio_query.synthesis(speaker=1)
        
        # change result bytes stream to file-like object
        wav_file_bytesIO = BytesIO(result)

        # 1. directly play the audio
        play_audio(wav_file_bytesIO)

        with open(output_path, "wb") as f:
            f.write(result)


if __name__ == "__main__":
    asyncio.run(main())
    # Audio(output_path)
    # play_audio(output_path)


