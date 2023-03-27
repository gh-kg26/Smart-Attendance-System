#Importing the libraries

import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging

from scripts.makeNewApparelSheet import makeNewApparelSheet
from scripts.makeFrajaamConfirmedSheet import *
from scripts.ProductionPipelinePush import Pipeline
from scripts.makeConfirmedSheetCOD import makeConfirmedOrdersSheetCOD
from scripts.ProductionPipelinePushFrajaam import *

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

with open('service_account.json') as source:
    info = json.load(source )
credentials = service_account.Credentials.from_service_account_info(info)

# client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
client = pygsheets.authorize(service_account_file='service_account.json')

ShopifySheet = client.open('2021-03-18 07:18 merchit-official-merch.myshopify.com - Order')
MasterOrdersPipe = client.open('VM Test')
# MasterOrdersPipe = client.open('MERCHIT ORDER MASTER WORKING')

FrajaamSheet = client.open('2022-04-13 05:28 frajaam.myshopify.com - Order')

#NOTE Worksheets
# wksOrders = ShopifySheet.worksheet_by_title('Orders')
# wksOrderItems = ShopifySheet.worksheet_by_title('OrderItems')
wksDSD = ShopifySheet.worksheet_by_title('DSD') 
# wksConfirmed = ShopifySheet.worksheet_by_title('Confirmed') 
wksConfirmed = MasterOrdersPipe.worksheet_by_title('Input Sheet') 
#NOTE wksMasterShopifySheet is to be changed by uncommenting line 35
# wksMasterShopifySheet = ShopifySheet.worksheet_by_title('Master Sheet')
#NOTE wksMasterShopifySheet is to be changed by uncommenting line 37
wksMasterShopifySheet = MasterOrdersPipe.worksheet_by_title('Master Sheet')
wksMasterShopifySheetCh = ShopifySheet.worksheet_by_title('Master Sheet Ch')

# wksErrorSKUs = ShopifySheet.worksheet_by_title('Error SKUs')
wksErrorSKUs = MasterOrdersPipe.worksheet_by_title('Error SKUs')

wksFrajaamOrders = FrajaamSheet.worksheet_by_title('Orders')
wksFrajaamOrderItems = FrajaamSheet.worksheet_by_title('OrderItems')
wksFrajaamConfirmed = FrajaamSheet.worksheet_by_title('Confirmed')
wksFrajaamMasterSheet = FrajaamSheet.worksheet_by_title('Master Sheet')
wksFrajaamDSD = FrajaamSheet.worksheet_by_title('DSD')

#NOTE Production Pipeline Sheets
wksMasterOrders = MasterOrdersPipe.worksheet_by_title('ORDERS MASTER')
wksMasterOrdersCOD = MasterOrdersPipe.worksheet_by_title('COD Orders')
wksFrajaamMasterOrders = MasterOrdersPipe.worksheet_by_title('Frajaam - ORDERS MASTER')
wksFrajaamMasterCODOrders = MasterOrdersPipe.worksheet_by_title('Frajaam - COD Orders')


logging.info('Passing Control from Main to makeConfirmedSheet')

# makeConfirmedOrdersSheetCOD(wksOrders , wksOrderItems , wksConfirmed)
# makeFrajaamConfirmedSheet(wksFrajaamOrders, wksFrajaamOrderItems , wksFrajaamConfirmed)
Pipeline(wksConfirmed , wksMasterShopifySheet, wksMasterOrders , wksMasterOrdersCOD ,wksDSD , wksErrorSKUs)
# PipelineFrajaam(wksFrajaamConfirmed , wksFrajaamMasterSheet, wksFrajaamMasterOrders , wksFrajaamMasterCODOrders ,wksFrajaamDSD)
# makeNewApparelSheet(wksMasterOrders , wksMasterShopifySheetCh)
# print(a)
    