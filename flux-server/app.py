from flask import Flask, request, jsonify
import subprocess
import requests
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    # This route handles the root URL and returns a welcome message
    return "Welcome to the Audio Transcription API"

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.json
    audio_url = data['audioUrl']

    # Generate a unique filename for each transcription to avoid conflicts
    output_filename = f"output_{os.urandom(6).hex()}.json"

    # Using subprocess to call Whisper directly with the URL
    # This works only if insanely-fast-whisper supports direct URL usage
    command = f"pipx run insanely-fast-whisper --file-name \"{audio_url}\" --output {output_filename}"
    subprocess.run(command, shell=True)

    # Read and return the transcription result
    transcription = {}
    if os.path.exists(output_filename):
        with open(output_filename, "r") as file:
            transcription = json.load(file)

    # Clean up the JSON file after reading
    if os.path.exists(output_filename):
        os.remove(output_filename)

    return jsonify(transcription)


@app.errorhandler(404)
def page_not_found(e):
    # This function returns a custom 404 error message
    return jsonify({"error": "Page not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
