from server.main import app
import unittest
import json
import os


class TestFlask(unittest.TestCase):
    def setUp(self):
        # Cria um cliente de teste
        self.app = app.test_client()
        # Propaga as exceções para o cliente de teste
        self.app.testing = True

    def test_list_actors(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/actors')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        with open('data/actors.json') as data_file:
            list_actors_original = json.load(data_file)

        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r, list_actors_original)

    def test_list_dates(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/dates')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        data_folders = [x[1] for x in os.walk('data/')][0]

        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r['dates'], data_folders)

    def test_list_actor_channel_info(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/07-05-2018/canal/Frente_Brasil_Popular')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        channel_id = "UCX2Aanu4fGewmhP4rf5GQ3Q"
        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r['channel_id'], channel_id)

    def test_list_actor_channel_info_latest(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/latest/canal/Frente_Brasil_Popular')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        channel_id = "UCX2Aanu4fGewmhP4rf5GQ3Q"
        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r['channel_id'], channel_id)

    def test_list_actor_channel_info_with_actor_name_lower(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/07-05-2018/canal/frente_brasil_popular')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        channel_id = "UCX2Aanu4fGewmhP4rf5GQ3Q"
        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r['channel_id'], channel_id)

    def test_list_actor_channel_info_with_wrong_data(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/07-05/canal/Frente_Brasil_Popular')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 450)

    def test_list_actor_channel_info_with_wrong_actor_name(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/07-05-2018/canal/Frente')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 460)

    def test_list_actor_videos_info(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/07-05-2018/canal/instituto_lula/videos')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)
        video_data_keys = ['title', 'views', 'likes', 'dislikes',
                           'comments', 'favorites', 'url'].sort()

        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(list(r['videos'][0].keys()).sort(), video_data_keys)

    def test_list_actor_videos_info_latest(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/latest/canal/instituto_lula/videos')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)
        video_data_keys = ['title', 'views', 'likes', 'dislikes',
                           'comments', 'favorites', 'url'].sort()

        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(list(r['videos'][0].keys()).sort(), video_data_keys)


if __name__ == '__main__':
    unittest.main()
