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

    Raises:
        ValueError: If filename is not passed.
    """

    def __init__(self, filename):
        if not filename:
            raise ValueError('Nome do arquivo não informado.')
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
            ValueError: If there're no data inside of the csv file or
                        if a problem occurs in exporting the new CSV.

        """

        data = self.get_all_data()

        if data:
            found = False
            for row in data:
                if row[search_cell] == search_value:
                    row[column] = value
                    found = True

            if not found:
                return False

            headers = data[0].keys()

            try:
                return self.export_to_CSV(data, headers)
            except ValueError as err:
                raise err
        else:
            raise ValueError('Nenhum dado encontrado na planilha %s'
                             % self._filename)


    def insert_multiple_values(self, column, search_cell, search_value):
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
            ValueError: If there're no data inside of the csv file or
                        if a problem occurs in exporting the new CSV.

        """

        data = self.get_all_data()

        if data:
            found = False
            for row in data:
                for header in column:
                    if row[search_cell] == search_value:
                        row[header] = 'null'
                        found = True

            if not found:
                return False

            headers = data[0].keys()

            try:
                return self.export_to_CSV(data, headers)
            except ValueError as err:
                raise err
        else:
            raise ValueError('Nenhum dado encontrado na planilha %s'
                             % self._filename)

    def get_row(self, column, value):
        """Get a row in a specific csv file.

        If there're more than one match for the column and value,
        the function returns the first match.

        Args:
            column (str): Cell name to search for the value.
            value (str): Value that indicates which row is to get.

        Returns:
            ``list`` of str: List with the row found, an empty row otherwise.

        """

        with open(self._filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row[column].lower() == value.lower():
                    row.pop(column)

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

    def export_to_CSV(self, input_data, headers=[]):
        """Creates a csv file with the content of input_data.

        Args:
            input_data (``list`` of ``dict``): Data that will be insert.
            headers (``list`` of str): Columns name of the csv file. If no
                                        header is passed, than the keys of
                                        the ``dict`` from the first value of
                                        input_data will become the headers.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            ValueError: If filename/path of the filename/input_data
                        is not correct.

        """
        try:
            with open(self._filename, 'w') as csv_file:
                if not headers:
                    headers = input_data[0].keys()

                writer = csv.DictWriter(csv_file,
                                        fieldnames=headers,
                                        quotechar='"',
                                        quoting=csv.QUOTE_NONNUMERIC)

                writer.writeheader()
                writer.writerows(input_data)
        except (FileNotFoundError, UnboundLocalError):
            raise ValueError('Nome do arquivo ou caminho incorreto.')
        except (AttributeError, IndexError, ValueError):
            os.remove(self._filename)
            raise ValueError('O tipo do dado está incorreto.')
        else:
            return os.path.isfile(self._filename)
