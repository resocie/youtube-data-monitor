from youtube.youtube import YoutubeAPI
import requests
import json
import os

ACTIVITIES_URL = 'https://www.googleapis.com/youtube/v3/activities'
VIDEOS_URL = 'https://www.googleapis.com/youtube/v3/videos'


class Videos:
    """Gets all video's informations.

        Following certain date gets video's id, views and title.
    """
    def __init__(self):
        self.user = YoutubeAPI()
        self._activities = {'part': 'snippet,contentDetails',
                            'channelId': '',
                            'maxResults': '',
                            'publishedAfter': '2018-01-01T00:00:01.45-03:00',
                            'key': self.user._youtube_key}
        self._videos = {'part': 'snippet,statistics',
                        'id': '',
                        'maxResults': '',
                        'key': self.user._youtube_key}

    def get_activity_info(self, channel_id, max_results):
        self._activities['maxResults'] = max_results
        self._activities['channelId'] = channel_id
        return requests.get(ACTIVITIES_URL, params=self._activities).json()

    def get_videos_info(self, video_id, max_results):
        self._videos['maxResults'] = max_results
        self._videos['id'] = video_id
        return requests.get(VIDEOS_URL, params=self._videos).json()

    def get_all_video_ids(self, response):
        video_ids = []

        for video in response['items']:
            try:
                video_ids.append(video['contentDetails']['upload']['videoId'])
            except KeyError:
                pass

        return video_ids

    def get_all_video_items(self, response, max_results):
        videos_dic = []

        for item in response:
            views = self.get_videos_info(item, max_results)
            video_views = (views['items'][0]['statistics']['viewCount'])
            video_titles = (views['items'][0]['snippet']['title'])
            videos_dic.append({'title': video_titles, 'views': video_views})

        return videos_dic

    def get_all_video_views_user_id(self, response, max_results):
        channel_id = self.user.get_channel_id(response)
        result_activities = self.get_activity_info(channel_id, max_results)
        videos_id = self.get_all_video_ids(result_activities)
        video_views = self.get_all_video_items(videos_id, max_results)

        return video_views
