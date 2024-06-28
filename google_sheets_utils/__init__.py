import os.path
import gspread
import time
import time
from ssl import SSLError
from typing import Any, List
import gspread.utils
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials
from google_sheets_utils.errors import *
from google_sheets_utils.text_handler import all_to_low_and_del_spc as to_low
from ssl import SSLError
from googleapiclient.discovery import build
