from google_sheets_utils import *


class GoogleSheets:
    def __init__(self, creds_path: str):
        self.creds = Credentials.from_service_account_file(creds_path)
        self.service = build('sheets', 'v4', credentials=self.creds)

    def __req_update(self, spreadsheet: str, body: dict, retries: int = 5) -> dict:
        for retry in range(retries):
            try:
                request = self.service.spreadsheets().values().batchUpdate(
                    spreadsheetId=spreadsheet,
                    body=body
                )
                return request.execute()
            except Exception as error:
                err_type = exceptions_handler_for_requests(error)
                if not err_type:
                    continue
                else:
                    raise

    def __req_get(
            self, spreadsheet: str, range_: str, value_render_option: str | None = None,
            major_dimension: str | None = None, retries: int = 5
    ) -> list:
        for retry in range(retries):
            try:
                request = self.service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet,
                    range=range_,
                    valueRenderOption=value_render_option,
                    majorDimension=major_dimension
                )
                return request.execute().get('values')
            except Exception as error:
                err_type = exceptions_handler_for_requests(error)
                if not err_type:
                    continue
                else:
                    raise

    def __req_get_info(self, spreadsheet: str, retries: int = 5) -> dict:
        for retry in range(retries):
            try:
                request = self.service.spreadsheets().get(spreadsheetId=spreadsheet)
                return request.execute()
            except Exception as error:
                err_type = exceptions_handler_for_requests(error)
                if not err_type:
                    continue
                else:
                    raise

    def __req_update_info(self, spreadsheet: str, body: dict, retries: int = 5) -> dict:
        for retry in range(retries):
            try:
                request = self.service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet,
                    body=body
                )
                return request.execute()
            except Exception as error:
                err_type = exceptions_handler_for_requests(error)
                if not err_type:
                    continue
                raise

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

    def get_sheets_name(self, spreadsheet: str) -> list:
        """
        Gets the list of sheets names in spreadsheet.
        :param spreadsheet: Spreadsheet ID. (string)
        :return: List with sheet names.
        """
        sheets = []
        response = self.__req_get_info(spreadsheet)
        for sheet in response.get('sheets'):
            sheets.append(sheet.get('properties').get('title'))
        return sheets

    def rows_count(self, spreadsheet: str, worksheet: str | list) -> int:
        """
        Gets the total number of rows in the specified worksheets.
        :param spreadsheet: Spreadsheet ID.
        :param worksheet: String or list with worksheet name.
        :return: Total number of rows from specified worksheets.
        """
        row_count = 0
        response = self.__req_get_info(spreadsheet).get('sheets')
        if response:
            for sheet in response:
                if sheet.get('properties').get('title') in worksheet:
                    row_count += sheet.get('properties').get('gridProperties').get('rowCount')
        return row_count

    def columns_count(self, spreadsheet: str, worksheet: str | list) -> int:
        """
        Gets the total number of columns in the specified worksheets.
        :param spreadsheet: Spreadsheet ID.
        :param worksheet: String or list with worksheet name.
        :return: Total number of columns from specified worksheets.
        """
        column_count = 0
        response = self.__req_get_info(spreadsheet).get('sheets')
        if response:
            for sheet in response:
                if sheet.get('properties').get('title') in worksheet:
                    column_count += sheet.get('properties').get('gridProperties').get('columnCount')
        return column_count

    def get_column_index_by_column_name(
            self, spreadsheet: str, worksheet: str, column_name: str
    ) -> int | None:
        """
        Function for getting the index of the column by its name.
        :param spreadsheet: Spreadsheet ID.
        :param worksheet: Worksheet name.
        :param column_name: Column name.
        :return: Returns index of the column
        """
        columns = self.get_columns_names(spreadsheet, worksheet)
        if columns:
            if column_name in columns:
                return columns.index(column_name)
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
        try:
            first_row = [to_low(elem) for elem in worksheet_data[0]]
        except KeyError:
            raise KeyError('Did not find any data in the worksheet.')
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

    def get_sheet_id_by_name(self, spreadsheet: str, sheet_name: str) -> int | None:
        """
        Function for getting the ID of the sheet by its name.
        :param spreadsheet: Spreadsheet ID. (string)
        :param sheet_name: Sheet name. (string)
        :return: Returns the ID of the sheet.
        """
        request = self.__req_get_info(spreadsheet).get('sheets')
        if request:
            for sheet in request:
                if sheet.get('properties').get('title') == sheet_name:
                    return sheet.get('properties').get('sheetId')
        return None

    def create_new_sheet(self, spreadsheet: str, sheet_name: str) -> dict:
        """
        Function for creating a new sheet in the spreadsheet.
        :param spreadsheet: Spreadsheet ID. (string)
        :param sheet_name: Sheet name. (string)
        :return: Returns a dictionary with a response from the Google Sheets API.
        """

        body = {
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }
            ]
        }

        return self.__req_update_info(spreadsheet, body)

    def delete_sheet(
            self, spreadsheet: str, sheet_name: str | None = None, sheet_id: int | None = None
    ) -> dict | None:
        """
        Function for deleting a sheet in the spreadsheet.
        :param spreadsheet: Spreadsheet ID. (string)
        :param sheet_name: Sheet name. (string)
        :param sheet_id: Need to specify the sheet ID if the sheet name is not unique. (int | None)
        :return: Returns a dictionary with a response from the Google Sheets API.
        """

        if sheet_name and not sheet_id:
            sheet_id = self.get_sheet_id_by_name(spreadsheet, sheet_name)

        if not sheet_id:
            return None

        body = {
            'requests': [
                {
                    'deleteSheet': {
                        'sheetId': sheet_id
                    }
                }
            ]
        }

        return self.__req_update_info(spreadsheet, body)

    def rename_sheet(self, spreadsheet: str, old_name: str, new_name: str) -> dict | None:
        """
        Function for renaming a sheet in the spreadsheet.
        :param spreadsheet: Spreadsheet ID. (string)
        :param old_name: Old sheet name. (string)
        :param new_name: New sheet name. (string)
        :return: Returns a dictionary with a response from the Google Sheets API.
        """

        if old_name == new_name:
            return None

        old_sheet_id = self.get_sheet_id_by_name(spreadsheet, old_name)
        if old_sheet_id is None:
            return None

        body = {
            'requests': [
                {
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': old_sheet_id,
                            'title': new_name
                        },
                        'fields': 'title'
                    }
                }
            ]
        }

        return self.__req_update_info(spreadsheet, body)

    def clear_range(
            self, spreadsheet: str, start_row: int, end_row: int, start_col: int, end_col: int,
            sheet_name: str | None = None, sheet_id: int | None = None,
    ) -> dict | None:
        """
        Function for clearing a range in the spreadsheet.
        :param spreadsheet: Spreadsheet ID. (string)
        :param start_row: Start row. (int)
        :param end_row: End row. (int)
        :param start_col: Start column. (int)
        :param end_col: End column. (int)
        :param sheet_name: Sheet name. (string)
        :param sheet_id: Need to specify the sheet ID if the sheet name is not unique. (int | None)
        :return: Returns a dictionary with a response from the Google Sheets API.
        """

        if sheet_name and not sheet_id:
            sheet_id = self.get_sheet_id_by_name(spreadsheet, sheet_name)

        if not sheet_id:
            return None

        body = {
            'requests': [
                {
                    'updateCells': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': start_row - 1,
                            'endRowIndex': end_row,
                            'startColumnIndex': start_col - 1,
                            'endColumnIndex': end_col
                        },
                        'fields': 'userEnteredValue'
                    }
                }
            ]
        }

        return self.__req_update_info(spreadsheet, body)

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
