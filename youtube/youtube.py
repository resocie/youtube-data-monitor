from core.output import FileOutput
import requests
import json
import os

class YoutubeAPI:
	def __init__(self):
		self.YOUTUBE_CHANNELS_URL = 'https://www.googleapis.com/youtube/v3/channels'
		self.YOUTUBE_KEY = os.environ['YOUTUBE_KEY']
		self.payload = {'part': 'snippet,contentDetails,statistics,id',
						'forUsername': '',
						'key' : self.YOUTUBE_KEY}

		self.FILENAME = 'data/youtube.csv'
		self.CSV_HEADERS = ['atores', 'username', 'channel_id']

	def generate_csv(self, clean=False):
		if clean and os.path.isfile(self.FILENAME):
			os.remove(self.FILENAME)
		elif os.path.isfile(self.FILENAME):
			return True
		actors = json.load(open('data/grupos_politicos.json') )["atores"]
		return FileOutput(self.FILENAME).export_CSV(
											headers=self.CSV_HEADERS).status

	def get_channel_info(self, username):
		self.payload['forUsername'] = username
		return requests.get(self.YOUTUBE_CHANNELS_URL,
							params=self.payload).json()

	def get_channel_title(self, response):
		return response['items'][0]['snippet']['title'] if response['items'] \
											else 'ERROR: Canal não existe.'

	def get_channel_subscribers(self, response):
		return response['items'][0]['statistics']['subscriberCount'] \
			if response['items'] and response['items'][0]['statistics'] \
			else 'ERROR: Canal não existe ou não possui estatísticas sobre o canal.'

	def get_channel_total_view_count(self, response):
		return response['items'][0]['statistics']['viewCount'] \
			if response['items'] and response['items'][0]['statistics'] \
			else 'ERROR: Canal não existe ou não possui estatísticas sobre o canal.'
