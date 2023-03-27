import pygsheets
import copy
import numpy as np
import logging
import pygsheets
from google.oauth2 import service_account
import json

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def makeWksAutoApparel(ConfirmedOrdersDF1 , wksMasterShopifySheet , wksDSD , SKUapparels1 , LineItemIDapparels):

    with open('service_account.json') as source:
        info = json.load(source )
    credentials = service_account.Credentials.from_service_account_info(info)

    # client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
    client = pygsheets.authorize(service_account_file='service_account.json')
    Automation_Color_Sheet = client.open('Automation Color Sheet')
    Product_Listing_Price = Automation_Color_Sheet.worksheet_by_title('Product Listing Price')
    Product_Listing_Price_df = Product_Listing_Price.get_as_df()

    ConfirmedOrdersDF = ConfirmedOrdersDF1[ConfirmedOrdersDF1['LineItem_ID'].isin(LineItemIDapparels)]

    LID = ConfirmedOrdersDF['LineItem_ID'].tolist()
    ono = ConfirmedOrdersDF['OrderName'].tolist()
    pname = ConfirmedOrdersDF['Product Title'].tolist()
    qty = ConfirmedOrdersDF['Qty'].tolist()
    date = ConfirmedOrdersDF['Order Date'].tolist()
    SKUapparels = ConfirmedOrdersDF['SKU'].tolist()


    # AutoWksApparelDF = wksMasterShopifySheet.get_as_df()
    # lastRow = AutoWksApparelDF.shape[0]

    # wksMasterOrdersDF = wksMasterOrders.get_as_df()
    # lastRow2 = wksMasterOrdersDF.shape[0]
    

    sku = []
    for i in range(0 , len(SKUapparels)):
        txt = SKUapparels[i].split('-')
        sku.append(txt)

    designcode = []
    size = []
    style = []
    color = []
    gender = []

    # OrderIDFlags = []
    LineItemIDFlags  = []
    SKUFlags = []

    

    designcode = copy.deepcopy(sku)

    for i in range(0, len(designcode)):
        try:
            size1 = designcode[i].pop()
            style1 = designcode[i].pop()
            color1 = designcode[i].pop()
            
            size.append(size1)
            style.append(style1)
            color.append(color1)

        except:
            LineItemIDFlags.append(LineItemIDapparels[i])
            SKUFlags.append(SKUapparels[i])

    # CurrentErrorsDF = wksErrorSKUs.get_as_df()
    # CurrentErrorONo = CurrentErrorsDF['OrderName'].tolist()

    # ConfirmedOrdersDF3 = ConfirmedOrdersDF[~ConfirmedOrdersDF['OrderName'].isin(CurrentErrorONo)]

    # ConfirmedOrdersDF2 = ConfirmedOrdersDF3[ConfirmedOrdersDF3['OrderName'].isin(OrderIDFlags)]

    # for i in range(0 , len(style)):
    #     Product_Listing_Price_df_hsn_extract = Product_Listing_Price_df[Product_Listing_Price_df['SKU Entry'] == style[i]]
    hsn_entry = []
    gst_entry = []
    print("STYLE IS : " , style)
    for i in range(0 , len(style)):
        for idx in Product_Listing_Price_df.index:
            if Product_Listing_Price_df['SKU Entry'][idx].lower() == style[i].lower():
                hsn_entry.append(str(Product_Listing_Price_df['HSN'][idx]))
                gst_entry.append(Product_Listing_Price_df['GST'][idx])
                # break

            
    print(hsn_entry , gst_entry)

    for i in range(0 , len(designcode)):
        designcode[i] = '-'.join(designcode[i])
    
    for i in range(0 , len(style)):
        text = 'UNISEX'
        gender.append(text)

    df_sizing = wksDSD.get_as_df()
    # dimensions = df_sizing['Dimensions'].tolist()
    front_width = df_sizing['Front Width'].tolist()
    front_height = df_sizing['Front Height'].tolist()
    placement = df_sizing['Placement'].tolist()
    designurl = df_sizing['Design URL'].tolist()
    dcode = df_sizing['Design Code'].tolist()
    branding = df_sizing['Branding'].tolist()
    mockupurl = df_sizing['Front Mockup URL'].tolist()
    backmockup = df_sizing['Back Mockup'].tolist()
    backurl = df_sizing['Back URL'].tolist()
    back_width = df_sizing['Back Width'].tolist()
    back_height = df_sizing['Back Height'].tolist()
    # backdimensions = df_sizing['Back Dimensions'].tolist()
    messagecardurl = df_sizing['Message Card URL'].tolist()
    messagecard = df_sizing['Message Card'].tolist()

    indexlist = []

    #Checks Design Code from DSD
    # statusCheck = 0
    for i in range(0 , len(designcode)):
        statusCheck = 0
        for j in range(0 , len(dcode)):
            if designcode[i].lower() == dcode[j].lower():
                indexlist.append(j)
                statusCheck = 1
                # break
        if statusCheck == 0:
            indexlist.append(0)

    dynamic_sizing_chart = {"S" : 0.9 , "M":0.95 , "L":1 , "XL":1.05 , "XXL" : 1.1}    

    dimensions1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if front_width[x] == '' or front_height[x] == '':
            dimensions1.append('-')
        else:
            print("Before adjusted : " , front_width[x], "  ", front_height[x] )
            front_width_adjusted = float(dynamic_sizing_chart[size[i]]) * float(front_width[x])
            front_width_adjusted_rounded = "{:.2f}".format(float(front_width_adjusted))
            front_height_adjusted = float(dynamic_sizing_chart[size[i]]) * float(front_height[x])
            front_height_adjusted_rounded = "{:.2f}".format(float(front_height_adjusted))
            print("After adjusted : " , front_width_adjusted_rounded, "  ", front_height_adjusted_rounded )
            dimensions_adjusted = str(front_width_adjusted_rounded) + " x " + str(front_height_adjusted_rounded)
            dimensions1.append(dimensions_adjusted)
    # for i in range(0 , len(indexlist)):
    #     x = indexlist[i]
    #     if dimensions[x] == '':
    #         dimensions1.append('-')
    #     else:
    #         dimensions1.append(dimensions[x])
        
    placement1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if placement[x] == '':
            placement1.append('-')
        else:
            placement1.append(placement[x])
        
    designurl1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if designurl[x] == '':
            designurl1.append('-')
        else:
            designurl1.append(designurl[x])    

    mockupurl1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if mockupurl[x] == '':
            mockupurl1.append('-') 
        else:
            mockupurl1.append(mockupurl[x]) 

    branding1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if branding[x] == '':
            branding1.append('-') 
        else:
            branding1.append(branding[x]) 

    backmockup1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if backmockup[x] == '':
            backmockup1.append('-')
        else:
            backmockup1.append(backmockup[x]) 

    backurl1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if backurl[x] == '':
            backurl1.append('-')
        else:
            backurl1.append(backurl[x])

    backdimensions1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if back_width[x] == '' or back_height[x] == '':
            backdimensions1.append('-')
        else:
            print("Before adjusted : " , back_width[x], "  ", back_height[x] )
            back_width_adjusted = float(dynamic_sizing_chart[size[i]]) * float(back_width[x])
            back_width_adjusted_rounded = "{:.2f}".format(float(back_width_adjusted))
            back_height_adjusted = float(dynamic_sizing_chart[size[i]]) * float(back_height[x])
            back_height_adjusted_rounded = "{:.2f}".format(float(back_height_adjusted))
            print("After adjusted : " , back_width_adjusted_rounded, "  ", back_height_adjusted_rounded )
            back_dimensions_adjusted = str(back_width_adjusted_rounded) + " x " + str(back_height_adjusted_rounded)
            backdimensions1.append(back_dimensions_adjusted)
    # for i in range(0 , len(indexlist)):
    #     x = indexlist[i]
    #     if backdimensions[x] == '':
    #         backdimensions1.append('-')
    #     else:
    #         backdimensions1.append(backdimensions[x]) 

    status = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        status.append('-')   

    pipe = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        pipe.append('B2C')

    messagecardurl1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if messagecardurl[x] == '':
            messagecardurl1.append('-')
        else:
            messagecardurl1.append(messagecardurl[x]) 


    messagecard1 = []
    for i in range(0 , len(indexlist)):
        x = indexlist[i]
        if messagecard[x] == '':
            messagecard1.append('-')
        else:
            messagecard1.append(messagecard[x]) 


    finalo = list(zip(LID, date, ono , status, pipe, pname, branding1, style ,size, color,qty, placement1,designcode , mockupurl, designurl1  , dimensions1 , backmockup1 , backurl1, backdimensions1 , messagecard1 , messagecardurl1 , hsn_entry , gst_entry))
    print(finalo)
    final = [list(ele) for ele in finalo]


    # lastRow = lastRow + 1
    # lastRow2 = lastRow2 + 1
    # wksMasterShopifySheet.insert_rows(lastRow, values=final)
    # wksMasterOrders.insert_rows(lastRow2 , values=final)

    logging.info('Returned Apparel Sheet') 

    return final