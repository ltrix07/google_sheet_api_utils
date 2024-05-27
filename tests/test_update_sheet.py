from tests import *

google = GoogleSheets('/home/black_bounty/PycharmProjects/Amazon-Parser/creds.json')

data = [
    ['1', 'hello', 111],
    [2, '', 333]
]

response = google.update_sheet(TEST_SPREADSHEET_ID, f'{TEST_WORKSHEET_WRITE}!A1:C2',
                               data)
print(response)
