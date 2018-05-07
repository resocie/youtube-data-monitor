from core import FileOutput
import requests
import json
import os

CHANNELS_URL = 'https://www.googleapis.com/youtube/v3/channels'

class YoutubeAPI:
	def __init__(self):
		self._youtube_key = os.environ['YOUTUBE_KEY']
		if not self._youtube_key:
			raise ValueError('YOUTUBE_KEY not provided.')

		payload = {'part': 'snippet,contentDetails,statistics,id',
					'key' : self._youtube_key}

		self._payload_id = {**payload, **{'id':''}}
		self._payload_username = {**payload, **{'forUsername':''}}

		self._filename = 'data/youtube.csv'
		self._csv_headers = ['actor', 'username', 'channel_id',
							'video_count', 'view_count','subscribers']

	def insert_value(self, column, value, search_cell, search_value):
		return FileOutput(self._filename).insert_value(column, value,
														search_cell,
														search_value)

	def get_row(self, column, value):
		return FileOutput(self._filename).get_row(column, value)

	# returns True if csv is created with success
	def generate_csv(self, clean=False):
		if clean and os.path.isfile(self._filename):
			os.remove(self._filename)
		elif os.path.isfile(self._filename):
			return True

		with open('data/actors.json') as data_file:
			actors = json.load(data_file)
			actors = actors['actors']
			input_data = [{'actor': name,
							'username': '',
							'channel_id':'',
							'video_count':'',
							'view_count':'',
							'subscribers':''} for name in actors]

		return FileOutput(self._filename).export_to_CSV(input_data=input_data,
											headers=self._csv_headers)

	def get_channel_info(self, channel_id):
		self._payload_id['id'] = channel_id
		return requests.get(CHANNELS_URL, params=self._payload_id).json()

	def get_channel_info_by_username(self, username):
		self._payload_username['forUsername'] = username
		return requests.get(CHANNELS_URL, params=self._payload_username).json()

	def get_channel_title(self, response):
		if not response['items']:
			raise ValueError('Canal não existe.')
		return response['items'][0]['snippet']['title']

	def get_channel_id(self, response):
		if not response['items'] or not response['items'][0]['id']:
			raise ValueError('Canal não existe.')
		return response['items'][0]['id']

	def get_channel_subscribers(self, response):
		if not response['items'] or not response['items'][0]['statistics']:
			raise ValueError(' Canal não existe ou não possui estatísticas' +
							' sobre o canal.')
		return response['items'][0]['statistics']['subscriberCount']

	def get_channel_video_count(self, response):
		if not response['items'] or not response['items'][0]['statistics']:
			raise ValueError(' Canal não existe ou não possui estatísticas' +
									' sobre o canal.')
		return response['items'][0]['statistics']['videoCount']

	def get_channel_total_view_count(self, response):
		if not response['items'] or not response['items'][0]['statistics']:
			raise ValueError(' Canal não existe ou não possui ' +
									'estatísticas sobre o canal.')
		return response['items'][0]['statistics']['viewCount']
