from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-Parser/creds.json')

print(google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET))
print(google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET, 'FORMATTED_VALUE'))
print(google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET, 'UNFORMATTED_VALUE'))
print(google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET, 'FORMULA'))
