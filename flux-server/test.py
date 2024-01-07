import requests
import subprocess
import os
import re

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def sanitize_filename(url):
    """Sanitizes the filename extracted from the URL."""
    filename = url.split('/')[-1]
    filename = re.sub(r'\?.*$', '', filename)  # Remove URL query parameters
    filename = re.sub(r'%2F', '_', filename)  # Replace %2F with an underscore
    return filename

def download_file(url):
    """Downloads file from the given URL and saves it locally."""
    local_filename = sanitize_filename(url)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def transcribe_audio(file_path):
    """Transcribes the given audio file using insanely_fast_whisper."""
    # Corrected command with --file-name
    command = f"insanely-fast-whisper --file-name \"{file_path}\""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print("Error in transcription process:", result.stderr)
        return None
    return result.stdout

# URL of the audio file
audio_url = 'https://firebasestorage.googleapis.com/v0/b/audiotranscriptionalapp-b6259.appspot.com/o/audio%2Fsubhanallah-alhamdulillah-ilaha-illallah-naat-tone-256k-61342.mp3?alt=media&token=2dfba7a5-786e-4145-af85-c751da8be492'

# Download the file
audio_file = download_file(audio_url)

# Transcribe the audio file
transcription = transcribe_audio(audio_file)

# Print the transcription
print(transcription)
