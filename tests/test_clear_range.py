from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-HomeDepot-Checker/creds/google_creds.json')

print(google.clear_range(
    TEST_SPREADSHEET_ID, 1, 28, 1, 4, TEST_WORKSHEET_WRITE
))
