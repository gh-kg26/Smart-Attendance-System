import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging
from scripts.makeErrorSKUSheet import makeWksErrorSKUs

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def SegregateProducts(wksConfirmed , wksMasterShopifySheet , wksErrorSKUs):

    CurrentShopifyMasterSheetDF = wksMasterShopifySheet.get_as_df()
    # CurrentShopifyMasterSheetOrderNo = CurrentShopifyMasterSheetDF['Order No'].tolist()
    CurrentShopifyMasterSheetLineItemID = CurrentShopifyMasterSheetDF['LineItem_ID'].tolist()

    ConfirmedOrdersDF1 = wksConfirmed.get_as_df()
    ConfirmedOrdersDF = ConfirmedOrdersDF1[~ConfirmedOrdersDF1['LineItem_ID'].isin(CurrentShopifyMasterSheetLineItemID)]

    SKUs = ConfirmedOrdersDF['SKU'].tolist()

    

    #Handling any spaces in SKU
    for i in range(0 , len(SKUs)):
        SKUs[i] = SKUs[i].replace(" ", "")
        

    # OrderID = ConfirmedOrdersDF['OrderName'].tolist()
    LineItemID = ConfirmedOrdersDF['LineItem_ID'].tolist()

    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)
    client = pygsheets.authorize(service_account_file='service_account.json')
    Color_Sheet = client.open('Automation Color Sheet')
    wks_products_listing = Color_Sheet.worksheet_by_title('Product Listing Price')
    products_listing_df = wks_products_listing.get_as_df()

    products_listing_df_accessory = products_listing_df[products_listing_df['Product Type'].str.contains('Accessory')]
    accessories = products_listing_df_accessory['SKU Entry'].tolist()
    products_listing_df_apparel = products_listing_df[products_listing_df['Product Type'].str.contains('Apparel')]
    apparels = products_listing_df_apparel['SKU Entry'].tolist()


    #accessories = ['PopGrip' , 'ButtonBadge' , 'Coaster' , 'Mug' , 'ToteBag' , 'BlackMug' , 'BlackToteBag']
    #apparels = ['HALF' , 'FULL' , 'HOODIE' , 'TANK' , 'Sweatshirt' , 'CropHood' , 'WomenHalf' , 'CropTop'] 

    nidhi_dumpsheet = ['Jogger' , 'SportsBra' ,'FanBox' , 'Combo']

    SKUapparels = []
    #OrderIDapparels = []
    LineItemIDapparels = []

    SKUphonecovers = []
    # OrderIDphonecovers = []
    LineItemIDphonecovers = []

    SKUaccessories = []
    # OrderIDaccessories = []
    LineItemIDaccesories = []

    LineItemID_nidhi_dump = []

    SKUFlags = []
    # OrderIDFlags = []
    LineItemIDflags = []

    for i in range(0 , len(SKUs)):
        try:
            for j in range(0 , len(accessories)):
                if accessories[j].lower() in SKUs[i].lower():
                    # SKUaccessories.append(SKUs[i])
                    LineItemIDaccesories.append(LineItemID[i])
                    
            for j in range(0 , len(apparels)):
                if apparels[j].lower() in SKUs[i].lower():
                    # SKUapparels.append(SKUs[i])
                    LineItemIDapparels.append(LineItemID[i])

            for j in range(0 , len(nidhi_dumpsheet)):
                if nidhi_dumpsheet[j].lower() in SKUs[i].lower():
                    # SKUapparels.append(SKUs[i])
                    LineItemID_nidhi_dump.append(LineItemID[i])
            
            if 'PhoneCover'.lower() in SKUs[i].lower():
                # SKUphonecovers.append(SKUs[i])
                LineItemIDphonecovers.append(LineItemID[i])

            if '' == SKUs[i].lower():
                print("Entered '' Error Block for " , LineItemID[i])
                SKUFlags.append(SKUs[i])
                LineItemIDflags.append(LineItemID[i])

        except Exception as exception:
            print("Entered Look Up Error Block for " , LineItemID[i])
            SKUFlags.append(SKUs[i])
            LineItemIDflags.append(LineItemID[i])

    #ConfirmedOrdersDFApparel = ConfirmedOrdersDF[ConfirmedOrdersDF['OrderName'].isin(OrderIDapparels)]
    CODTags = ['Cash on Delivery (COD)'] 
    ConfirmedOrdersDFCOD = ConfirmedOrdersDF[ConfirmedOrdersDF['Payment Method'].isin(CODTags)]
    ConfirmedOrdersDFPrepaid = ConfirmedOrdersDF[~ConfirmedOrdersDF['Payment Method'].isin(CODTags)]

    # ConfirmedDFCODono = ConfirmedOrdersDFCOD['OrderName'].tolist()
    ConfirmedDFCODLineItemID = ConfirmedOrdersDFCOD['LineItem_ID'].tolist()
    # ConfirmedDFPrepaidono = ConfirmedOrdersDFPrepaid['OrderName'].tolist()
    ConfirmedDFPrepaidLineItemID = ConfirmedOrdersDFPrepaid['LineItem_ID'].tolist()

    makeWksErrorSKUs(ConfirmedOrdersDF , wksErrorSKUs , SKUFlags ,LineItemIDflags)
    # a = makeWksAutoApparel(ConfirmedOrdersDFPrepaid , wksAutoWksApparel , wksErrorSKUs, wksAllOrders_OrderFileDL, wksMasterOrders , wksB2C, wksDSD , SKUApparelPrepaid , ConfirmedDFPrepaidApparelono)
    # b = makeWksAutoApparelCOD(ConfirmedOrdersDFCOD , wksAutoWksApparel , wksErrorSKUs, wksAllOrders_OrderFileDL, wksMasterOrdersCOD , wksB2C, wksDSD , SKUApparelCOD , ConfirmedDFCODApparelono)
    # # c = automateCustomOrders(wksConfirmed , OrderIDCustom)

    
    # logging.info("PPOno" , ConfirmedDFPrepaidono)
    # logging.info(SKUs) 
    # logging.info(ConfirmedOrdersDF['OrderName'].tolist()) 
    # logging.info(OrderIDaccessories)
    # logging.info(OrderIDapparels)

    logging.info('Products Segregation done') 

    # return SKUaccessories , SKUapparels, OrderIDaccessories , OrderIDapparels, OrderIDphonecovers , ConfirmedDFPrepaidono, ConfirmedDFCODono , ConfirmedOrdersDF
    return SKUaccessories , SKUapparels, LineItemIDaccesories , LineItemIDapparels, LineItemIDphonecovers, LineItemID_nidhi_dump , ConfirmedDFPrepaidLineItemID, ConfirmedDFCODLineItemID , ConfirmedOrdersDF



    
