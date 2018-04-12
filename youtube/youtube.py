import requests
import os

class YoutubeUser:
	def __init__(self):
		self.YOUTUBE_CHANNELS_URL = 'https://www.googleapis.com/youtube/v3/channels'
		self.YOUTUBE_KEY = os.environ['YOUTUBE_KEY']
		self.payload = {'part': 'snippet',
						'forUsername': '',
						'key' : self.YOUTUBE_KEY}

	def get_channel_info(self, username):
		self.payload['forUsername'] = username
		return requests.get(self.YOUTUBE_CHANNELS_URL,
							params=self.payload).json()

	def get_channel_title(self, response):
		return response['items'][0]['snippet']['title'] if response['items'] \
											else 'ERROR: Canal não existe.'
