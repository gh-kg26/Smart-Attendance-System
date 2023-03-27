from google.oauth2 import service_account

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '1Xp3mBGgSs7l1e14ASnEonzUqo0LaVwImZGWK4tZBgXU'

service = build('sheets', 'v4', credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()

# The A1 notation of the values to update.
range_ = 'GSHEET!A1'  # TODO: Update placeholder value.

# How the input data should be interpreted.
value_input_option = 'RAW'  # TODO: Update placeholder value.

aoa = [["Hello World"]]
value_range_body = {"values":aoa
}

request = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, body=value_range_body)
response = request.execute()

# TODO: Change code below to process the `response` dict:
print(response)