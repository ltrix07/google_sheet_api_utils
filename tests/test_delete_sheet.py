from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-HomeDepot-Checker/creds/google_creds.json')

print(google.delete_sheet(TEST_SPREADSHEET_ID, 'test'))
