from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-Parser/creds.json')

indices = [
    {
        'col': 3,
        'data': [['data'], [1], [34], [112]]
    },
    {
        'col': 6,
        'row': 6,
        'data': [['lol', 'BLS']]
    }
]

print(google.update_sheet_by_indices(TEST_SPREADSHEET_ID, TEST_WORKSHEET_WRITE,
                                     indices))
