import time
import requests
import json
from api_secret import API_KEY_ASSEMBLYAI

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(filename))
    audio_url = upload_response.json().get('upload_url')
    return audio_url

# Transcribe function
def transcribe(audio_url, sentiment_analysis):
    transcript_request = {
        "audio_url": audio_url,
        "sentiment_analysis": sentiment_analysis
    }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    
    if transcript_response.status_code != 200:
        print(f"Error: {transcript_response.json()}")
        return None  # Handle API failure
    
    return transcript_response.json().get('id')

# Polling function
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def get_transcription_results_url(audio_url, sentiment_analysis):
    transcript_id = transcribe(audio_url, sentiment_analysis)
    
    if not transcript_id:
        return None, "Failed to get transcript ID"

    while True:
        data = poll(transcript_id)  # Fixed variable name
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return None, data['error']

        print("Waiting 30 Seconds........")
        time.sleep(30)

# Save transcript
def save_transcript(audio_url, filename, sentiment_analysis=False):
    data, error = get_transcription_results_url(audio_url, sentiment_analysis)

    if data and 'text' in data:
        text_filename = filename + ".txt"
        with open(text_filename, "w") as f:
            f.write(data['text'])

        if sentiment_analysis and 'sentiment_analysis_results' in data:
            sentiment_filename = filename + "_sentiments.json"
            with open(sentiment_filename, "w") as f:
                json.dump(data['sentiment_analysis_results'], f, indent=4)  # Fixed key

        print("Transcription Saved!!!")
    else:
        print("Error:", error or "No text returned from API")
