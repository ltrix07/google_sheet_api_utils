from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-HomeDepot-Checker/creds/google_creds.json')

print(google.get_sheets_name(TEST_SPREADSHEET_ID))
