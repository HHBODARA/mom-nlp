import os
from datetime import date, datetime
import time
import json
import requests

api_key = "309133d2fd80488680160e5d17452702"

with open('transcript.txt') as f:
    id_t = f.readlines()

transcript_id = id_t[0]
# print(transcript_id)

# transcript_id = '6raenoqau3-f7e2-4f5d-8df6-9ad189379071'

endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
# print(endpoint)
headers = {
    "authorization": api_key,
}

transcript_output_response = requests.get(endpoint, headers=headers)
data = transcript_output_response.json()
# print(data)

if os.path.exists("transcript.json"):
  os.remove("transcript.json")
else:
  pass


name = input("Enter Your Name: ")
email = input("Enter Your Email Address: ")
organizer = input("Enter Organizer: ")
location = input("Enter Location: ")
datei = input('Enter a date formatted as YYYY-MM-DD: ').split('-')
year, month, day = [int(item) for item in datei]
d = date(year, month, day)

participants = set()
for ent in data['entities']:
  if ent['entity_type'] == 'person_name':
    participants.add(ent['text'])
for utterance in data['utterances']:
  utt = "Speaker" + utterance['speaker']
  participants.add(utt)

tranc_lst = []
for utterance in data['utterances']:
    text = "Speaker" + utterance["speaker"] + ": " + utterance['text']
    tranc_lst.append(text)

summ = []
agenda_lst = []
for agenda in data['chapters']:
    text = agenda['headline']
    summary = agenda['summary']
    agenda_lst.append(text)
    summ.append(summary)

topic_lst = []
for x in (sorted(data['iab_categories_result']['summary'], key=lambda k: data['iab_categories_result']['summary'][k], reverse=True)[:1]):
  topic_lst.append(x.split('>')[0])


json_data = {
  "email":email,
  "updated_on":str(datetime.now()),
  "topic":topic_lst,
  "organizer": organizer,
  "participants":sorted(participants),
  "location":location,
  "date":str(d),
  "duration":time.strftime("%H:%M:%S", time.gmtime(data['audio_duration'])),
  "updated_by":name,
  "prepared_by":name,
  "transcript":tranc_lst,
  "agenda":agenda_lst,
  "summary":summ
}

json_object = json.dumps(json_data, indent=4)
with open("sample.json", "w") as outfile:
  outfile.write(json_object)
