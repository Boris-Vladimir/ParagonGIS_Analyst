"""
@python version:
    Python 3.3

@summary:
    Control composed by the XlsControl() class, which reads data from
    an EXEL file and return them in a form of a list.
    The class has two public functions:
        - __init__(file_name),
        - read_exel().

@note:
    function __init__(file_name):
        Class constructor.
        Take as parameters the name of the EXEL file.

    function read_exel():
        Reads the names of the EXEL sheets and append them to a list.
        Then, reads all the cells from that sheets and append their
        values to another list.
        At last, returns a list which combines the sheet names and the
        cell values.

@author:
    Venâncio 2000644

@contact:
    venancio.gnr@gmail.com

@organization:
    SDATO - DP - UAF - GNR

@version:
    1.0 (14/11/2013):
        - Creation of the function abrir_exel(ficheiro)

    1.1 (18/11/2013):
        - Implementation of the XlsControl() class.
        - Update of the abrir_exel() function, which is now named
            read_exel():
            - The EXEL cell values to append to the list, are now
              formated according they are Unicode, ints, floats or
              EXEL datetime values.

    1.2 (06/12/2013):
        - Translation of all comments to english and limitation of the
          maximum line lenght. Following the rules of the PEP 8,
          Style Guide for Python Code, writed by Guido van Rossum,
          Barry Warsaw and Nick Coghlan:
            - "Python coders from non-English speaking countries: please
              write your comments in English, unless you are 120 per
              cent sure that the code will never be read by people who
              don't speak your language."
            - "Limit all lines to a maximum of 79 characters. For
              flowing long blocks of text with fewer structural
              restrictions (docstrings or comments), the line length
              should be limited to 72 characters."
        - Changed the python version to 3.3

    1.3 (09/04/2014):
        - Added a call to the new class FistRowChecker() which breaks the
            program if the first four columns of the Excel file aren't
                - latitude
                - longitude
                - name
                - description

@since:
    14/11/2013
"""

from itertools import zip_longest  # to combine lists
import xlrd  # to read EXEL files
#from first_row_checker import FirstRowChecker


class XlsControl(object):
    '''
    Reads the data of an EXEL file and returns a list.
    '''

    def __init__(self, file_name):
        '''
        str -> Xlscontrol() object

        file_name is the name of the EXEL file.
        '''
        self.file_name = file_name

    def read_excel(self):
        '''
        None -> list

        Reads the names of the EXEL books and append them to a list.
        Then, reads all the cells from that books and append their
        values to another list.
        At last, returns a list which combines the book names and the
        cell values.
        '''

        workbook = xlrd.open_workbook(self.file_name)  # xlrd() object
        worksheet_names = [x for x in workbook.sheet_names()]  # sheet names
        worksheets = []  # cell values of all sheets

        # Construction of the worksheets list --------------------------
        for name in worksheet_names:
            worksheet = workbook.sheet_by_name(name)  # sheet.Sheet()
            num_rows = worksheet.nrows - 1  # total num of rows
            num_cells = worksheet.ncols - 1  # total num of columns
            curr_row = - 1  # current row
            data_rows = []  # data from all rows

            while curr_row < num_rows:
                data_row = []  # data from the current row
                curr_row += 1
                curr_cell = - 1

                while curr_cell < num_cells:
                    curr_cell += 1
                    cell_value = worksheet.cell_value(curr_row, curr_cell)
                    # Formatation of the cell values to append: --------
                    # in Exel all ints are floats termined in .0 -------
                    if type(cell_value) is float and str(
                            cell_value)[-2:] == ".0" and \
                            worksheet.cell_type(curr_row, curr_cell) != 3:
                        data_row.append(int(cell_value))
                    # datetime -----------------------------------------
                    elif worksheet.cell_type(curr_row, curr_cell) == 3:
                        data_row.append(
                            xlrd.xldate_as_tuple(abs(cell_value), 0))
                    elif type(cell_value) is float:  # real floats -----
                        data_row.append(cell_value)
                    else:  # unicode -----------------------------------
                        try:  # In some files all values are unicode, so
                            if str(cell_value[-2] == ".0"):
                                data_row.append(int(cell_value))
                            else:
                                data_row.append(float(cell_value))
                        except:
                            data_row.append(cell_value)

                data_rows.append(data_row)

            #if not FirstRowChecker(data_rows[0]).check():
            #    return 'As primeiras 4 colunas do Excel têm de ser:\n\
            #    latitude, longitude, name e description.'
            #    break
            worksheets.append(data_rows)

        # 3D list combined of the sheet names and the sheet cell values:
        # [[[1st sheet name][1st row data][2nd row data][...][Nth row data]]
        # [[2nd sheet name][1st row data][...]]...]
        return [[[x]] + y for x, y in zip_longest(worksheet_names,
                worksheets)]
