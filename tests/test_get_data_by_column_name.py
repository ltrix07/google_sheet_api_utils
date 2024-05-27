from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-Parser/creds.json')

print(google.get_data_by_column_name(TEST_SPREADSHEET_ID, TEST_WORKSHEET_READ, 'col 11'))
print(google.get_data_by_column_name(TEST_SPREADSHEET_ID, TEST_WORKSHEET_READ, 'col 11', like_matrix=True))
