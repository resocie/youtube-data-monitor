import requests
import unittest
import json


class TestHeroku(unittest.TestCase):
    def test_home_status_code(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = requests.get('https://youtube-data-monitor.herokuapp.com/')

        # Verifica o código de estado da resposta da requisição
        #   Se for sucesso irá retornar 200
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = requests.get('https://youtube-data-monitor.herokuapp.com/')

        # Verifica o dado da resposta do caminho da página inicial
        self.assertEqual(result.content.decode("utf-8"), "Hello World.")

    def test_get_actor_name_example(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = requests.get(
                    'https://youtube-data-monitor.herokuapp.com/actor/example')

        self.assertEqual(result.content.decode("utf-8"),
                         "actor name : example")

    def test_get_actor_name_json_example(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = requests.get(
              'https://youtube-data-monitor.herokuapp.com/actorjson/example')
        r = json.loads(result.content.decode('utf8'))

        self.assertEqual(r, {'actor_name': 'example'})


if __name__ == '__main__':
    unittest.main()
