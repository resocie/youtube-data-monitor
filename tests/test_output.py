from core.output import FileOutput
import unittest
import os

class TestOutput(unittest.TestCase):
    def test_invalid_data_and_valid_filename(self):
        data = ''
        filename = 'file.csv'
        self.assertEqual(FileOutput(data).export_CSV(filename),
                        'ERROR: O tipo do dado está incorreto')

    def test_invalid_path_and_valid_data(self):
        data = [{}]
        filename = 'wrong_folder/file.csv'
        self.assertEqual(FileOutput(data).export_CSV(filename),
                         'ERROR: Nome do arquivo ou caminho incorreto')

    def test_save_file_with_valid_data_and_valid_path(self):
        data = [
            {'key1': 'value1.1', 'key2': 'value2.1'},
            {'key1': 'value2.1', 'key2': 'value2.2'},
            {'key1': 'value3.1', 'key2': 'value3.2'},
        ]
        filename = 'tests/test_file_output.csv'
        result = FileOutput(data).export_CSV(filename)
        self.assertTrue(result)
        if result :
            # remove file after test
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
