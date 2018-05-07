import requests
import unittest
import json

HEROKU_URL = 'https://youtube-data-monitor.herokuapp.com/'


class TestHeroku(unittest.TestCase):

    # def test_list_actors(self):
    #     # Envia uma requisição HTTP GET para a aplicação
    #     result = requests.get(HEROKU_URL+'actors')
    #
    #     # Verifica o código de estado da resposta da requisição
    #     self.assertEqual(result.status_code, 200)
    #
    #     with open('data/actors.json') as data_file:
    #         list_actors_original = json.load(data_file)
    #
    #     r = json.loads(result.content.decode('utf8'))
    #
    #     self.assertEqual(r, list_actors_original)

    def test_list_actor_channel_info(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = requests.get(HEROKU_URL+'07-05-2018/canal/'
                              'Frente_Brasil_Popular')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 200)

        channel_id = 'UCX2Aanu4fGewmhP4rf5GQ3Q'
        r = json.loads(result.content.decode('utf8'))

        self.assertEqual(r['channel_id'], channel_id)

    def test_list_actor_channel_info_with_wrong_data(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = requests.get(HEROKU_URL+'07-05/canal/Frente_Brasil_Popular')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 450)

    def test_list_actor_channel_info_with_wrong_actor_name(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = requests.get(HEROKU_URL+'07-05-2018/canal/Frente')

        # Verifica o código de estado da resposta da requisição
        self.assertEqual(result.status_code, 460)


if __name__ == '__main__':
    unittest.main()
