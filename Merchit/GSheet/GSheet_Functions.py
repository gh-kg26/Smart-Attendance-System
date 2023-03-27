from google.oauth2 import service_account
from googleapiclient.discovery import build

import pandas as pd

SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


SAMPLE_SPREADSHEET_ID = '1Xp3mBGgSs7l1e14ASnEonzUqo0LaVwImZGWK4tZBgXU'

service = build('sheets', 'v4', credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()

def read_sheet_as_df_with_headers(sheet_name):
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID , range=sheet_name).execute()
    values = result.get('values', [])
    # return values
    sheet_df = pd.DataFrame(values[1:],columns=values[0])
    return sheet_df

def update_bulk_sheet(sheet_name):
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, \
    range="GSHEET!B2", 
    valueInputOption="RAW", 
    body={"values":aoa}
    ).execute()
    # return values
    sheet_df = pd.DataFrame(values[1:],columns=values[0])
    return sheet_df

GSHEET_df = read_sheet_as_df_with_headers("GSHEET")
print(GSHEET_df)