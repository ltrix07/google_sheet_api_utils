import time
from ssl import SSLError
from typing import Any, List
import gspread.utils
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest
from google.auth.transport.requests import AuthorizedSession
from google_sheets_utils import *
from google_sheets_utils.text_handler import all_to_low_and_del_spc as to_low


class GoogleSheets:
    def __init__(self, creds_path: str):
        self.creds = Credentials.from_service_account_file(creds_path)
        self.service = build('sheets', 'v4', credentials=self.creds)

    def __req_update(self, spreadsheet: str, body: dict, retries: int = 5) -> dict:
        errors = {'status': 'error'}
        for retry in range(retries):
            try:
                request = self.service.spreadsheets().values().batchUpdate(
                    spreadsheetId=spreadsheet,
                    body=body
                )
                response = request.execute()
                return response
            except HttpError as error:
                errors[error] = error.content
                return errors
            except SSLError as error:
                errors[error] = error.errno
                time.sleep(3)
                continue
            except TimeoutError as error:
                errors[error] = error.errno
                time.sleep(3)
                continue

        return errors

    def __req_get(
            self, spreadsheet: str, range_: str, value_render_option: str | None = None,
            major_dimension: str | None = None, retries: int = 5
    ) -> list | dict:
        errors = {'status': 'error'}
        for retry in range(retries):
            try:
                request = self.service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet,
                    range=range_,
                    valueRenderOption=value_render_option,
                    majorDimension=major_dimension
                )
                response = request.execute()
                return response['values']
            except HttpError as error:
                errors[error] = error.content
                return errors
            except SSLError as error:
                errors[error] = error.errno
                time.sleep(3)
                continue
            except TimeoutError as error:
                errors[error] = error.errno
                time.sleep(10)
                continue

        return errors

    @staticmethod
    def __collect_body(indices: list, worksheet: str, value_input_option: str, major_dimension: str) -> dict:
        body = {
            'valueInputOption': value_input_option,
            'data': []
        }
        for data_dict in indices:
            start_row = 1
            col = data_dict.get('col')
            data = data_dict.get('data')
            if data_dict.get('row'):
                start_row = data_dict.get('row')

            start_range = gspread.utils.rowcol_to_a1(start_row, col)
            end_range = gspread.utils.rowcol_to_a1(start_row + len(data), col + len(data[0]))

            body['data'].append(
                {
                    'range': f'{worksheet}!{start_range}:{end_range}',
                    'majorDimension': major_dimension,
                    'values': data
                }
            )
        return body

    def get_column_index_by_column_name(
            self, spreadsheet: str, worksheet: str, column_name: str
    ) -> int | None:
        columns = self.get_columns_names(spreadsheet, worksheet)
        if columns:
            return columns.get(column_name)
        else:
            return None

    def get_all_info_from_sheet(
            self, spreadsheet: str, worksheet: str, value_render_option: str | None = None,
            major_dimension: str | None = None
    ) -> list:
        """
        Function get all info from spreadsheet.

        :param spreadsheet: spreadsheet ID.
        :param worksheet: worksheet name.
        :param value_render_option: ValueRenderOption. Can take values "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"
        :param major_dimension: Dimension. (string | None)
        "DIMENSION_UNSPECIFIED" - Default value, do not use.
        "ROWS" - Work with sheet rows.
        "COLUMNS" - Work with sheet columns.
        :return: All data from the table as a matrix.
        """

        return self.__req_get(spreadsheet, worksheet, value_render_option, major_dimension)

    @staticmethod
    def get_columns_indices(worksheet_data: list, columns: dict) -> dict | None:
        """
        Function for determining the index of the required columns relative to a pre-specified dictionary
        with the name of these columns (case and tabulation are omitted).

        :param worksheet_data: All the data from the table is in matrix format.
        :param columns: Headword. key is the definition of the column. value is its actual name in the table.
        :return: Dictionary as a key the column name (specified in the head dictionary),
        the value is the column index.
        """

        columns_indices = {}
        first_row = [to_low(elem) for elem in worksheet_data[0]]
        for key, value in columns.items():
            if to_low(value) in first_row:
                columns_indices[key] = first_row.index(to_low(value))

        return columns_indices

    def get_columns_names(
            self, spreadsheet: str, worksheet: str, value_render_option: str | None = None
    ) -> list:
        """
        Function for getting the names of the columns in the table.
        :param spreadsheet: Spreadsheet ID.
        :param worksheet: Worksheet name.
        :param value_render_option: ValueRenderOption. Can take values "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"
        :return: List with column names.
        """
        first_row = self.__req_get(spreadsheet, worksheet + '!1:1', value_render_option)
        return first_row[0]

    def get_column_index_by_name(
            self, spreadsheet: str | None, worksheet: str | None,
            column_name: str, columns_row: list | None = None
    ) -> int | None:
        """
        Function for getting the index of the column by its name.
        Must be specified spreadsheet and worksheet or the column_row.
        :param spreadsheet: Spreadsheet ID.
        :param worksheet: Worksheet name.
        :param column_name: Column name.
        :param columns_row: Row with column names from table. If not specified, the first row is used.
        :return: Index of the column.
        """
        if not columns_row:
            columns_row = [to_low(elem) for elem in self.get_columns_names(spreadsheet, worksheet)]
            return columns_row.index(to_low(column_name))
        else:
            columns_row = [to_low(elem) for elem in columns_row]
            return columns_row.index(to_low(column_name))

    def get_data_by_column_name(
            self, spreadsheet: str, worksheet: str, col_name: str, value_render_option: str | None = None,
            like_matrix: bool = False
    ) -> list | None:
        """
        Allows you to retrieve data from the specified column. Tabs and spaces are omitted.
        :param spreadsheet: Spreadsheet ID.
        :param worksheet: Worksheet name.
        :param col_name: Column name with data.
        :param value_render_option: ValueRenderOption. Can take values "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"
        :param like_matrix: Return as a matrix or as a regular list.
        :return: List with data.
        """

        all_data = self.__req_get(spreadsheet, worksheet, value_render_option)
        first_row = [to_low(elem) for elem in all_data[0]]
        if to_low(col_name) in first_row:
            index = first_row.index(to_low(col_name))
            if like_matrix:
                return [[row[index]] for row in all_data]
            else:
                return [row[index] for row in all_data]
        else:
            return None

    def update_sheet(
            self, spreadsheet: str, range_: str,
            data: list, value_input_option: str = 'USER_ENTERED',
            major_dimension: str = 'DIMENSION_UNSPECIFIED'
    ) -> dict:
        """
        Writes data to the table relative to the specified diapason.
        :param spreadsheet: Spreadsheet ID. (string)
        :param range_: Range for writing. Exemple: "Sheet1!A1:C3". (string)
        :param data: Data to be written. (list)
        :param value_input_option: ValueInputOption. Can take values "RAW", "USER_ENTERED". (string | None)
        :param major_dimension: majorDimension. Can take values "ROWS", "COLUMNS".
        :return: Returns a dictionary with a response from the Google Sheets API.
        """

        body = {
            'valueInputOption': value_input_option,
            'data': [
                {
                    'range': range_,
                    'majorDimension': major_dimension,
                    'values': data
                }
            ]
        }

        return self.__req_update(spreadsheet, body)

    def update_sheet_by_indices(
            self, spreadsheet: str, worksheet: str,
            indices: list, value_input_option: str = 'USER_ENTERED',
            major_dimension: str = 'DIMENSION_UNSPECIFIED', chunk_size: int = 1000
    ) -> list[dict]:
        """
        Enters data into the table with respect to
        indices and values specified in the 'indices' dictionary.
        :param chunk_size: Size of the chunk.
        :param spreadsheet: Spreadsheet ID. (string)
        :param worksheet: Worksheet name. (string)
        :param indices: List with dictionary with index and data indices = [{'col': int, 'data': list}]
        :param major_dimension: majorDimension. Can take values "ROWS", "COLUMNS".
        :param value_input_option: ValueInputOption. Can take values "RAW", "USER_ENTERED". (string | None)
        :return: Returns a dictionary with a response from the Google Sheets API.
        """
        responses = []
        if len(indices) < chunk_size:
            body = self.__collect_body(indices, worksheet, value_input_option, major_dimension)
            return [self.__req_update(spreadsheet, body)]
        else:
            for _ in range(0, len(indices), chunk_size):
                body = self.__collect_body(indices[_:_ + chunk_size], worksheet, value_input_option, major_dimension)
                responses.append(self.__req_update(spreadsheet, body))

        return responses
