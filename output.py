import csv
import unittest

class Output:

    def __init__(self,input): # input is a list of dictionaries
        self.inputdata = input

    def exportCSV(self,filename): #creates a csv file with the content of self.inputdata
        try:
            f = open(filename, 'w')
            writer = csv.DictWriter(f, self.inputdata[0].keys(), quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for item in self.inputdata:
                writer.writerow((item))
        except (FileNotFoundError, UnboundLocalError):
            return 'ERROR: Não passou o nome do arquivo'
        except (AttributeError, IndexError):
            return 'ERROR: O tipo do dado está incorreto'
        else:
            f.close()
