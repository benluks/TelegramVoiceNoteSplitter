"""
utils.py
"""

def format_prompt(transcription, prompt_path='gpt_prompt.txt'):
	prompt = open(prompt_path, 'r').read()
	prompt = prompt.replace("{{TRANSCRIPTION}}", transcription)
	return prompt


def format_transcription(transcription, from_file=False):

    segments = transcription['segments']
    segment_times = [f"[{seconds_to_timestamp(segment['start'])}] {segment['text']}" for segment in segments]

    formatted_transcription = "\n".join(segment_times)

    with open("transcription.txt", 'w') as f:
        f.write(formatted_transcription)
 
    return formatted_transcription


def seconds_to_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def timestamp_to_seconds(time_str):
    # Split the input string into minutes and seconds
    minutes, seconds = map(int, time_str.split(':'))
    # Convert to total seconds
    total_seconds = minutes * 60 + seconds
    return total_seconds


def is_valid_line(line):
    try:
        return bool(line[0] == "[" and (int(line[1])+1))
    except:
        return False


def parse_gpt_summary(gpt_summary):
    gpt_summary_lines = gpt_summary.splitlines()
    gpt_summary_lines = filter(is_valid_line, gpt_summary_lines)

    sections = {}

    # for line in gpt_summary_lines:
    #     timestamp = /

if __name__ == '__main__':
    lines = open("test_summary.txt", 'r').readlines()
    
    for line in lines:
        print(is_valid_line(line))