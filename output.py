import csv
import unittest
from os import remove,path

class Output:

    def __init__(self,input): # input is a list of dictionaries
        self.inputdata = input

    def exportCSV(self,filename = 'output.csv'): #creates a csv file with the content of self.inputdata
        try:
            f = open(filename, 'w')
            writer = csv.DictWriter(f, self.inputdata[0].keys(), quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for item in self.inputdata:
                writer.writerow((item))
            f.close()
        except (FileNotFoundError, UnboundLocalError):
            return 'ERROR: Nome do arquivo ou caminho incorreto'
        except (AttributeError, IndexError):
            f.close()
            remove(filename)
            return 'ERROR: O tipo do dado está incorreto'
        else:
            return path.isfile(filename);
