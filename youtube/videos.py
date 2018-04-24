from youtube.youtube import YoutubeAPI
import json
import os
import requests

class Videos:

    def __init__ (self):
        self.user = YoutubeAPI()
        self._youtube_activities_url = 'https://www.googleapis.com/youtube/v3/activities'
        self._youtube_videos_url = 'https://www.googleapis.com/youtube/v3/videos'
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
        return requests.get(self._youtube_activities_url,
                            params=self._activities).json()

    def get_videos_info(self, id, maxResults):
        self._videos['maxResults'] = maxResults
        self._videos['id'] = id
        return requests.get(self._youtube_videos_url,
    						params=self._videos).json()

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

    def get_all_Video_Views_user_ID(self, response, maxResults):
        id = self.user.get_channel_id(response)
        result_activities = self.get_activitie_info(id, maxResults)
        videos_id = self.get_all_videos_ids(result_activities)
        VideoViews = self.get_all_Video_Items(videos_id, maxResults)
        return VideoViews
