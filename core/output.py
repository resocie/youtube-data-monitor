import unittest
import csv
import os

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class FileOutput:

    def __init__(self, filename=''):
        self._filename = filename
        self._result = dotdict({'status': False, 'error_msg': ''})

    def insert_data(self, param, value, field_name, field_value):
        data = self.get_data()
        if not data:
            return 'ERROR: Planilha danificada'

        for row in data:
            if row[field_name] == field_value:
                row[param] = value

        headers = data[0].keys()

        with open(self._filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers,
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(data)

    def get_data(self, param='', data=''):
        with open(self._filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames

            if not param and not data:
                return list(reader)

            for row in reader:
                if row[param] == data:
                    row.pop(param)
                    return row

    # Creates a csv file with the content of input_data
    #   input_data has to be a list of dictionaries, e.g. [{}]
    #   If no header is passed, than the keys of the first value of input_data
    #   list will become the headers
    def export_CSV(self, input_data=[], headers=[]):
        try:
            if not self._filename:
                self._result.error_msg = 'ERROR: Nome do arquivo não informado'
                return self._result

            csv_file = open(self._filename, 'w')
            if not headers:
                headers = input_data[0].keys()

            writer = csv.DictWriter(csv_file, fieldnames=headers,
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

            writer.writeheader()
            writer.writerows(input_data)
            csv_file.close()
        except (FileNotFoundError, UnboundLocalError):
            self._result.error_msg = 'ERROR: Nome do arquivo ou caminho incorreto'
            return self._result
        except (AttributeError, IndexError, ValueError):
            csv_file.close()
            os.remove(self._filename)
            self._result.error_msg = 'ERROR: O tipo do dado está incorreto'
            return self._result
        else:
            self._result.status = os.path.isfile(self._filename);
            return self._result
