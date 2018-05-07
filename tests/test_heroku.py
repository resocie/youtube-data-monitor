from website.main import app
import requests
import unittest


class TestHeroku(unittest.TestCase):
    def test_home_status_code(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = resquests.get('https://youtube-data-monitor.herokuapp.com/')

        # Verifica o código de estado da resposta da requisição
        #   Se for sucesso irá retornar 200
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # Envia uma requisição HTTP GET para a aplicação
        result = resquests.get('https://youtube-data-monitor.herokuapp.com/')

        # Verifica o dado da resposta do caminho da página inicial
        self.assertEqual(result.data.decode("utf-8") , "Hello World.")

if __name__ == '__main__':
    unittest.main()
