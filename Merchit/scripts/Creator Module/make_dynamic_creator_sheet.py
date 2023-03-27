from pydoc import cli
import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging

from scripts.makeCreatorSheetTemplate import generateCreatorSheetList
from scripts.update_lineitem_id import update_lineitemID
from scripts.update_single_SR_Profit import *

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Inside Creator Sheet Dynamic Function')

def makeCreatorSheetDynamic(wksConfirmed):

    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)

    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')


    # SauravSinhaAccounts = client.open('Saurav Sinha Accounts')
    # wksSauravSinhaOrders = SauravSinhaAccounts.worksheet_by_title('Orders')

    merchit_client_data = client.open('Merchit Client Data')

    wks_client_master = merchit_client_data.worksheet_by_title('Master')
    
    client_master_df = wks_client_master.get_as_df()

    sheet_names = client_master_df['Sheet Name'].tolist()
    checktag_list = client_master_df['Checktag'].tolist()
    base_price_sheet_list = client_master_df['Base Price Sheet'].tolist()
    # print(sheet_names , checktag_list)

    for i in range(0 , len(sheet_names)):

        print("UPDATING CREATOR SHEET WITH TITLE : " , sheet_names[i])

        wks_client_baseprice = merchit_client_data.worksheet_by_title(base_price_sheet_list[i])
        CreatorAccountsSheet = client.open(sheet_names[i])
        wksCreatorOrders = CreatorAccountsSheet.worksheet_by_title('Orders')

        # update_lineitemID(wksCreatorOrders , wksConfirmed)

        generateCreatorSheetList(wksConfirmed , checktag_list[i] , wksCreatorOrders)

        update_tracking_status(wksCreatorOrders , wks_client_baseprice)
                                                                                                                                                                  

