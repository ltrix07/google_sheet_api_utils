from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-HomeDepot-Checker/creds/google_creds.json')
indices = []
for i in range(1, 2754):
    indices.append({
        'col': 1,
        'row': i,
        'data': [['hello']]
    })

print(google.update_sheet_by_indices(TEST_SPREADSHEET_ID, TEST_WORKSHEET_WRITE,
                                     indices))
