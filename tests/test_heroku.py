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

        def test_list_actors(self):
            # Envia uma requisição HTTP GET para a aplicação
            result = requests.get(
                'https://youtube-data-monitor.herokuapp.com/actors')

            # Verifica o código de estado da resposta da requisição
            self.assertEqual(result.status_code, 200)

            with open('data/actors.json') as data_file:
                list_actors_original = json.load(data_file)

            r = json.loads(result.content.decode('utf8'))

            self.assertEqual(r, list_actors_original)


if __name__ == '__main__':
    unittest.main()
