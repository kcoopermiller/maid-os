from voicevox import Client
import torchaudio
import sounddevice as sd
from io import BytesIO
import sys

async def play_audio(query: str, speaker_id: int):
    async with Client() as client:
        audio_query = await client.create_audio_query(query, speaker=speaker_id)
        result = await audio_query.synthesis(speaker=speaker_id)
        
        wav_bytesIO = BytesIO(result)
        data, sr = torchaudio.load(wav_bytesIO)
        sd.play(data[0].numpy(), sr)
        sd.wait()