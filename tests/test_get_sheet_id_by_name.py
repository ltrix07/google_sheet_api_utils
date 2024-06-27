from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-HomeDepot-Checker/creds/google_creds.json')
print(google.get_sheet_id_by_name(TEST_SPREADSHEET_ID, 'test'))
