from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-HomeDepot-Checker/creds/google_creds.json')

print(google.rows_count(TEST_SPREADSHEET_ID, TEST_WORKSHEET_READ))
