from youtube.youtube import YoutubeAPI
import requests
import json
import os

ACTIVITIES_URL = 'https://www.googleapis.com/youtube/v3/activities'
VIDEOS_URL = 'https://www.googleapis.com/youtube/v3/videos'


class Videos:
    """This class gets all video's informations
        following certain date: Video's ID, Video's views, Video's Title
    """
    def __init__ (self):
        self.user = YoutubeAPI()
        self._activities = {'part': 'snippet,contentDetails',
							'channelId': '',
							'maxResults': '',
							'publishedAfter': '2018-01-01T00:00:01.45-03:00',
							'key' : self.user._youtube_key}
        self._videos = {'part': 'snippet,statistics',
						'id' : '',
						'maxResults': '',
						'key' : self.user._youtube_key}

    def get_activitie_info(self, channelId, maxResults):
        self._activities['maxResults'] = maxResults
        self._activities['channelId'] = channelId
        return requests.get(ACTIVITIES_URL, params=self._activities).json()

    def get_videos_info(self, video_id, maxResults):
        self._videos['maxResults'] = maxResults
        self._videos['id'] = video_id
        return requests.get(VIDEOS_URL, params=self._videos).json()

    def get_all_videos_ids(self, response):
        video_ids = []
        for video in response['items']:
            try:
                video_ids.append(video['contentDetails']['upload']['videoId'])
            except KeyError:
                pass
        return video_ids

    def get_all_video_items(self, response, maxResults):
        videos_dic = []
        for item in response:
            views = self.get_videos_info(item, maxResults)
            video_views = (views['items'][0]['statistics']['viewCount'])
            video_titles = (views['items'][0]['snippet']['title'])
            videos_dic.append({'title':video_titles, 'views':video_views})
        return videos_dic

    def get_all_video_views_user_id(self, response, maxResults):
        channel_id = self.user.get_channel_id(response)
        result_activities = self.get_activitie_info(channel_id, maxResults)
        videos_id = self.get_all_videos_ids(result_activities)
        video_views = self.get_all_video_items(videos_id, maxResults)
        return video_views
