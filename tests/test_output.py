from output import Output
import unittest
from os import remove,path

class TestOutput(unittest.TestCase):
    def test_valid_data(self):
        data = ''
        self.out = Output(data)
        result = self.out.exportCSV('file.csv')
        self.assertEqual(result, 'ERROR: O tipo do dado está incorreto')

    def test_valid_path(self):
        data = [{}]
        self.out = Output(data)
        result = self.out.exportCSV('wrong_folder/file.csv')
        self.assertEqual(result, 'ERROR: Nome do arquivo ou caminho incorreto')

    def test_save_file(self):
        data=[{'key1': 'value1.1','key2': 'value2.1'},
              {'key1': 'value2.1','key2': 'value2.2'},
              {'key1': 'value3.1','key2': 'value3.2'},
             ]
        filename = 'tests/test_file_output'
        self.out = Output(data)
        result = self.out.exportCSV(filename)
        self.assertTrue(result)
        if(result):
            remove(filename) #remove file after test

if __name__ == '__main__':
    unittest.main()
