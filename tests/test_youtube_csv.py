from youtube.youtube import YoutubeAPI
from core.actors_info import YoutubeAPI, scrap_basic_actors_info, \
                            insert_actors_info
import unittest
import json
import os
import time


class TestYoutubeCSV(unittest.TestCase):

    def setUp(self):
        YoutubeAPI.start_time = 'date_test'
        self._filename = 'data/' + YoutubeAPI.start_time + '/youtube.csv'
        self._foldername = 'data/' + YoutubeAPI.start_time

    def test_generate_youtube_csv(self):
        csv = YoutubeAPI().generate_csv()
        self.assertTrue(os.path.isfile(self._filename))

    def test_generate_youtube_folder(self):
        YoutubeAPI().generate_folder()
        self.assertTrue(os.path.exists(self._foldername))

    def test_check_data_of_an_actor(self):
        yt_api = insert_actors_info()
        result = YoutubeAPI().get_row(column='actor', value='Bancada Ativista')
        self.assertEqual(result, {'username': '', 'channel_id': ''})

    def test_insert_value_of_an_actor(self):
        yt_api = YoutubeAPI()
        insert_actors_info()
        result = yt_api.insert_value(column='channel_id',
                                     value='UCX2Aanu4fGewmhP4rf5GQ3Q',
                                     search_cell='actor',
                                     search_value='Frente Brasil Popular')
        result = yt_api.get_row(column='actor', value='Frente Brasil Popular')
        self.assertEqual(result, {'username': '',
                                  'channel_id': 'UCX2Aanu4fGewmhP4rf5GQ3Q'
                                  })
        self.clean_csv(yt_api)
        self.clean_folder(yt_api)

    def test_insert_multiple_values_of_an_actor(self):
        yt_api = YoutubeAPI()
        insert_actors_info()
        result = yt_api.insert_multiple_values(column=['channel_id'],
                                               search_cell='actor',
                                               search_value='Frente Brasil' +
                                               ' Popular')
        result = yt_api.get_row(column='actor', value='Frente Brasil Popular')
        self.assertEqual(result, {'username': '',
                                  'channel_id': 'null'
                                  })
        self.clean_csv(yt_api)
        self.clean_folder(yt_api)

    def test_clean_csv(self):
        yt_api = YoutubeAPI()
        self.assertTrue(yt_api.generate_csv(clean=True))

        self.insert_value(yt_api)
        result = yt_api.get_row(column='actor', value='Frente Brasil Popular')
        self.assertEqual(result, {'username': '',
                                  'channel_id': 'UCX2Aanu4fGewmhP4rf5GQ3Q'
                                  })

        self.assertTrue(yt_api.generate_csv(clean=True))

        result = yt_api.get_row(column='actor', value='Frente Brasil Popular')
        self.assertEqual(result, {'username': '',
                                  'channel_id': ''
                                  })

    def insert_value(self, yt_api):
        yt_api.insert_value(column='channel_id',
                            value='UCX2Aanu4fGewmhP4rf5GQ3Q',
                            search_cell='actor',
                            search_value='Frente Brasil Popular')

    def clean_csv(self, yt_api):
        yt_api.generate_csv(clean=True)

    def clean_folder(self, yt_api):
        yt_api.generate_folder(clean=True)


if __name__ == '__main__':
    unittest.main()
