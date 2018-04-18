from core.output import FileOutput
import requests
import json
import os

class YoutubeAPI:
	def __init__(self):
		self._youtube_channels_url = 'https://www.googleapis.com/youtube/v3/channels'
		# @TODO handle if youtube_key not found
		self._youtube_key = os.environ['YOUTUBE_KEY']
		self._payload = {'part': 'snippet,contentDetails,statistics,id',
						'forUsername': '',
						'key' : self._youtube_key}

		self._filename = 'data/youtube.csv'
		self._csv_headers = ['ator', 'username', 'channel_id']

	def insert_data(self, param, value, field_name, field_value):
		return FileOutput(self._filename).insert_data(param, value,
													field_name, field_value)

	def get_data(self, param, data):
		return FileOutput(self._filename).get_data(param, data)

	# returns True if csv is created with success
	def generate_csv(self, clean=False):
		if clean and os.path.isfile(self._filename):
			os.remove(self._filename)
		elif os.path.isfile(self._filename):
			return True

		with open('data/actors.json') as data_file:
			actors = json.load(data_file)
		actors = actors['atores']
		input_data = [{'ator': name,
					'username': '',
					'channel_id':''} for name in actors]

		return FileOutput(self._filename).export_CSV(input_data=input_data,
											headers=self._csv_headers).status

	def get_channel_info(self, username):
		self._payload['forUsername'] = username
		return requests.get(self._youtube_channels_url,
							params=self._payload).json()

	def get_channel_title(self, response):
		return response['items'][0]['snippet']['title'] if response['items'] \
											else 'ERROR: Canal não existe.'

	def get_channel_subscribers(self, response):
		return response['items'][0]['statistics']['subscriberCount'] \
			if response['items'] and response['items'][0]['statistics'] \
			else 'ERROR: Canal não existe ou não possui estatísticas sobre o canal.'

	def get_channel_video_count(self, response):
		return response['items'][0]['statistics']['videoCount'] \
			if response['items'] and response['items'][0]['statistics'] \
			else 'ERROR: Canal não existe ou não possui estatísticas sobre o canal.'

	def get_channel_total_view_count(self, response):
		return response['items'][0]['statistics']['viewCount'] \
			if response['items'] and response['items'][0]['statistics'] \
			else 'ERROR: Canal não existe ou não possui estatísticas sobre o canal.'
