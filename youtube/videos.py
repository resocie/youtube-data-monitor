from youtube.youtube import YoutubeAPI
import requests
import json
import os

ACTIVITIES_URL = 'https://www.googleapis.com/youtube/v3/activities'
VIDEOS_URL = 'https://www.googleapis.com/youtube/v3/videos'
VIDEOS_BASE_URL = 'https://www.youtube.com/watch?v='
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
CATEGORY_URL = 'https://www.googleapis.com/youtube/v3/videoCategories'


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
        self._activities_extent = {'part': 'snippet,contentDetails',
                                   'channelId': '',
                                   'maxResults': '',
                                   'publishedAfter':
                                   '2018-01-01T00:00:01.45-03:00',
                                   'publishedBefore': '',
                                   'key': self.user._youtube_key}
        self._videos = {'part': 'snippet,statistics,status,contentDetails',
                        'id': '',
                        'maxResults': '',
                        'key': self.user._youtube_key}
        self._search = {'part': 'id,snippet',
                        'maxResults': '',
                        'type': '',
                        'relatedToVideoId': '',
                        'key': self.user._youtube_key}
        self._category = {'part': 'id,snippet',
                          'hl': 'pt_BR',
                          'id': '',
                          'key': self.user._youtube_key}

    def get_category_info(self, id):
        self._category['id'] = id
        return requests.get(CATEGORY_URL, params=self._category).json()

    def get_search_info(self, max_results, related_to_video_id, type):
        self._search['maxResults'] = max_results
        self._search['relatedToVideoId'] = related_to_video_id
        self._search['type'] = type
        return requests.get(SEARCH_URL, params=self._search).json()

    def get_activity_info(self, channel_id, max_results):
        self._activities['maxResults'] = max_results
        self._activities['channelId'] = channel_id
        self._activities_extent['maxResults'] = max_results
        self._activities_extent['channelId'] = channel_id
        request = requests.get(ACTIVITIES_URL, params=self._activities).json()

        if('items' in request):
            length = len(request['items'])
            while(length >= 50):
                last_date = request['items'][-1]['snippet']['publishedAt']
                self._activities_extent['publishedBefore'] = last_date
                request_extent = requests.get(ACTIVITIES_URL,
                                              params=self._activities_extent)
                request_extent = request_extent.json()
                if('items' in request_extent):
                    length = len(request_extent['items'])
                    request['items'].extend(request_extent['items'])
                else:
                    length = 0
            self._activities_extent['publishedBefore'] = ''
        return request

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
            search = self.get_search_info(max_results, item, 'video')
            video_views = views['items'][0]['statistics']['viewCount']
            if 'likeCount' in views['items'][0]['statistics']:
                video_likes = views['items'][0]['statistics']['likeCount']
            else:
                video_likes = 'disabled'
            if 'dislikeCount' in views['items'][0]['statistics']:
                video_dislikes = \
                 views['items'][0]['statistics']['dislikeCount']
            else:
                video_dislikes = 'disabled'
            if 'commentCount' in views['items'][0]['statistics']:
                video_comments = \
                 views['items'][0]['statistics']['commentCount']
            else:
                video_comments = 'disabled'
            if 'favoriteCount' in views['items'][0]['statistics']:
                video_favorites = \
                 views['items'][0]['statistics']['favoriteCount']
            else:
                video_favorites = 'disabled'
            if 'publishedAt' in views['items'][0]['snippet']:
                video_published_date = \
                 views['items'][0]['snippet']['publishedAt']
            else:
                video_published_date = 'disabled'
            if 'description' in views['items'][0]['snippet']:
                video_description = \
                 views['items'][0]['snippet']['description']
            else:
                video_description = 'disabled'
            if 'tags' in views['items'][0]['snippet']:
                video_tags = \
                 views['items'][0]['snippet']['tags']
            else:
                video_tags = 'disabled'
            if 'embeddable' in views['items'][0]['status']:
                video_embeddable = \
                 views['items'][0]['status']['embeddable']
            else:
                video_embeddable = 'disabled'
            if 'duration' in views['items'][0]['contentDetails']:
                video_duration = \
                 views['items'][0]['contentDetails']['duration']
            else:
                video_duration = 'disabled'
            if 'thumbnails' in views['items'][0]['snippet']:
                video_thumbnail = \
                 views['items'][0]['snippet']['thumbnails']['high']['url']
            else:
                video_thumbnail = 'disabled'
            if search['items']:
                related_to_video = ''
                for video in search['items']:
                    related_to_video += VIDEOS_BASE_URL + \
                                         video['id']['videoId'] + ','
            else:
                related_to_video = 'disabled'
            if 'categoryId' in views['items'][0]['snippet']:
                category_id = views['items'][0]['snippet']['categoryId']
                category_info = self.get_category_info(category_id)
                video_category = category_info['items'][0]['snippet']['title']
            else:
                video_category = 'disabled'
            video_titles = views['items'][0]['snippet']['title']
            video_url = VIDEOS_BASE_URL + views['items'][0]['id']
            videos_dic.append({'title': video_titles,
                               'views': video_views,
                               'likes': video_likes,
                               'dislikes': video_dislikes,
                               'comments': video_comments,
                               'favorites': video_favorites,
                               'url': video_url,
                               'publishedAt': video_published_date,
                               'description': video_description,
                               'tags': video_tags,
                               'embeddable': video_embeddable,
                               'duration': video_duration,
                               'thumbnail': video_thumbnail,
                               'related_to_video': related_to_video,
                               'video_category': video_category
                               })

        return videos_dic

    def get_all_video_views_user_id(self, response, max_results):
        channel_id = self.user.get_channel_id(response)
        result_activities = self.get_activity_info(channel_id, max_results)
        videos_id = self.get_all_video_ids(result_activities)
        video_views = self.get_all_video_items(videos_id, max_results)

        return video_views
