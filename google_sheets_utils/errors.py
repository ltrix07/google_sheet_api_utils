from google_sheets_utils import *


def exceptions_handler_for_requests(error: Exception):
    if isinstance(error, HttpError):
        return 'HttpError'
    elif isinstance(error, SSLError):
        print(error)
        time.sleep(3)
        return None
    elif isinstance(error, TimeoutError):
        print(error)
        time.sleep(3)
        return None
    else:
        return str(error)
