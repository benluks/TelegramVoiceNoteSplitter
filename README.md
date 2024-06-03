# Telegram Voice Note Splitter

This app grabs the last voice note sent in a conversation with your partner and splits it up into sections, along with headers.

## Setup

Uptake is a little involved, so I've listed the steps below.

### 1. Creating a Telegram Application

Follow the steps [here](https://core.telegram.org/api/obtaining_api_id) to create a telegram application. There you'll get an `api_id` and an `api_hash`, which you'll need in you .env file (below).

### 2. OpenAI credentials

This app using the OpenAI API and GPT-4o. You can sign up [here](https://openai.com/index/openai-api/). It can't get it to work unless I pass my organization-ID, hence why I included it in the .env. I keep my API key accessible in my `$PATH`, as a variable named `OPENAI_API_KEY`, so I don't need to specify it in the .env file.

### 3. Adding the environment variables

A sample is provided in `example.env`. You'll want to create a `.env` file in the same directory as this file.

## Running

First, get the requirements:

`pip install -r requirements.txt`

You'll have to figure out the ID of your partner. You can list the chat/contact names and IDs of all your current chats by running the follwoing ([simplified from the `telethon` docs](https://docs.telethon.dev/en/stable/basic/quick-start.html))
```python
from telethon import TelegramClient

# Remember to use your own values from my.telegram.org!
api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Getting information about yourself
    me = await client.get_me()
    
    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

with client:
    client.loop.run_until_complete(main())
```

This'll save your info in a session and help you find your partner's ID. Save the ID in the .env file.

And you're off to the races!

`python main.py`

Enjoy!

## Notes

This app runs whisper locally. It works, even on an Intel CPU, but it's slow. I opted for the `"tiny"` model, which was plenty good enough for me. Be warned, it'll download the 72.1MB model when you run the program.