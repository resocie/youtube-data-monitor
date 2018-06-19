from server.models import Actor, Videos
from server.queries import DBYouTube
from flask import Flask
import unittest
from datetime import datetime
from server import app, db

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db.init_app(app)


class TestFlask(unittest.TestCase):

    def setUp(self):
        app.app_context().push()
        db.create_all()
        actor_db = Actor(actor_name='Marina Silva',
                         actor_username='msilvaonline',
                         channel_id='UC9uefWa6TXIPDRWGZYMcTuA',
                         title='Marina Silva',
                         subscribers=13515,
                         video_count=876,
                         view_count=4307555,
                         comment_count=0,
                         created_date='2010-01-26',
                         collected_date=datetime.strptime('2018-06-14',
                                                          '%Y-%m-%d').date(),
                         thumbnail_url='https://yt3.ggpht.com/-dKJCCcRJLUM/' +
                         'AAAAAAAAAAI/AAAAAAAAAAA/dPAqpLhWma4/s88-c-k' +
                         '-no-mo-rj-c0xffffff/photo.jpg',
                         description='Canal oficial da candidata à ' +
                         'Presidência pelo PSB-Rede-PPS-PPL-PHS-PRP.',
                         keywords='nova politica',
                         banner_url='https://yt3.ggpht.com/_TMNHFdl76PF7' +
                         'AePJJu6CK384TYDUHxWG2EkqSsS5VBjdC6ZYekK1-H15L' +
                         'cbna4Kyv2HLsiDexI=w1060-fcrop64=1,00005a57ffff' +
                         'a5a8-nd-c0xffffffff-rj-k-no',
                         above_one_hundred_thousand=False)
        # Cria um cliente de teste
        db.session.add(actor_db)
        db.session.commit()
        self.app = app.test_client()
        # Propaga as exceções para o cliente de teste
        self.app.testing = True

    def test_db_get_dates(self):
        dates = DBYouTube.get_dates()
        self.assertEqual(dates['dates'], ['14-06-2018'])

    def test_db_get_info_actor(self):
        actor = DBYouTube.get_info_actor('14-06-2018', 'Marina Silva')
        self.assertEqual(actor['actor_name'], 'Marina Silva')

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
