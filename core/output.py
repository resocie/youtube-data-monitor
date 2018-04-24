import unittest
import csv
import os

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class FileOutput:
    """A file output API.

    This class is an API to get and/or insert data in a CSV.

    Args:
        filename (str): Filename to insert and/or get data.
    """

    def __init__(self, filename=None):
        # @TODO handle no filename passed
        self._filename = filename

    def insert_value(self, column, value, search_cell, search_value):
        """Insert a value in a specific cell in a specific csv file.

        Args:
            column (str): Cell name where the value will be insert.
            value (str): Value that will be insert.
            search_cell (str): Cell name to search for the search_value.
            search_value (str): Value that indicates which row is to add the
                                value.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            ValueError: If there're no data inside of the csv file.

        """

        data = self.get_all_data()

        if data:
            found = False
            for row in data:
                if row[field_name] == field_value:
                    row[param] = value
                    found = True

            if not found:
                return False

            headers = data[0].keys()

            with open(self._filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers,
                                    quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                writer.writerows(data)

            return True
        else:
            raise ValueError('Nenhum dado encontrado na planilha %s' %
                                                        self._filename)

    def get_row(self, column=None, value=None):
        """Get a row in a specific csv file.

        If there're more than one match for the column and value,
        the function returns the first match.

        Args:
            column (str): Cell name to search for the value.
            value (str): Value that indicates which row is to get.

        Returns:
            A ``list``: List with the row found, an empty row otherwise.

        """

        with open(self._filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row[param] == data:
                    row.pop(param)

                    return row

            return []

    def get_all_data(self):
        """Get all data from a csv file.

        Returns:
            A ``list`` of ``list``: Each element of the list
                                    is a row from the csv file.

        """

        with open(self._filename, 'r') as csvfile:
            return list(csv.DictReader(csvfile))

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
