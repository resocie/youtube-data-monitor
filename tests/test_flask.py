from server.main import *
from server.models import Actor, Videos
from flask import Flask
import unittest
import json
from datetime import datetime
from server import db
from server.main import app

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db.init_app(app)


class TestFlask(unittest.TestCase):

    def setUp(self):
        app.app_context().push()
        db.create_all()
        collected_date_value = datetime.strptime('2018-06-14',
                                                 '%Y-%m-%d').date()
        actor_db = Actor(actor_name='Marina Silva',
                         actor_username='msilvaonline',
                         channel_id='channel_id_value',
                         title='Marina Silva',
                         subscribers=13515,
                         video_count=876,
                         view_count=4307555,
                         comment_count=0,
                         created_date='2010-01-26',
                         keywords='keywords_value',
                         collected_date=collected_date_value,
                         thumbnail_url='thumbnail_url_value',
                         description='description_value',
                         banner_url='banner_url_value',
                         above_one_hundred_thousand=False)

        video_db = Videos(views='1',
                          title='Video Marina Silva',
                          likes='1',
                          dislikes='1',
                          comments='1',
                          favorites='1',
                          url='url Marina Silva',
                          publishedAt='data publicação',
                          description='descrição',
                          tags='tags',
                          embeddable='embeddable',
                          duration='duration',
                          thumbnail='thumbnail',
                          related_to_video='related_to_video',
                          category='category',
                          collected_date=collected_date_value,
                          channel_id='channel_id_value',
                          video_id='1')

        db.session.add(video_db)
        db.session.add(actor_db)
        db.session.commit()
        # Cria um cliente de teste
        self.app = app.test_client()
        # Propaga as exceções para o cliente de teste
        self.app.testing = True

    def test_list_actors(self):
        # Envia uma requisição HTTP GET para a aplicação

        result = self.app.get('/actors')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

    def test_list_dates(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/dates')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

    def test_list_actor_channel_info(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/2018-06-14/canal/Marina_Silva')
        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        channel_id = "channel_id_value"
        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r['channel_id'], channel_id)

    def test_list_actor_channel_info_latest(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/latest/canal/Marina_Silva')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        channel_id = "channel_id_value"
        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r['channel_id'], channel_id)

    def test_list_actor_channel_info_with_actor_name_lower(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/2018-06-14/canal/marina_silva')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        channel_id = "channel_id_value"
        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(r['channel_id'], channel_id)

    def test_list_actor_channel_info_with_wrong_data(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/14-06/canal/marina_silva')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 450)

    def test_list_actor_channel_info_with_wrong_actor_name(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/2018-06-14/canal/marina')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 460)

    def test_list_actor_videos_info(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/2018-06-14/canal/marina_silva/videos')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)
        video_data_keys = ['title', 'views', 'likes', 'dislikes',
                           'comments', 'favorites', 'url'].sort()

        r = json.loads(result.data.decode('utf8'))

        self.assertEqual(list(r['videos'][0].keys()).sort(), video_data_keys)

    def test_list_actor_videos_info_latest(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/latest/canal/marina_silva/videos')

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
