from openai import OpenAI
import whisper

from dotenv import load_dotenv
from pathlib import Path
import os
import sys

from utils import *

load_dotenv()
openai_organization = os.getenv("OPENAI_ORGANIZATION")
client = OpenAI(organization=openai_organization)

SYSTEM_MESSAGE = "You are a helpful text summarizer"


def whisper_transcribe(audio_file, model_version="tiny"):
    model = whisper.load_model(model_version)
    transcription = model.transcribe(audio_file)

    return transcription


def gpt_client(prompt):
	messages=[
		{"role": "system", "content": SYSTEM_MESSAGE},
		{"role": "user", "content": prompt}
	]
	response = client.chat.completions.create(
		model="gpt-4o",
		n=1,
		messages=messages,
		# max_tokens=
		)
	response = response.choices[0]
	if response.finish_reason == 'length':
		print("GPT stopped early for length. Consider raising `max_tokens`")
	return response.message.content


def gpt_summarize(formatted_transcription_or_path, output_path="test_summary.txt"):

	if os.path.exists(formatted_transcription_or_path):
		with open(formatted_transcription_or_path, 'r') as f:
			formatted_transcription = f.read()
	else:
		formatted_transcription = formatted_transcription_or_path

	prompt = format_prompt(formatted_transcription)
	gpt_response = gpt_client(prompt)
	
	with open(output_path, 'w') as f:
		f.write(gpt_response)

	return gpt_response


def get_gpt_response_from_audio_file(audio_file_path):
	transcription = whisper_transcribe(audio_file_path)
	formatted_transcription = format_transcription(transcription)
	
	gpt_summary = gpt_summarize(formatted_transcription)
	sections = parse_gpt_summary(gpt_summary)

	return sections


def parse_gpt_summary(gpt_summary):
	"""
	Get a list of sections from a raw GPT summary
	"""
	gpt_summary_lines = gpt_summary.splitlines()
	gpt_summary_lines = filter(is_valid_line, gpt_summary_lines)

	sections=[]

	for line in gpt_summary_lines:
		timestamp, text = line.split("] ")
		timestamp = timestamp[1:]
		sections.append((timestamp, text))
	
	return sections


if __name__ == '__main__':
	gpt_summary = gpt_summarize('test_trans.txt', "test_summary2.txt")
	print(parse_gpt_summary(gpt_summary))