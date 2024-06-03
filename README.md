# Telegram Voice Note Splitter

This app grabs the last voice note sent in a conversation with your partner and splits it up into sections.
Uptake is a little involved, so I've listed the steps below.

## Creating a Telegram Application

Follow the steps [here](https://core.telegram.org/api/obtaining_api_id) to create a telegram application. There you'll get an `api_id` and an `api_hash`, which you'll need in you .env file (below).

## OpenAI

This app using the OpenAI API and GPT-4o. You can sign up [here](https://openai.com/index/openai-api/). It can't get it to work unless I pass my organization-ID, hence why I included it in the .env. I keep my API key accessible in my `$PATH`, as a variable named `OPENAI_API_KEY`, so I don't need to specify it in the .env file.

## Adding the environment variables

A sample is provided in `example.env`. You'll want to create a `.env` file in the same directory as this file.