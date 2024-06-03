from dotenv import load_dotenv
import os
from pathlib import Path
from natsort import natsorted

from telethon import TelegramClient

from audio_utils import convert_to_wav, split_and_save_audio
from ai_clients import get_gpt_response_from_audio_file
from utils import format_transcription, format_prompt

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
amarens=int(os.getenv("AMARENS_ID"))
me=int(os.getenv("ME_ID"))

client = TelegramClient("me", api_id, api_hash)

async def main():
    
    path = None
    
    async for message in client.iter_messages(int(amarens)):
        if message.voice:
            path = await message.download_media(os.getcwd())
            break
    
    sections = get_gpt_response_from_audio_file(path)
    timestamps, _ = zip(*sections)
    
    split_and_save_audio(timestamps, path)
    audio_files = natsorted(list(Path('tmp').iterdir()))

    # send audio with summaries
    await client.send_message('me', f"**{os.path.basename(path).split('_')[1]}**")
    for afile, (timestamp, summary) in zip(audio_files, sections):
        await client.send_message('me', f"[{timestamp}] **{summary}**")
        await client.send_file('me', afile, voice_note=True)
    
    # clean-up
    for afile in audio_files:
        afile.unlink()
    Path(path).unlink()
    

with client:
    client.loop.run_until_complete(main())