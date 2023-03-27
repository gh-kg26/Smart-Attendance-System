import pygsheets
import copy
import numpy as np
import logging

import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def makeDumpSheetCropHoodFix(wksConfirmed):

    ConfirmedOrdersDF1 = wksConfirmed.get_as_df()

    # print(LineItemID_nidhi_dump)

    # ConfirmedOrdersDF = ConfirmedOrdersDF1[ConfirmedOrdersDF1['LineItem_ID'].isin(LineItemID_nidhi_dump)]

    # print(ConfirmedOrdersDF)



    ConfirmedOrdersDF2 = ConfirmedOrdersDF1[ConfirmedOrdersDF1['Product Title'].str.contains('Cropped Hoodie')]
    ConfirmedOrdersDF = ConfirmedOrdersDF2[ConfirmedOrdersDF2['SKU'].str.contains('CropTop')]
    
    order_name = ConfirmedOrdersDF['OrderName'].tolist()
    product_title = ConfirmedOrdersDF['Product Title'].tolist()
    sku =  ConfirmedOrdersDF['SKU'].tolist()
    Qty = ConfirmedOrdersDF['Qty'].tolist()
    Customer_Name = ConfirmedOrdersDF['Customer Name'].tolist()
    phone_number = ConfirmedOrdersDF['Phone Number'].tolist()
    date = ConfirmedOrdersDF['Order Date'].tolist()
    payment = ConfirmedOrdersDF['Payment Method'].tolist()


    finalo = list(zip( order_name, product_title, sku, Qty, Customer_Name, phone_number, date, payment))
    final = [list(ele) for ele in finalo]

    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)
    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')

    MasterOrdersPipe = client.open('MERCHIT ORDER MASTER WORKING')
    wks_dump_sheet = MasterOrdersPipe.worksheet_by_title('DUMP SHEET')

    wks_dump_sheet_df = wks_dump_sheet.get_as_df()

    lastRow1 = wks_dump_sheet_df.shape[0] + 2
    wks_dump_sheet.insert_rows(lastRow1, values = final)

