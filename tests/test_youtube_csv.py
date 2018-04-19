from youtube.youtube import YoutubeAPI
from core.get_info_actors import get_actors_info
import unittest
import json
import os

class TestYoutubeCSV(unittest.TestCase):

    def setUp(self):
        self.filename = 'data/youtube.csv'

    def test_generate_youtube_csv(self):
        csv = YoutubeAPI().generate_csv()
        self.assertTrue(os.path.isfile(self.filename))

    def test_check_data_of_an_actor(self):
        yt_api = YoutubeAPI()
        self.assertTrue(yt_api.generate_csv())

        result = yt_api.get_data(param='ator', data='Bancada Ativista')
        self.assertEqual(result, {'username': '', 'channel_id': ''})

    def test_insert_data_of_an_actor(self):
        yt_api = YoutubeAPI()
        self.assertTrue(yt_api.generate_csv())

        result = yt_api.insert_data(param='channel_id',
                                    value='UCX2Aanu4fGewmhP4rf5GQ3Q',
                                    field_name='ator',
                                    field_value='Frente Brasil Popular')

        result = yt_api.get_data(param='ator', data='Frente Brasil Popular')
        self.assertEqual(result, {'username': '',
                                  'channel_id': 'UCX2Aanu4fGewmhP4rf5GQ3Q'})
        self.clean_csv(yt_api)

    def test_clean_csv(self):
        yt_api = YoutubeAPI()
        self.assertTrue(yt_api.generate_csv())

        self.insert_data(yt_api)
        result = yt_api.get_data(param='ator', data='Frente Brasil Popular')
        self.assertEqual(result, {'username': '',
                                  'channel_id': 'UCX2Aanu4fGewmhP4rf5GQ3Q'})

        self.assertTrue(yt_api.generate_csv(clean=True))

        result = yt_api.get_data(param='ator', data='Frente Brasil Popular')
        self.assertEqual(result, {'username': '', 'channel_id': ''})

    def test_get_info_actors(self):
        getinfo = get_actors_info()
        self.assertNotEqual(getinfo.read_actors_info(), [])


    def insert_data(self, yt_api):
        yt_api.insert_data(param='channel_id',
                        value='UCX2Aanu4fGewmhP4rf5GQ3Q',
                        field_name='ator',
                        field_value='Frente Brasil Popular')

    def clean_csv(self, yt_api):
        yt_api.generate_csv(clean=True)


if __name__ == '__main__':
    unittest.main()
