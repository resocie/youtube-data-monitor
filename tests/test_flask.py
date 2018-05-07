from website.main import app
import unittest
import json

class TestFlask(unittest.TestCase):
    def setUp(self):
        # Cria um cliente de teste
        self.app = app.test_client()
        # Propaga as exceções para o cliente de teste
        self.app.testing = True

    def test_home_status_code(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/')

        # Verifica o código de estado da resposta da requisição
        #   Se for sucesso irá retornar 200
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/')

        self.assertEqual(result.data.decode("utf-8") , "Hello World.")

    def test_get_actor_name_example(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/actor/example')

        self.assertEqual(result.data.decode("utf-8") , "actor name : example")

    def test_get_actor_name_json_example(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = self.app.get('/actorjson/example')
        r = json.loads(result.data.decode('utf8'))
        
        self.assertEqual(r , {'actor_name' : 'example'})

if __name__ == '__main__':
    unittest.main()
