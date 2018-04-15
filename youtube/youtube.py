import requests
import os

class YoutubeUser:
	def __init__(self):
		self.YOUTUBE_CHANNELS_URL = 'https://www.googleapis.com/youtube/v3/channels'
		self.YOUTUBE_ACTIVITIES_URL = 'https://www.googleapis.com/youtube/v3/activities'
		self.YOUTUBE_VIDEOS_URL = 'https://www.googleapis.com/youtube/v3/videos'
		self.YOUTUBE_KEY = os.environ['YOUTUBE_KEY']
		self.payload = {'part': 'snippet,contentDetails,statistics,id',
						'forUsername': '',
						'key' : self.YOUTUBE_KEY}
		self.activities = {'part': 'snippet,contentDetails',
							'channelId': '',
							'key' : self.YOUTUBE_KEY}
		self.videos = {'part': 'statistics',
						'id' : '',
						'key' : self.YOUTUBE_KEY}

	def get_channel_info(self, username):
		self.payload['forUsername'] = username
		return requests.get(self.YOUTUBE_CHANNELS_URL,
							params=self.payload).json()

	def get_activitie_info(self, channelId):
		self.activities['channelId'] = channelId
		return requests.get(self.YOUTUBE_ACTIVITIES_URL,
							params=self.activities).json()

	def get_videos_info(self, id):
		self.videos['id'] = id
		return requests.get(self.YOUTUBE_VIDEOS_URL,
							params=self.videos).json()

	def get_channel_title(self, response):
		return response['items'][0]['snippet']['title'] if response['items'] \
											else 'ERROR: Canal não existe.'

	def get_channel_subscribers(self, response):
		return response['items'][0]['statistics']['subscriberCount'] \
			if response['items'] and response['items'][0]['statistics'] \
			else 'ERROR: Canal não existe ou não possui estatísticas sobre o canal.'

	def get_channel_id(self, response):
		return response['items'][0]['id'] \
			if response['items'] and response['items'][0]['id'] \
			else 'ERROR: Canal não existe.'

	def get_all_videos_ids(self, response):
		videoIDs = []
		for id in response['items']:
			videoIDs.append(id['contentDetails']['upload']['videoId'])
		return videoIDs

	def get_all_Videoviews(self, response):
		videoViews = []
		for item in response:
			views = self.get_videos_info(item)
			videoViews.append(views['items'][0]['statistics']['viewCount'])
		return videoViews
