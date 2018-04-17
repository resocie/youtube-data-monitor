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
        self.filename = filename
        self.result = dotdict({'status': False, 'error_msg': ''})

    # Creates a csv file with the content of input_data
    #   input_data has to be a list of dictionaries, e.g. [{}]
    #   If no header is passed, than the keys of the first value of input_data
    #   list will become the headers
    def export_CSV(self, input_data, headers=[]):
        try:
            if not self.filename:
                self.result.error_msg = 'ERROR: Nome do arquivo não informado'
                return self.result

            csv_file = open(self.filename, 'w')
            if not headers:
                headers = input_data[0].keys()

            writer = csv.DictWriter(csv_file, fieldnames=headers,
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

            writer.writeheader()
            for item in input_data:
                writer.writerow((item))
            csv_file.close()
        except (FileNotFoundError, UnboundLocalError):
            self.result.error_msg = 'ERROR: Nome do arquivo ou caminho incorreto'
            return self.result
        except (AttributeError, IndexError, ValueError):
            csv_file.close()
            os.remove(self.filename)
            self.result.error_msg = 'ERROR: O tipo do dado está incorreto'
            return self.result
        else:
            self.result.status = os.path.isfile(self.filename);
            return self.result
