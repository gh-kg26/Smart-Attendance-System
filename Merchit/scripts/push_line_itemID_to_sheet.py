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

def makeDumpSheet(ConfirmedOrdersDF1 , wksMasterShopifySheet , wksDSD , LineItemID_nidhi_dump):

    print(LineItemID_nidhi_dump)

    ConfirmedOrdersDF = ConfirmedOrdersDF1[ConfirmedOrdersDF1['LineItem_ID'].isin(LineItemID_nidhi_dump)]

    print(ConfirmedOrdersDF)

    order_name = ConfirmedOrdersDF['OrderName'].tolist()
    product_title = ConfirmedOrdersDF['Product Title'].tolist()
    sku =  ConfirmedOrdersDF['SKU'].tolist()
    Qty = ConfirmedOrdersDF['Qty'].tolist()
    Customer_Name = ConfirmedOrdersDF['Customer Name'].tolist()
    phone_number = ConfirmedOrdersDF['Phone Number'].tolist()
    date = ConfirmedOrdersDF['Order Date'].tolist()


    # finalo = list(zip(order_name, product_title, sku, Qty ,Customer_Name, phone_number))
    # final = [list(ele) for ele in finalo]

    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)
    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')

    MasterOrdersPipe = client.open('MERCHIT ORDER MASTER WORKING')
    wks_dump_sheet = MasterOrdersPipe.worksheet_by_title('DUMP SHEET')

    DSD_Master = client.open('Design Sizing Data')
    wks_combination_dsd = DSD_Master.worksheet_by_title('Combination Designs')
    combination_design_df = wks_combination_dsd.get_as_df()

    ono = []
    title = []
    skus = []
    qty = []
    name = []
    phone = []
    placement_x = []
    url_x = []
    branding_x = []
    p = []
    date_x = []
    dimension_x = []
    print("PRINTING")
    print(sku)
    print(len(sku))
    for i in range(len(sku)):
        print("SKUS : " , sku[i])
        if 'FanBox' in sku[i] or 'Combo' in sku[i]:
            SKUs_List1 = sku[i].split('-')
            designcode_list1 = []
            designcode_list1 = SKUs_List1[0:3]
            designcode = []
            designcode.append(designcode_list1)
            for k in range(0 , len(designcode)):
                designcode[k] = '-'.join(designcode[k])
            print(designcode[0])
            combination_design_df_current = combination_design_df[combination_design_df['Design Code'].str.contains(designcode[0])]
            Products = combination_design_df_current['Product'].tolist()
            Placement = combination_design_df_current['Front Placement'].tolist()
            DesignURL = combination_design_df_current['Front Design URL'].tolist()
            Dimension = combination_design_df_current['Front Width x Height'].tolist()
            Branding = combination_design_df_current['Branding'].tolist()
            print("LL : " , Products)
            #for individual_product in Products:
            for j in range(0 , len(Products)):
                print("HELLOO" , i)
                ono.append(order_name[i])
                print(ono)
                title.append(product_title[i])
                skus.append(sku[i])
                qty.append(Qty[i])
                name.append(Customer_Name[i])
                phone.append(phone_number[i])
                # p.append(individual_product)                
                p.append(Products[j])
                # date_x(date[i])
                dimension_x.append(Dimension[j])
                placement_x.append(Placement[j])
                url_x.append(DesignURL[j])
                branding_x.append(Branding[j])

        else:
            ono.append(order_name[i])
            title.append(product_title[i])
            skus.append(sku[i])
            qty.append(Qty[i])
            name.append(Customer_Name[i])
            phone.append(phone_number[i])
            p.append("SPLIT SKU")
            # date_x(date[i])
            dimension_x.append("SPLIT SKU")
            placement_x.append("SPLIT SKU")
            url_x.append("SPLIT SKU")
            branding_x.append("SPLIT SKU")


    finalo = list(zip( ono, title, branding_x, p, skus, qty, placement_x, url_x, dimension_x, name, phone))
    final = [list(ele) for ele in finalo]

    wks_dump_sheet_df = wks_dump_sheet.get_as_df()

    lastRow1 = wks_dump_sheet_df.shape[0] + 2
    wks_dump_sheet.insert_rows(lastRow1, values = final)

