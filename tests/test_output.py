from core import FileOutput
import unittest
import os


class TestOutput(unittest.TestCase):
    def test_raise_value_error_with_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            FileOutput('file.csv').export_to_CSV('')

        self.assertTrue('O tipo do dado está incorreto.' in
                        str(context.exception))

    def test_raise_value_error_with_invalid_path(self):
        with self.assertRaises(ValueError) as context:
            FileOutput('wrong_folder/file.csv').export_to_CSV([{}])

        self.assertTrue('Nome do arquivo ou caminho incorreto.' in
                        str(context.exception))

    def test_save_file_without_headers(self):
        data = [
            {'First': 'f1', 'Second': 's1'},
            {'First': 'f2', 'Second': 's2'},
            {'First': 'f3', 'Second': 's3'},
            {'First': 'f4', 'Second': 's4'}
        ]
        filename = 'tests/test_file_output.csv'
        result = FileOutput(filename).export_to_CSV(data)

        self.assertTrue(result)
        self.remove_file(filename, result)

    def test_save_file_with_valid_headers(self):
        headers = ['First', 'Second', 'Third']
        data = [
            {'First': 'f1', 'Second': 's1', 'Third': ''},
            {'First': 'f2', 'Second': 's2', 'Third' : 't1'}
        ]
        filename = 'tests/test_file_output.csv'
        result = FileOutput(filename).export_to_CSV(data, headers)

        self.assertTrue(result)
        self.remove_file(filename, result)

    def test_raise_value_error_when_save_file_with_invalid_header_on_data(self):
        headers = ['First', 'Second']
        data = [
            {'First': 'f1', 'S': 's1'},
            {'First': 'f2', 'S': 's2'}
        ]
        filename = 'tests/test_file_output.csv'

        with self.assertRaises(ValueError) as context:
            FileOutput(filename).export_to_CSV(data, headers)

        self.assertTrue('O tipo do dado está incorreto.' in
                        str(context.exception))

    def remove_file(self, filename, result):
        if result:
            # remove file after test
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
