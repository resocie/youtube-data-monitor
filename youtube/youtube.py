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
							'maxResults': '',
							'key' : self.YOUTUBE_KEY}
		self.videos = {'part': 'snippet,statistics',
						'id' : '',
						'maxResults': '',
						'key' : self.YOUTUBE_KEY}
		self.payload_ID = {'part': 'snippet,contentDetails,statistics,id',
						'id': '',
						'key' : self.YOUTUBE_KEY}



	def get_channel_info(self, username):
		self.payload['forUsername'] = username
		return requests.get(self.YOUTUBE_CHANNELS_URL,
							params=self.payload).json()

	def get_channel_info_ID(self, id):
		self.payload_ID['id'] = id
		return requests.get(self.YOUTUBE_CHANNELS_URL,
								params=self.payload_ID).json()

	def get_activitie_info(self, channelId, maxResults):
		self.activities['maxResults'] = maxResults
		self.activities['channelId'] = channelId
		return requests.get(self.YOUTUBE_ACTIVITIES_URL,
							params=self.activities).json()

	def get_videos_info(self, id, maxResults):
		self.videos['maxResults'] = maxResults
		self.videos['id'] = id
		return requests.get(self.YOUTUBE_VIDEOS_URL,
							params=self.videos).json()

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
			videos_dic.append({videoTitles:videoViews})
		return videos_dic

	def get_all_Video_Views_Username(self, username, maxResults):
		result = self.get_channel_info(username)
		id = self.get_channel_id(result)
		result_activities = self.get_activitie_info(id, maxResults)
		videos_id = self.get_all_videos_ids(result_activities)
		VideoViews = self.get_all_Video_Items(videos_id, maxResults)
		return VideoViews

	def get_all_Video_Views_user_ID(self, userID, maxResults):
		result = self.get_channel_info_ID(userID)
		id = self.get_channel_id(result)
		result_activities = self.get_activitie_info(id, maxResults)
		videos_id = self.get_all_videos_ids(result_activities)
		VideoViews = self.get_all_Video_Items(videos_id, maxResults)
		return VideoViews
