from youtube.youtube import YoutubeAPI
from core.actors_info import YoutubeAPI, scrap_basic_actors_info, \
                            insert_actors_info
import unittest
import json
import os


class TestYoutubeCSV(unittest.TestCase):

    def setUp(self):
        self._filename = 'data/youtube.csv'

    def test_generate_youtube_csv(self):
        csv = YoutubeAPI().generate_csv()
        self.assertTrue(os.path.isfile(self._filename))

    def test_check_data_of_an_actor(self):
        actors_info = scrap_basic_actors_info()
        insert_actors_info(actors_info)
        result = YoutubeAPI().get_row(column='actor', value='Bancada Ativista')
        self.assertEqual(result, {'username': '', 'channel_id': ''})

    def test_insert_value_of_an_actor(self):
        yt_api = YoutubeAPI()
        actors_info = scrap_basic_actors_info()
        insert_actors_info(actors_info)
        result = yt_api.insert_value(column='channel_id',
                                     value='UCX2Aanu4fGewmhP4rf5GQ3Q',
                                     search_cell='actor',
                                     search_value='Frente Brasil Popular')
        result = yt_api.get_row(column='actor', value='Frente Brasil Popular')
        self.assertEqual(result, {'username': '',
                                  'channel_id': 'UCX2Aanu4fGewmhP4rf5GQ3Q'
                                  })
        self.clean_csv(yt_api)

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


if __name__ == '__main__':
    unittest.main()
