import unittest
import csv
import os

class FileOutput:

    # input_data has to be a list of dictionaries, e.g. [{}]
    def __init__(self, input_data):
        self.input_data = input_data

    # Creates a csv file with the content of self.input_data
    #   filename default value 'output.csv'
    def export_CSV(self, filename = 'output.csv'):
        try:
            csv_file = open(filename, 'w')
            writer = csv.DictWriter(csv_file, self.input_data[0].keys(),
                                    quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for item in self.input_data:
                writer.writerow((item))
            csv_file.close()
        except (FileNotFoundError, UnboundLocalError):
            return 'ERROR: Nome do arquivo ou caminho incorreto'
        except (AttributeError, IndexError):
            csv_file.close()
            os.remove(filename)
            return 'ERROR: O tipo do dado está incorreto'
        else:
            return os.path.isfile(filename);
