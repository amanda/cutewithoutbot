from random import choice
from twython import Twython, TwythonError
import os
from textblob import TextBlob
import time

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
OAUTH_KEY = os.getenv('OAUTH_KEY')
OAUTH_SECRET = os.getenv('OAUTH_SECRET')

twitter = Twython(API_KEY, API_SECRET, OAUTH_KEY, OAUTH_SECRET)

with open('endswithe.txt') as f:
	#words = (f.read()).split('\n')
	endswithe = f.read()

with open('dict.txt') as f:
	words = (f.read()).split('\n') #list

def find_nouns(wordlist):
	blob = TextBlob(wordlist)
	tags = blob.tags
	nouns = [w[0] for w in tags if w[1] == 'NN' or 'NNP' or 'NNS']
	return nouns

nouns = find_nouns(endswithe)

def generate_status():
	w = choice(endswithe.split('\n'))
	no_e = w[:-1]
	if no_e in words and not nouns:
		song = w + ' without the e (' + w[:-1] + ' from the team)'
	elif no_e in words and nouns:
		song = w + ' without the e (' + w[:-1] + ' for the team)'
	else:
		return None
	return song

def run():
	try:
		status = generate_status()
		if status is not None:
			twitter.update_status(status=status)
			twitter.update_status(status='testing')
		time.sleep(3600)
	except TwythonError:
	 	pass

if __name__ == '__main__':
	while True:
		run()
