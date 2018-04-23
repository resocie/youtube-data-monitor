from core.output import FileOutput
import requests
import json
import os

class YoutubeAPI:
	def __init__(self):
		self._youtube_channels_url = 'https://www.googleapis.com/youtube/v3/channels'
		# @TODO handle if youtube_key not found
		self._youtube_activities_url = 'https://www.googleapis.com/youtube/v3/activities'
		self._youtube_videos_url = 'https://www.googleapis.com/youtube/v3/videos'
		self._youtube_key = os.environ['YOUTUBE_KEY']
		self._payload = {'part': 'snippet,contentDetails,statistics,id',
						'id': '',
						'key' : self._youtube_key}

		self._payload_username = {'part': 'snippet,contentDetails,statistics,id',
						'forUsername':'',
						'key' : self._youtube_key}

		self._activities = {'part': 'snippet,contentDetails',
							'channelId': '',
							'maxResults': '',
							'publishedAfter': '2018-01-01T00:00:01.45-03:00',
							'key' : self._youtube_key}
		self._videos = {'part': 'snippet,statistics',
						'id' : '',
						'maxResults': '',
						'key' : self._youtube_key}


		self._filename = 'data/youtube.csv'
		self._csv_headers = ['ator', 'username', 'channel_id','video_count','view_count','subscribers']

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
					'channel_id':'',
					'video_count':'',
					'view_count':'',
					'subscribers':''} for name in actors]

		return FileOutput(self._filename).export_CSV(input_data=input_data,
											headers=self._csv_headers).status

	def get_channel_info(self, id):
		self._payload['id'] = id
		return requests.get(self._youtube_channels_url,
							params=self._payload).json()

	def get_activitie_info(self, channelId, maxResults):
		self._activities['maxResults'] = maxResults
		self._activities['channelId'] = channelId
		return requests.get(self._youtube_activities_url,
							params=self._activities).json()

	def get_videos_info(self, id, maxResults):
		self._videos['maxResults'] = maxResults
		self._videos['id'] = id
		return requests.get(self._youtube_videos_url,
							params=self._videos).json()

	def get_channel_info_by_username(self,username):
		self._payload_username['forUsername'] = username
		return requests.get(self._youtube_channels_url,
							params=self._payload_username).json()

	def get_channel_title(self, response):
		return response['items'][0]['snippet']['title'] if response['items'] \
											else 'ERROR: Canal não existe.'

	def get_channel_id(self, response):
		return response['items'][0]['id'] \
			if response['items'] and response['items'][0]['id'] \
			else 'ERROR: Canal não existe.'

	def get_all_videos_ids(self, response):
		videoIDs = []
		for id in response['items']:
			try:
				videoIDs.append(id['contentDetails']['upload']['videoId'])
			except KeyError:
				pass
		return videoIDs

	def get_all_Video_Items(self, response, maxResults):
		videos_dic = []
		for item in response:
			views = self.get_videos_info(item, maxResults)
			videoViews=(views['items'][0]['statistics']['viewCount'])
			videoTitles=(views['items'][0]['snippet']['title'])
			videos_dic.append({'Título':videoTitles,'Número de visualizações':videoViews})
		return videos_dic

	def get_all_Video_Views_user_ID(self, userID, maxResults):
		result = self.get_channel_info(userID)
		id = self.get_channel_id(result)
		result_activities = self.get_activitie_info(id, maxResults)
		videos_id = self.get_all_videos_ids(result_activities)
		VideoViews = self.get_all_Video_Items(videos_id, maxResults)
		return VideoViews

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
