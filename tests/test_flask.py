from server.main import app
from server.models import Actor, Videos, db
import unittest
import json
import os

bank_connection = "sqlite:///:memory:"


class TestFlask(unittest.TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = bank_connection
        return app

    def setUp(self):
        app.app_context().push()
        db.create_all()
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

        dates = db.session.query(Actor.collected_date).distinct()
        all_dates = [item[0] for item in dates]

        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r['dates'], all_dates)

    def test_list_actor_channel_info(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/02-06-2018/canal/Frente_Brasil_Popular')

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
        result = self.app.get('/02-06-2018/canal/frente_brasil_popular')

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
        result = self.app.get('/02-06-2018/canal/Frente')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 460)

    def test_list_actor_videos_info(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/02-06-2018/canal/lula/videos')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)
        video_data_keys = ['title', 'views', 'likes', 'dislikes',
                           'comments', 'favorites', 'url'].sort()

        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(list(r['videos'][0].keys()).sort(), video_data_keys)

    def test_list_actor_videos_info_latest(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/latest/canal/lula/videos')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)
        video_data_keys = ['title', 'views', 'likes', 'dislikes',
                           'comments', 'url', 'category', 'channel_id',
                           'collected_date', 'description', 'duration',
                           'embeddable', 'favorites',
                           'publishedAt', 'related_to_video',
                           'tags', 'thumbnail', 'video_id'].sort()

        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(list(r['videos'][0].keys()).sort(), video_data_keys)

    def test_all_actors(self):
        all_actors = db.session.query(Actor).all()
        actors = []
        for item in all_actors:
            actors.append(item.__dict__)

        for item in actors:
            result = self.app.get(item['collected_date']+'/canal/' +
                                  item['actor_name'])
            self.assertEqual(result.status_code, 200)

    def test_all_videos(self):
        all_actors = db.session.query(Actor).all()
        actors = []
        for item in all_actors:
            actors.append(item.__dict__)

        for item in actors:
            result = self.app.get(item['collected_date']+'/canal/' +
                                  item['actor_name']+'/videos')
            self.assertEqual(result.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
