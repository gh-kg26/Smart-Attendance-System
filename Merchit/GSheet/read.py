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
# result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                             range="SAMPLE_RANGE_NAME").execute()

result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID , range="GSHEET").execute()

values = result.get('values', [])

print(values)

aoa = [["1" , "NIKHIL"] , ["2" , "AKHIL"] , ["3" , "ANUUJ"]]

request = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, \
    range="GSHEET!B2", 
    valueInputOption="RAW", 
    body={"values":aoa}
    ).execute()

print(request)

