import os
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'service_account.json'

scopes=[
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
    ]

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=scopes)

# creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/drive',
#                                               'https://www.googleapis.com/auth/drive.file',
#                                               'https://www.googleapis.com/auth/drive.metadata.readonly',
#                                               'https://www.googleapis.com/auth/spreadsheets'])


drive_service = build('drive', 'v3', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)


sheet_name = 'Sheet1'

folder_id = '1Q07R-i0OHyyR1MNCFJ7KJ52VjlCKjl2c'


try:
    results = drive_service.files().list(q=f"'{folder_id}' in parents and trashed = false", fields="nextPageToken, files(id, name, webViewLink)").execute()
    files = results.get('files', [])
except HttpError as error:
    print(f"An error occurred: {error}")
    files = []


try:
    sheet_values = sheets_service.spreadsheets().values().get(spreadsheetId='1fGLSZKHERmCC20sh4o68G-8NEuoBnnZQNwdtdQtd3s0', range=f'{sheet_name}!A2:C').execute().get('values', [])
except HttpError as error:
    print(f"An error occurred: {error}")
    sheet_values = []

 

list_file_names = []
image_links = {}
for file in files:
    name = file['name']
    list_file_names.append(file['name'])
    link = file['webViewLink']
    image_links[name] = link

# list_file_names = list_file_names.sort()
list_file_names = sorted(list_file_names)
list_list_file_names = []
list_list_file_names.append(list_file_names)
# list = [["valuea1"], ["valuea2"], ["valuea3"]]
resource = {
  "majorDimension": "COLUMNS",
  "values": list_list_file_names
}
spreadsheetId = "1fGLSZKHERmCC20sh4o68G-8NEuoBnnZQNwdtdQtd3s0"
range = "Sheet1!A:A"
sheets_service.spreadsheets().values().append(
  spreadsheetId=spreadsheetId,
  range=range,
  body=resource,
  valueInputOption="USER_ENTERED"
).execute()


try:
    sheet_values = sheets_service.spreadsheets().values().get(spreadsheetId='1fGLSZKHERmCC20sh4o68G-8NEuoBnnZQNwdtdQtd3s0', range=f'{sheet_name}!A2:C').execute().get('values', [])
except HttpError as error:
    print(f"An error occurred: {error}")
    sheet_values = []


value_range_body = {'valueInputOption': 'USER_ENTERED', 'data': []}
for row in sheet_values:
    name = row[0]
    drive_link = image_links.get(name)
    if drive_link:
        value_range_body['data'].append({'range': f"{sheet_name}!C{sheet_values.index(row)+2}",
                                         'majorDimension': 'ROWS',
                                         'values': [[drive_link]]})
if value_range_body['data']:
    try:
        sheets_service.spreadsheets().values().batchUpdate(spreadsheetId='1fGLSZKHERmCC20sh4o68G-8NEuoBnnZQNwdtdQtd3s0',
                                                            body=value_range_body).execute()
        print(f"Google Sheet {sheet_name} updated successfully.")
    except HttpError as error:
        print(f"An error occurred: {error}")
else:
    print(f"No updates to Google Sheet {sheet_name} were made.")
