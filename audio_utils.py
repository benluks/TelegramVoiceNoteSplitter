import os
import subprocess


from utils import timestamp_to_seconds
from ai_clients import parse_gpt_summary
from pydub import AudioSegment


def convert_to_wav(input_file, output_file, delete=True):
    command = [
        'ffmpeg',
        '-i', input_file,
        output_file
    ]
    if delete:
        os.remove(input_file)
        
    subprocess.run(command, check=True)



def split_audio(file_path, timestamps):
    # Load the audio file
    audio = AudioSegment.from_ogg(file_path)

    # Create a list to store the audio segments
    audio_segments = []

    # Split the audio at the given timestamps
    for i, timestamp in enumerate(timestamps):
        start_time = timestamp_to_seconds(timestamp) * 1000
        if i == len(timestamps)-1:
            end_time = audio.duration_seconds * 1000
        else:    
            end_time = timestamp_to_seconds(timestamps[i + 1]) * 1000  # Convert to milliseconds
        segment = audio[start_time:end_time]
        audio_segments.append(segment)
    
    # Handle the final segment from the last timestamp to the end of the file
    # final_segment = audio[timestamps[-1] * 1000:]
    # audio_segments.append(final_segment)

    return audio_segments


# Function to save audio segments
def save_audio_segments(segments, base_filename):
    for i, segment in enumerate(segments):
        segment.export(f"{base_filename}_part{i + 1}.oga", codec="libopus", format="ogg", bitrate="30k")
    
    return 

def split_and_save_audio(timestamps, audio_file_path, output_basename="tmp/tmp"):
    
    audio_segments = split_audio(audio_file_path, timestamps)
    save_audio_segments(audio_segments, output_basename)

if __name__ == '__main__':
    sections = parse_gpt_summary(open("test_summary1.txt", 'r').read())
    timestamps, summaries = zip(*sections)
    split_and_save_audio(timestamps)