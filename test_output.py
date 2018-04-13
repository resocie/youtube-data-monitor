from output import Output
import unittest

class TestOutput(unittest.TestCase):
    def test_has_filename(self):
        data = [{}]
        self.out = Output(data)
        result = self.out.exportCSV('')
        self.assertEqual(result, 'ERROR: Não passou o nome do arquivo')

    def test_valid_data(self):
        data = ''
        self.out = Output(data)
        result = self.out.exportCSV('file.csv')
        self.assertEqual(result, 'ERROR: O tipo do dado está incorreto')

if __name__ == '__main__':
    unittest.main()
