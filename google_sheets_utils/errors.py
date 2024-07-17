from google_sheets_utils import *


def exceptions_handler_for_requests(error):
    if isinstance(error, HttpError):
        status = error.status_code
        if status == 403:
            return 'forbidden'
        if status == 404:
            return 'not_found'
        else:
            return f'http_error_{status}'
    else:
        return f"{error}"
