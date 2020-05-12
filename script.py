import requests
import json
import pyttsx3
import re
import speech_recognition as sr
import itertools
import sys
import time
import numpy as np
import threading


API_KEY=''
PROJECT_TOKEN=''
RUN_TOKEN=''

response=requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',params={"api_key": API_KEY})
data=json.loads(response.text)

#print(data['country'])




done=False
#print(data['country'][0])
#print(data['country'])






class Data:
	def __init__(self,api_key,project_token):
		self.api_key=api_key
		self.project_token=project_token
		self.params={'api_key': self.api_key}

		self.data=self.retrieve_data()

	def retrieve_data(self):
		response=requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',params={"api_key": API_KEY})
		data=json.loads(response.text)

		return data

	def retrieve_total_cases(self):
		data=self.data['total']

		for subdata in data:
			if subdata['name']=='Coronavirus Cases:':
				return subdata['value']
		return "0"
	def retrieve_total_deaths(self):
		data=self.data['total']

		for subdata in data:
			if subdata['name']=='Deaths:':
				return subdata['value']

		return "0"
	def retrieve_total_recoveries(self):
		data=self.data['total']

		for subdata in data:
			if subdata['name']=='Recovered:':
				return subdata['value']
		return "0"

	def retrieve_total_countries(self):
		country_list=[]
		#data=self.data['country']
		data=self.data
		for subdata in data['country']:
			country_list.append(subdata['name'].lower())
		return country_list

	def retrieve_country_stats(self,country):
		data=self.data['country']
		for subdata in data:
			if subdata['name'].lower()==country.lower():
				return subdata
		return "0"

	def update_data(self):
		response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

		def poll():
			time.sleep(0.1)
			old_data = self.data
			while True:
				new_data = self.retrieve_data()
				if new_data != old_data:
					self.data = new_data
					print("Data updated")
					break
				time.sleep(5)


		t = threading.Thread(target=poll)
		t.start()

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')
#print(data['country'])
def tts(txt):
	engine=pyttsx3.init()
	engine.say(txt)
	engine.runAndWait()

def retrieve_speech():
	r=sr.Recognizer()
	with sr.Microphone() as src:
		audio=r.listen(src)
		said=''

		try:
			said=r.recognize_google(audio)

		except Exception as e:
			print(str(e))

	return said.lower()


def main():
	print('Initiated the Script')
	data=Data(API_KEY,PROJECT_TOKEN)
	END_PHRASE="stop"
	result=None
	TOTAL_PATTERNS = {
					re.compile("[\w\s]+ total [\w\s]+ cases"):data.retrieve_total_cases,
					re.compile("[\w\s]+ total cases"): data.retrieve_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"): data.retrieve_total_deaths,
                    re.compile("[\w\s]+ total deaths"): data.retrieve_total_deaths
					}

	COUNTRY_PATTERNS = {
					re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.retrieve_country_stats(country)['total_cases'],
                    re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.retrieve_country_stats(country)['total_deaths'],

                    re.compile("[\w\s]+ cases today [\w\s]+"): lambda country: data.retrieve_country_stats(country)['day_cases'],
                    re.compile("[\w\s]+ deaths today [\w\s]+"): lambda country: data.retrieve_country_stats(country)['day_deaths'],

					}
	UPDATE_PHRASE="update"

	while True:
		#animate()
		print('Rendering audio input...')
		txt=retrieve_speech()

		print(txt)
		total_countries=data.retrieve_total_countries()
		result=None
		for pattern,exec_f in COUNTRY_PATTERNS.items():
			if pattern.match(txt):
				tokenized_word=set(txt.split(" "))
				for country in total_countries:
					if country in tokenized_word:
						result=exec_f(country)
						break

		for pattern,exec_f in TOTAL_PATTERNS.items():
			if pattern.match(txt):
				result=exec_f()
				break

		if txt == UPDATE_PHRASE:
			result=str('Might take a moment to refresh the data...')
			data.update_data()

		if result:
			tts(result)

		if txt.find(END_PHRASE)!=-1:
			print('EXIT!')
			break
main()













