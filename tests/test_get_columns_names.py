from tests import *


google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-Parser/creds/google_creds.json')

data = google.get_columns_names(TEST_SPREADSHEET_ID, TEST_WORKSHEET_READ)
print(data)
