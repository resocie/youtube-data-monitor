from website.main import app
import unittest
import json


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


if __name__ == '__main__':
    unittest.main()
