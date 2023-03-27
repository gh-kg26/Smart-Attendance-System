import copy
import numpy as np
import pygsheets
from google.oauth2 import service_account
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def makeWksAutoPhoneCovers(ConfirmedOrdersDF1 , wksDSD , LineItemIDphonecovers):
    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)

    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')
    Automation_Color_Sheet = client.open('Automation Color Sheet')
    Product_Listing_Price = Automation_Color_Sheet.worksheet_by_title('Product Listing Price')
    Product_Listing_Price_df = Product_Listing_Price.get_as_df()

    ConfirmedOrdersDF = ConfirmedOrdersDF1[ConfirmedOrdersDF1['LineItem_ID'].isin(LineItemIDphonecovers)]

    LID = ConfirmedOrdersDF['LineItem_ID'].tolist()
    ono = ConfirmedOrdersDF['OrderName'].tolist()
    pname = ConfirmedOrdersDF['Product Title'].tolist()
    qty = ConfirmedOrdersDF['Qty'].tolist()
    date = ConfirmedOrdersDF['Order Date'].tolist()
    SKUPhoneCovers = ConfirmedOrdersDF['SKU'].tolist()

    sku = []
    for i in range(0 , len(SKUPhoneCovers)):
        txt = SKUPhoneCovers[i].split('-')
        sku.append(txt)    

    print("SKU:" , sku)


    designcode = []
    style = []
    for SKUItem in sku:
        designcode.append(SKUItem[0:4])
        style1 = SKUItem[4:]
        style1.append(SKUItem[2])
        style.append(style1)

    print("Design Code" , designcode)
    print("Style" , style)


    designcode1 = []
    style1 = []
    # for i in designcode:
    #     # designcode[i] = '-'.join(designcode[i])
    #     # style[i] = '-'.join(style[i])
    #     tmp = '-'.join(i)
    #     designcode1.append(tmp)
    
    # designcode1 = '-'.join(designcode)
    for des in designcode:
        str1 = '-'.join(des)
        designcode1.append(str1) 

    for sty in style:
        str1 = '-'.join(sty)
        style1.append(str1)

    hsn_entry = []
    gst_entry = []

    Product_Listing_HSN_Extract = Product_Listing_Price_df[Product_Listing_Price_df['SKU Entry'].str.contains('PhoneCover')]
    # print(Product_Listing_HSN_Extract , Product_Listing_HSN_Extract['HSN'] , Product_Listing_HSN_Extract['GST'])
    for i in range(0 , len(style)):
        hsn_entry.append(str(Product_Listing_HSN_Extract.iloc[0]['HSN']))
        gst_entry.append( Product_Listing_HSN_Extract.iloc[0]['GST'])


    df_sizing = wksDSD.get_as_df()
    dimensions = df_sizing['Dimensions'].tolist()
    placement = df_sizing['Placement'].tolist()
    designurl = df_sizing['Design URL'].tolist()
    dcode = df_sizing['Design Code'].tolist()
    branding = df_sizing['Branding'].tolist()
    mockupurl = df_sizing['Front Mockup URL'].tolist()
    backmockup = df_sizing['Back Mockup'].tolist()
    backurl = df_sizing['Back URL'].tolist()
    backdimensions = df_sizing['Back Dimensions'].tolist()

    indexlist = []

    #Checks Design Code from DSD
    # statusCheck = 0
    for i in range(0 , len(designcode1)):
        statusCheck = 0
        for j in range(0 , len(dcode)):
            if designcode1[i].lower() == dcode[j].lower():
                indexlist.append(j)
                statusCheck = 1
                # break
        if statusCheck == 0:
            indexlist.append(0)


    dimensions1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        dimensions1.append(dimensions[x])
        
    placement1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        placement1.append(placement[x])
        
    designurl1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        designurl1.append(designurl[x])    

    mockupurl1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        mockupurl1.append(mockupurl[x]) 

    branding1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        branding1.append(branding[x]) 
    
    color = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        color.append('-')

    size = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        size.append('-')   

    status = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        status.append('-')    

    pipe = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        pipe.append('B2C')

    backmockup1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        backmockup1.append(backmockup[x]) 
    backurl1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        backurl1.append(backurl[x]) 
    backdimensions1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        backdimensions1.append(backdimensions[x]) 



    finalo = list(zip(LID, date, ono , status, pipe, pname, branding1, style1 ,size, color,qty, placement1,designcode1 , mockupurl, designurl1  , dimensions1, backmockup1 , backurl1, backdimensions1 , hsn_entry , gst_entry))
    print(finalo)
    final = [list(ele) for ele in finalo]

    return final
