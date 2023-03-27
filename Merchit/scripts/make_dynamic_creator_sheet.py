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

from datetime import datetime

print("ENTERED DYNAMIC CREATOR SHEET 2")

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def makeCreatorSheetDynamic():

    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)

    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')


    # SauravSinhaAccounts = client.open('Saurav Sinha Accounts')
    # wksSauravSinhaOrders = SauravSinhaAccounts.worksheet_by_title('Orders')

    Shopify_2021_Sheet = client.open('2021-03-18 07:18 merchit-official-merch.myshopify.com - Order')
    wksDSD = Shopify_2021_Sheet.worksheet_by_title('DSD')

    merchit_client_data = client.open('Merchit Client Data')

    wks_client_master = merchit_client_data.worksheet_by_title('Master')
    
    client_master_df = wks_client_master.get_as_df()

    sheet_names = client_master_df['Sheet Name'].tolist()
    checktag_list = client_master_df['Checktag'].tolist()
    percentage_split = client_master_df['Percentage Split'].tolist()
    base_price_sheet_list = client_master_df['Base Price Sheet'].tolist()
    confirmed_sheet_master = client_master_df['Master Sheet'].tolist()

    # print(sheet_names , checktag_list)

    for i in range(0 , len(sheet_names)):

        print("UPDATING CREATOR SHEET WITH TITLE : " , sheet_names[i])

        Shopify_Sheet = client.open(confirmed_sheet_master[i])
        wks_Confirmed = Shopify_Sheet.worksheet_by_title('Confirmed')

        wks_client_baseprice = merchit_client_data.worksheet_by_title(base_price_sheet_list[i])
        CreatorAccountsSheet = client.open(sheet_names[i])
        wksCreatorOrders = CreatorAccountsSheet.worksheet_by_title('Orders')

        # update_lineitemID(wksCreatorOrders , wksConfirmed)
 
        generateCreatorSheetList(wks_Confirmed , checktag_list[i] , wksCreatorOrders)

        creator_payable_amount = update_tracking_status(wksCreatorOrders , wks_client_baseprice , wksDSD , checktag_list[i] , percentage_split[i])
        cell_to_update = "I" +str(i+2)
        date_now = str(datetime.now())
        #TIME IS BEING UPDATED
        wks_client_master.update_value(addr=cell_to_update , val=date_now)

        #TODO Update Profit
        cell_to_update_profit = "K" +str(i+2)
        #TIME IS BEING UPDATED
        wks_client_master.update_value(addr=cell_to_update_profit , val=str(creator_payable_amount))
        
