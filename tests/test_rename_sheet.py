from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-HomeDepot-Checker/creds/google_creds.json')

print(google.rename_sheet(TEST_SPREADSHEET_ID, 'top', '234'))
