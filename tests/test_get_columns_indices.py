from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-Parser/creds.json')

data = google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET)
columns = {
    'col1': 'COl 11',
    'col2': 'coll213',
    'col3': 'aslkls dw dd qd sqew'
}

indices = google.get_columns_indices(data, columns)

print(indices)
