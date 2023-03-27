#Importing the libraries

import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging
from scripts.makeCreatorSheets import makeCreatorSheet

from scripts.makeNewApparelSheet import makeNewApparelSheet
from scripts.makeFrajaamConfirmedSheet import *
from scripts.ProductionPipelinePush import Pipeline
from scripts.makeConfirmedSheetCOD import makeConfirmedOrdersSheetCOD
from scripts.ProductionPipelinePushFrajaam import *
from scripts.make_dynamic_creator_sheet import makeCreatorSheetDynamic

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

with open('service_account.json') as source:
    info = json.load(source )
credentials = service_account.Credentials.from_service_account_info(info)

client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
# client = pygsheets.authorize(service_account_file='service_account.json')

ShopifySheet = client.open('2021-03-18 07:18 merchit-official-merch.myshopify.com - Order')
MasterOrdersPipe = client.open('VM Test')
# MasterOrdersPipe = client.open('MERCHIT ORDER MASTER WORKING')

FrajaamSheet = client.open('2022-04-13 05:28 frajaam.myshopify.com - Order')

#NOTE Worksheets
wksOrders = ShopifySheet.worksheet_by_title('Orders')
wksOrderItems = ShopifySheet.worksheet_by_title('OrderItems')
wksDSD = ShopifySheet.worksheet_by_title('DSD') 
wksConfirmed = ShopifySheet.worksheet_by_title('Confirmed') 

# wksMasterShopifySheet = ShopifySheet.worksheet_by_title('Master Sheet')
wksMasterShopifySheet = MasterOrdersPipe.worksheet_by_title('Master Sheet')

#NOTE wksMasterShopifySheet is to be changed by uncommenting line 36
# wksMasterShopifySheet = MasterOrdersPipe.worksheet_by_title('Master Sheet')
wksMasterShopifySheetCh = ShopifySheet.worksheet_by_title('Master Sheet Ch')

wksErrorSKUs = ShopifySheet.worksheet_by_title('Error SKUs')

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


#NOTE Creator Sheets
SauravSinhaAccounts = client.open('Saurav Sinha Accounts')
TISAccounts = client.open('TIS Accounts')
PCMBMemesAccounts = client.open('PCMB Memes Accounts')
MridulAccounts = client.open('MriDul Accounts')
VDAccounts = client.open('Vidit X Merchit Accounts')
AshwinAccounts = client.open('Ashwin Bhaskar Accounts')
TirthAccounts = client.open('Tirth Accounts')
MemeMandirAccounts = client.open('MemeMandir - Merchit - Finance')
TMPAccounts = client.open('That Music Project x Merchit')
NaginaAccounts = client.open('Nagina Sethi x Merchit')
ItSuchAccounts = client.open('It Such X Merchit')
DevJoshiAccounts = client.open('Dev Joshi x Merchit')
UnfinanceAccounts = client.open('Unfinance X Merchit')
TapeATaleAccounts = client.open('Tape A Tale - Account Ledger')
ShadabAccounts = client.open('Shadab x Merchit - Account Ledger')
SharmaSistersAccount = client.open('Sharma Sisters x Merchit')
GuluaAccounts = client.open('Mr Gulua Comedy x Merchit')

TDTAccounts = client.open('TDT X Merchit')
TSSAccounts = client.open('TSS x Merchit')
wksOrdersTDT = TDTAccounts.worksheet_by_title('Live Orders')
wksOrdersTSS = TSSAccounts.worksheet_by_title('Live Orders')
wksConfirmedTSS = TSSAccounts.worksheet_by_title('Confirmed Orders')
wksMemeMandirOrders = MemeMandirAccounts.worksheet_by_title('Orders')

wksSauravSinhaOrders = SauravSinhaAccounts.worksheet_by_title('Orders')
wksTISOrders = TISAccounts.worksheet_by_title('Orders')
wksPCMBMemesOrders = PCMBMemesAccounts.worksheet_by_title('Orders')
wksMriDulOrders = MridulAccounts.worksheet_by_title('Orders')
wksViditOrders = VDAccounts.worksheet_by_title('Orders')
wksAshwinOrders = AshwinAccounts.worksheet_by_title('Orders')
wksTirthOrders = TirthAccounts.worksheet_by_title('Orders')
wksTMPOrders = TMPAccounts.worksheet_by_title('Orders')
wksNaginaOrders = NaginaAccounts.worksheet_by_title('Orders')
wksItSuchOrders = ItSuchAccounts.worksheet_by_title('Orders')
wksDevJoshiOrders = DevJoshiAccounts.worksheet_by_title('Orders')
wksUnfinanceOrders = UnfinanceAccounts.worksheet_by_title('Orders')
wksTapeATaleOrders = TapeATaleAccounts.worksheet_by_title('Orders')
wksShadabOrders = ShadabAccounts.worksheet_by_title('Orders')
wksSharmaSistersOrders = SharmaSistersAccount.worksheet_by_title('Orders')
wksGuluaOrders = GuluaAccounts.worksheet_by_title('Orders')


logging.info('Passing Control from Main to makeConfirmedSheet')

makeConfirmedOrdersSheetCOD(wksOrders , wksOrderItems , wksConfirmed)
# makeFrajaamConfirmedSheet(wksFrajaamOrders, wksFrajaamOrderItems , wksFrajaamConfirmed)
Pipeline(wksConfirmed , wksMasterShopifySheet, wksMasterOrders , wksMasterOrdersCOD ,wksDSD , wksErrorSKUs)
# PipelineFrajaam(wksFrajaamConfirmed , wksFrajaamMasterSheet, wksFrajaamMasterOrders , wksFrajaamMasterCODOrders ,wksFrajaamDSD)
# makeNewApparelSheet(wksMasterOrders , wksMasterShopifySheetCh)

makeCreatorSheetDynamic(wksConfirmed)
# 
# print(a)

# makeCreatorSheet(wksConfirmed , wksSauravSinhaOrders , wksTISOrders, wksPCMBMemesOrders , wksMriDulOrders , wksViditOrders , wksAshwinOrders, wksTirthOrders , wksMemeMandirOrders , wksTMPOrders , wksNaginaOrders , wksItSuchOrders , wksDevJoshiOrders , wksUnfinanceOrders , wksTapeATaleOrders , wksShadabOrders , wksSharmaSistersOrders , wksGuluaOrders)