import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging


def push_to_consolidated_sheet(wksRMClientDataSheet, wks_master_data_consolidated_rm_sheet , RM_Sheet_Name, username_field, match_column , Inserted_Column):
    '''
    1. Read all data where Column "Inserted into Consolidated sheet" != TRUE
    2. Loop through that data one by one
        2.1 Check if username exists in Consolidated Master Sheet
        2.2 If yes, then in Column "Match", update FOUND IN RM_Sheet_df['RM Sheet Name'][idx] and update Column "Inserted into Consolidated sheet" = TRUE
        2.3 If no, then insert in Consolidated Master Sheet and update Column "Inserted into Consolidated sheet" = TRUE
    '''
    print("entered function")
    print(wksRMClientDataSheet)
    # Read all data where Column "Inserted into Consolidated sheet" != TRUE
    data_to_push = wksRMClientDataSheet.get_as_df().loc[wksRMClientDataSheet.get_as_df()['Inserted in Consolidated RM Sheet'] != 'TRUE']
    wks_master_data_consolidated_rm_sheet_df = wks_master_data_consolidated_rm_sheet.get_as_df()
    print("Data to push " , data_to_push )
    
    # Loop through that data one by one
    for idx in data_to_push.index:
        username = data_to_push.loc[idx][username_field]
        # email = data_to_push.loc[idx]['Email']
        # print(username)
        
        Usernames_In_Consolidated_Sheet = wks_master_data_consolidated_rm_sheet_df['Instagram User Name'].tolist()
        RM_Name_list = wks_master_data_consolidated_rm_sheet_df['RM Name'].tolist()    
    
        if username in Usernames_In_Consolidated_Sheet:
            print("FOUND")
            # cell_to_update = "E" + str(idx+2)
            cell_to_update = match_column + str(idx+2)
            # cell_to_update_true = "R" + str(idx+2)
            cell_to_update_true = Inserted_Column + str(idx+2)
            
            index_match = Usernames_In_Consolidated_Sheet.index(username)
            wksRMClientDataSheet.update_value(addr=cell_to_update_true , val="TRUE")
            wksRMClientDataSheet.update_value(addr=cell_to_update , val=f"FOUND IN {RM_Name_list[index_match]}")
            
        else:
            print("NOT FOUND")
            # cell_to_update_true = "R" + str(idx+2)
            cell_to_update_true = Inserted_Column + str(idx+2)

            wks_master_data_consolidated_rm_sheet_dff = wks_master_data_consolidated_rm_sheet.get_as_df()
            last_row = wks_master_data_consolidated_rm_sheet_dff.shape[0] + 1
            
            row_to_insert = [username, RM_Sheet_Name]
            
            wksRMClientDataSheet.update_value(addr=cell_to_update_true , val="TRUE")
            wks_master_data_consolidated_rm_sheet.insert_rows(last_row , values = row_to_insert)
            


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

try:

    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)
    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')
    merchit_client_data = client.open('Merchit Client Data')
    RM_Master_Sheet = merchit_client_data.worksheet_by_title('RM Sheet')

    consolidated_rm_sheet = client.open('Consolidated RM Sheet')
    wks_master_data_consolidated_rm_sheet = consolidated_rm_sheet.worksheet_by_title('Master Data')

    RM_Sheet_df = RM_Master_Sheet.get_as_df()
    print(RM_Sheet_df)

    for idx in RM_Sheet_df.index:
        print("Entered Loop")
        try:
            RM_Sheet = client.open(RM_Sheet_df['RM Sheet Name'][idx])
            print(RM_Sheet_df['RM Sheet Name'][idx])
            wksRMClientDataSheet = RM_Sheet.worksheet_by_title(RM_Sheet_df['Client Data Sheet Name'][idx])
            print(RM_Sheet_df['Client Data Sheet Name'][idx])
            usernames = RM_Sheet_df.loc[idx]['User Name Column']

            match_column = RM_Sheet_df.loc[idx]['Match Column']
            Inserted_Column = RM_Sheet_df.loc[idx]['Inserted in Consolidated RM Sheet']
            
            push_to_consolidated_sheet(wksRMClientDataSheet , wks_master_data_consolidated_rm_sheet , RM_Sheet_df['RM Sheet Name'][idx], usernames , match_column , Inserted_Column)
            logging.info('RM Sheet Script')



        except Exception as exception:
            print(exception)
            continue
    


except Exception as exception:
    print("Error in app.py")
    print(exception)