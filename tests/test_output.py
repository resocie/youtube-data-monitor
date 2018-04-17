from core.output import FileOutput
import unittest
import os

class TestOutput(unittest.TestCase):
    def test_invalid_data(self):
        data = ''
        filename = 'file.csv'
        self.assertEqual(FileOutput(filename).export_CSV(data).error_msg,
                        'ERROR: O tipo do dado está incorreto')

    def test_invalid_path(self):
        data = [{}]
        filename = 'wrong_folder/file.csv'
        self.assertEqual(FileOutput(filename).export_CSV(data).error_msg,
                         'ERROR: Nome do arquivo ou caminho incorreto')

    def test_save_file_without_headers(self):
        data = [
            {'key1': 'value1.1', 'key2': 'value2.1'},
            {'key1': 'value2.1', 'key2': 'value2.2'},
            {'key1': 'value3.1', 'key2': 'value3.2'},
            {'key1': 'value3.1', 'key2': 'value3.2'}
        ]
        filename = 'tests/test_file_output.csv'
        result = FileOutput(filename).export_CSV(data).status
        self.assertTrue(result)
        self.remove_file(filename, result)


    def test_save_file_with_valid_headers(self):
        headers = ['First', 'Second', 'Third']
        data = [
            {'First': 'f1', 'Second': 's1', 'Third': ''},
            {'First': 'f2', 'Second': 's2', 'Third' : 't1'}
        ]
        filename = 'tests/test_file_output.csv'
        result = FileOutput(filename).export_CSV(data, headers).status
        self.assertTrue(result)
        self.remove_file(filename, result)

    def test_save_file_with_invalid_header_key_on_data(self):
        headers = ['First', 'Second']
        data = [
            {'First': 'f1', 'S': 's1'},
            {'First': 'f2', 'S': 's2'}
        ]
        filename = 'tests/test_file_output.csv'
        self.assertEqual(FileOutput(filename).export_CSV(data, headers).error_msg,
                        'ERROR: O tipo do dado está incorreto')

    def remove_file(self, filename, result):
        if result:
            # remove file after tests
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
