from core import FileOutput
import requests
import json
import os
import shutil
from datetime import datetime

start_time = datetime.now().strftime("%d-%m-%Y")
CHANNELS_URL = 'https://www.googleapis.com/youtube/v3/channels'


class YoutubeAPI:
    """Communicate with YoutubeAPI.

        Get channels information.
    """
    def __init__(self):
        self._youtube_key = os.environ['YOUTUBE_KEY']
        if not self._youtube_key:
            raise ValueError('YOUTUBE_KEY not provided.')

        payload = {'part': 'snippet,contentDetails,statistics,id,' +
                   'brandingSettings',
                   'key': self._youtube_key}
        self._payload_id = {**payload, **{'id': ''}}
        self._payload_username = {**payload, **{'forUsername': ''}}
        self._foldername = 'data/' + start_time
        self._filename = 'data/' + start_time + '/youtube.csv'
        self._csv_headers = ['actor', 'username', 'channel_id']

    def insert_value(self, column, value, search_cell, search_value):
        return FileOutput(self._filename).insert_value(column, value,
                                                       search_cell,
                                                       search_value)

    def insert_multiple_values(self, column, search_cell, search_value):
        return FileOutput(self._filename).insert_multiple_values(column,
                                                                 search_cell,
                                                                 search_value)

    def get_row(self, column, value):
        return FileOutput(self._filename).get_row(column, value)

    def generate_folder(self, clean=False):
        if clean and os.path.isdir(self._foldername):
            shutil.rmtree(self._foldername)
        elif os.path.isdir(self._foldername):
            return True
        else:
            os.makedirs(self._foldername)

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
                           'channel_id': ''} for name in actors]

        return FileOutput(self._filename).export_to_CSV(
                                                    input_data=input_data,
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

    def get_channel_total_comment_count(self, response):
        if not response['items'] or not response['items'][0]['statistics']:
            raise ValueError(' Canal não existe ou não possui ' +
                             'estatísticas sobre o canal.')
        return response['items'][0]['statistics']['commentCount']

    def get_channel_creation_date(self, response):
        if not response['items'] or not response['items'][0]['snippet']:
            raise ValueError(' Canal não existe ou não possui ' +
                             'estatísticas sobre o canal.')
        return response['items'][0]['snippet']['publishedAt']

    def get_channel_thumbnail(self, response):
        if not response['items'] or not response['items'][0]['snippet']:
            raise ValueError(' Canal não existe ou não possui ' +
                             'estatísticas sobre o canal.')
        return response['items'][0]['snippet']['thumbnails']['default']['url']

    def get_channel_description(self, response):
        if not response['items'] or not response['items'][0]['snippet']:
            raise ValueError(' Canal não existe ou não possui ' +
                             'estatísticas sobre o canal.')
        return response['items'][0]['snippet']['description']

    def get_channel_keywords(self, response):
        if not response['items'] or not response['items'][0]['branding' +
                                                             'Settings']:
            raise ValueError(' Canal não existe ou não possui ' +
                             'estatísticas sobre o canal.')
        try:
            return response['items'][0]['brandingSettings']['channel']['keyw' +
                                                                       'ords']
        except KeyError:
            pass

    def get_channel_banner(self, response):
        if not response['items'] or not response['items'][0]['branding' +
                                                             'Settings']:
            raise ValueError(' Canal não existe ou não possui ' +
                             'estatísticas sobre o canal.')
        return response['items'][0]['brandingSettings']['image']['banner' +
                                                                 'ImageUrl']

    def check_above_one_hundred_thousand(self, subscribers):
        return int(subscribers) >= 100000
