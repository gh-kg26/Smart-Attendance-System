#The script imports several libraries including pandas, json, csv, pygsheets, logging, and custom Python modules defined in other scripts.
import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging
from scripts.makeCreatorSheets import makeCreatorSheet
from scripts.makeDelayedOrderSheet import find_delayed_days

from scripts.makeNewApparelSheet import makeNewApparelSheet
from scripts.makeFrajaamConfirmedSheet import *
from scripts.ProductionPipelinePush import Pipeline
from scripts.makeConfirmedSheetCOD import makeConfirmedOrdersSheetCOD
from scripts.ProductionPipelinePushFrajaam import *
from scripts.make_dynamic_creator_sheet import makeCreatorSheetDynamic

#The script sets up logging with a basic configuration that includes the time and message level

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

#The script attempts to open a file called "service_account.json" which is expected to contain authentication information for accessing a Google Sheets account using a service account.

try:

    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)
    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')
    merchit_client_data = client.open('Merchit Client Data')
    client_master_sheets = merchit_client_data.worksheet_by_title('Master Sheets')
    client_master_sheets_df = client_master_sheets.get_as_df()

    client_data_info = merchit_client_data.worksheet_by_title('Master')
    client_data_info_df = client_data_info.get_as_df()

    Shopify_Sheet = client.open('2021-03-18 07:18 merchit-official-merch.myshopify.com - Order')
    wks_Confirmed = Shopify_Sheet.worksheet_by_title('Confirmed')
    # wksDSD = Shopify_Sheet.worksheet_by_title('DSD')

    DSDSheet = client.open('Design Sizing Data')
    wksDSD = DSDSheet.worksheet_by_title('Final Consolidated')

    DelayedOrderShet = client.open('Delayed Order Sheet')
    wksOrderDelays = DelayedOrderShet.worksheet_by_title('Order Delays')

    for idx in client_master_sheets_df.index:
        try:
            ShopifySheet = client.open(client_master_sheets_df['Order Spread Sheet'][idx])
            MasterOrdersPipe = client.open(client_master_sheets_df['Master Spead Sheet'][idx])

            wksOrders = ShopifySheet.worksheet_by_title(client_master_sheets_df['Orders Sheet'][idx])
            wksOrderItems = ShopifySheet.worksheet_by_title(client_master_sheets_df['Order Items Sheet'][idx])
            # wksDSD = ShopifySheet.worksheet_by_title(client_master_sheets_df['DSD'][idx])
            wksConfirmed = ShopifySheet.worksheet_by_title(client_master_sheets_df['Confirmed Sheet'][idx])

            wksErrorSKUs = ShopifySheet.worksheet_by_title(client_master_sheets_df['Error Sheet'][idx])
            wksMasterShopifySheet = ShopifySheet.worksheet_by_title(client_master_sheets_df['Local Master Sheet'][idx])

            wksMasterOrders = MasterOrdersPipe.worksheet_by_title(client_master_sheets_df['Master Prepaid Sheet'][idx])
            wksMasterOrdersCOD = MasterOrdersPipe.worksheet_by_title(client_master_sheets_df['Master COD Sheet'][idx])


            logging.info('Passing Control from Main to makeConfirmedSheet')

            makeConfirmedOrdersSheetCOD(wksOrders , wksOrderItems , wksConfirmed)
            # Pipeline(wksConfirmed , wksMasterShopifySheet, wksMasterOrders , wksMasterOrdersCOD ,wksDSD , wksErrorSKUs)

            find_delayed_days(wksMasterShopifySheet , wksOrderDelays)

        except Exception as exception:
            print("Error while processing" , client_master_sheets_df['Creator'][idx])
            print(exception)
            continue
    
    # for idx in client_data_info_df.index:
    #     Shopify_Sheet = client.open(client_data_info_df['Master Sheet'][idx])
    #     wks_Confirmed = Shopify_Sheet.worksheet_by_title('Confirmed')
    
    makeCreatorSheetDynamic()

except Exception as exception:
    print("Error in app.py")
    print(exception)