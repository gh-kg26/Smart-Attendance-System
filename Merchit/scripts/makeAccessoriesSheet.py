import pygsheets
import copy
import pygsheets
from google.oauth2 import service_account
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

#FIXME The URL Script returns URLs in hyperlinks, need to replace that with the URL text for the python script to work

def makeWksAutoAccessories(ConfirmedOrdersDF1 , wksDSD , SKUaccessories1 , LineItemIDaccesories):

    #Celeb-ViditGujrathi-Mug-12
    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)

    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')
    Automation_Color_Sheet = client.open('Automation Color Sheet')
    Product_Listing_Price = Automation_Color_Sheet.worksheet_by_title('Product Listing Price')
    Product_Listing_Price_df = Product_Listing_Price.get_as_df()

    ConfirmedOrdersDF = ConfirmedOrdersDF1[ConfirmedOrdersDF1['LineItem_ID'].isin(LineItemIDaccesories)]

    LID = ConfirmedOrdersDF['LineItem_ID'].tolist()
    ono = ConfirmedOrdersDF['OrderName'].tolist()
    pname = ConfirmedOrdersDF['Product Title'].tolist()
    qty = ConfirmedOrdersDF['Qty'].tolist()
    date = ConfirmedOrdersDF['Order Date'].tolist()
    SKUaccessories = ConfirmedOrdersDF['SKU'].tolist()

    df_sizing = wksDSD.get_as_df()
    designurl = df_sizing['Design URL'].tolist()
    dcode = df_sizing['Design Code'].tolist()
    branding = df_sizing['Branding'].tolist()
    mockupurl = df_sizing['Front Mockup URL'].tolist()
    placement = df_sizing['Placement'].tolist()

    backmockup = df_sizing['Back Mockup'].tolist()
    backurl = df_sizing['Back URL'].tolist()
    backdimensions = df_sizing['Back Dimensions'].tolist()


    indexlist = []

    for i in range(0 , len(SKUaccessories)):
        for j in range(0 , len(dcode)):
            if SKUaccessories[i] == dcode[j]:
                indexlist.append(j)

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

    size1=[]
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        size1.append('-')

    color1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        color1.append('-')

    status = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        status.append('-')    

    dimensions = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        dimensions.append('-')    


    pipe = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        pipe.append('B2C')

    placement1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        placement1.append(placement[x]) 

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


    style = []
    SKUFlags = []
    try:
        for i in range(0 , len(SKUaccessories)):
            if "PopGrip".lower() in SKUaccessories[i].lower():
                style.append("PopGrip")
            elif "BlackMug".lower() in SKUaccessories[i].lower():
                style.append("BlackMug")  
            elif "Mug".lower() in SKUaccessories[i].lower():
                style.append("Mug")
            elif "Coaster".lower() in SKUaccessories[i].lower():
                style.append("Coaster")
            elif "BlackToteBag".lower() in SKUaccessories[i].lower():
                style.append("BlackToteBag")
            elif "ToteBag".lower() in SKUaccessories[i].lower():
                style.append("ToteBag")

    except:
        SKUFlags.append(SKUaccessories[i])

    hsn_entry = []
    gst_entry = []
    for i in range(0 , len(style)):
        for idx in Product_Listing_Price_df.index:
            if Product_Listing_Price_df['SKU Entry'][idx] == style[i]:
                hsn_entry.append(str(Product_Listing_Price_df['HSN'][idx]))
                gst_entry.append(Product_Listing_Price_df['GST'][idx])
                break


    # logging.info(SKUFlags)


    # finalo = list(zip(date , ono , pname, branding1,  style, size1 , color1, qty, placement1, SKUaccessories , mockupurl1,designurl1))
    finalo = list(zip(LID, date , ono , status, pipe, pname, branding1, style, size1, color1,qty, placement1, SKUaccessories , mockupurl1,designurl1 , dimensions, backmockup1 , backurl1, backdimensions1 , hsn_entry , gst_entry))

    #finalo = list(zip(date, ono , status, pipe, pname, branding1, style ,size, color,qty, placement1,designcode , mockupurl, designurl1  , dimensions1))

    #finalo = list(zip(indexlist, date))
    final = [list(ele) for ele in finalo]

    logging.info('Returned Accessories Sheet') 

    return final

    # lastRow = lastRow + 1
    # wksAutoWksAccessories.insert_rows(lastRow, values=final)


    # lastRow1 = lastRow1 + 1
    # wksAllOrders_OrderFileDL.insert_rows(lastRow1 , values=final)



