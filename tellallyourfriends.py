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

def strip_ends(wordlist): #hacky, get rid of /r from ewords file
	new = [w[:-1].lower() for w in wordlist]
	return new

with open('endswithe.txt') as f:
	endswithe = f.read()

with open('sowpods.txt') as f:
	words = f.read()
	wordset = set(words.split('\n'))

def find_nouns(words):
	blob = TextBlob(words)
	tags = blob.tags
	nouns = [t[0].pluralize() for t in tags if t[1] == ('NN' or 'NNP' or 'NNS')]
	return nouns

nounset = set(find_nouns(words)) #unicode
e_wordset = set(strip_ends(endswithe.split('\n')))

def generate_songlist():
	songs = []
	for w in e_wordset:
		no_e = w[:-1]
		if no_e in wordset and no_e in nounset:
			song = w.lower() + ' without the e (' + w[:-1].lower() + ' for the team)'
			songs.append(song)
		elif no_e in wordset:
			song = w.lower() + ' without the e (' + w[:-1].lower() + ' from the team)'
			songs.append(song)
		else:
			pass
	return songs

def run():
	try:
		songs = generate_songlist()
		status = choice(songs)
		twitter.update_status(status=status)
		time.sleep(3600)
	except TwythonError:
	 	pass

if __name__ == '__main__':
	while True:
		run()
