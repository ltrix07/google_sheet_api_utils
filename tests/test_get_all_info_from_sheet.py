from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-HomeDepot-Checker/creds/google_creds.json')

print(google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET_READ))
print(google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET_READ, 'FORMATTED_VALUE'))
print(google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET_READ, 'UNFORMATTED_VALUE'))
print(google.get_all_info_from_sheet(TEST_SPREADSHEET_ID, TEST_WORKSHEET_READ, 'FORMULA'))
