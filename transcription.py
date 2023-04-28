import os
import sys
import time
import requests

api_key = "309133d2fd80488680160e5d17452702"

def read_file(file_path, chunk_size=5242880):
    with open(file_path, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def transcription(file_path):
    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(file_path))
    audio_url = response.json()['upload_url']
    print(audio_url)

    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
    "audio_url": audio_url,
    "redact_pii": True,
    "redact_pii_policies": ["medical_process", "medical_condition", "blood_type", "drug", "injury", "number_sequence", "email_address", "date_of_birth", "phone_number", "credit_card_number", "credit_card_expiration", "credit_card_cvv", "date", "nationality", "event", "language", "location", "money_amount", "person_name", "person_age", "organization", "political_affiliation", "occupation", "religion", "drivers_license", "banking_information"],
    "auto_highlights": True,
    "content_safety": True,
    "iab_categories": True,
    "sentiment_analysis": True,
    # "summarization": True,
    "summary_model": "informative",
    "summary_type": "bullets_verbose",
    "auto_chapters": True,
    "entity_detection": True,
    "speaker_labels": True
    # "filter_profanity": True
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    transcript_input_response = requests.post(endpoint, json=json, headers=headers)

    # print(transcript_input_response.json())

    transcript_id = transcript_input_response.json()["id"]
    print(transcript_id)
    if os.path.exists("transcript_id.txt"):
      os.remove("transcript_id.txt")
    else:
      pass
    
    with open('transcript.txt', 'a') as f:
        f.write(transcript_id)

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    headers = {
        "authorization": api_key,
    }

    while True:
        transcript_output_response = requests.get(endpoint, headers=headers)
        status = transcript_output_response.json()["status"]
        if status == "completed":
            print("Transcription is complted")
            break
        print("Transcription status is:", status)
        time.sleep(5)



#code start
file_path = input('Enter a file path: ')

if os.path.exists(file_path):
    # print('The file exists')
    file_name, file_ext = os.path.splitext(file_path)

    file_format = [".3ga", ".8svx", ".aac", ".ac3", ".aif", ".aiff", ".alac", ".amr", ".ape", ".au", ".dss", ".flac", ".flv", ".m4a", ".m4b", ".m4p", ".m4r", ".mp3", ".mpga", ".ogg", ".oga", ".mogg", ".opus", ".qcp", ".tta", ".voc", ".wav", ".wma", ".wv"]
    

    for name in file_format:
        if name == file_ext:
            transcription(file_path)
            break
    else:
        print(file_ext, "is not in the list.")

else:
    print('The specified file does NOT exist')