import logging
from numpy import product

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def makeNewApparelSheet(wksMasterOrders , wksMasterShopifySheetCh):

    apparels = ['HALF' , 'FULL' , 'HOODIE' , 'TANK' , 'SWEATSHIRT' , 'CROPHOOD']
    prodFilters = ['B2C' , 'B2B']

    wksMasterOrdersDF = wksMasterOrders.get_as_df()
    # wksMasterOrdersDF = wksMasterOrdersDF[1:]
    # print(wksMasterOrdersDF.head())
    # print(wksMasterOrdersDF.columns)

    header = wksMasterOrdersDF.iloc[0]
    wksMasterOrdersDF.columns = header

    # print(wksMasterOrdersDF.head())
    # print(wksMasterOrdersDF.columns)

    wksMasterShopifySheetChDF = wksMasterShopifySheetCh.get_as_df()
    lastRow = wksMasterShopifySheetChDF.shape[0]
    onoexisting = wksMasterShopifySheetChDF['Order_ID'].tolist()

    # OrdersDF2 = OrdersDF3[~OrdersDF3['Financial Status'].isin(FinancialStatus)]
    wksMasterOrdersDF1 = wksMasterOrdersDF[wksMasterOrdersDF['B2C/B2B/SAMPLE'].isin(prodFilters)]
    wksMasterOrdersDF3 = wksMasterOrdersDF1[wksMasterOrdersDF1['Product'].str.upper().isin(apparels)]
    wksMasterOrdersDF2 = wksMasterOrdersDF3[~wksMasterOrdersDF3['Order No'].isin(onoexisting)]


    OrderID = wksMasterOrdersDF2['Order No'].tolist()
    Qty = wksMasterOrdersDF2['Quantity'].tolist()
    FrontMockup = wksMasterOrdersDF2['Front Mockup'].tolist()
    FrontDesign = wksMasterOrdersDF2['Front Design URL (png file)'].tolist()
    Dimensions = wksMasterOrdersDF2['Front Dimensions of the print (WXH)(in Inches)'].tolist()  

    print(Dimensions)

    for i in range(0,len(Dimensions)):
        Dimensions[i] = Dimensions[i].replace('X' , 'x')

    Width1 , Height1 = zip(*(s.split("x") for s in Dimensions))    
    Width = list(Width1)
    Height = list(Height1)
    FrontDesignPos = wksMasterOrdersDF2['Place to print'].tolist()



    product_unchanged = wksMasterOrdersDF2['Product'].tolist()
    color_unchanged = wksMasterOrdersDF2['Colour'].tolist()
    size = wksMasterOrdersDF2['Size'].tolist()
    product_changed = []

    productType = {'HALF' : 'M-UNI',
    'HOODIE' : 'M-HOD',
    'SWEATSHIRT' : 'M-SW',
    'FULL' : 'M-RNFL',
    'CROPTOP' : 'W-CROP',
    'WHALF' : 'W-RN',
    'CROPHOOD' : 'W-CRHOD'}

    colors = {'BLACK' : 'BLA',
    'WHITE' : 'WHI',
    'GREY' : 'MGRE',
    'NAVYBLUE' : 'NB',
    'AQUABLUE' : 'AQB',
    'RED' : 'RED',
    'PINK' : 'BPNK',
    'OLIVEGREEN' : 'OGRN',
    'MAROON' : 'MRN',
    'BLUE' : 'RB'}

    # tmp = productType[product_unchanged[1].upper()]
    # print(tmp)

    for i in range(0 , len(product_unchanged)):
        # for j in range(0 , len(webProd)):
        tmp_prod = productType[product_unchanged[i].upper()]
        tmp_color = colors[color_unchanged[i].upper()]
        tmp_size = size[i]
        tmp = tmp_prod + '-' + tmp_color + '-' + tmp_size
        product_changed.append(tmp)

        # product_changed.append(tmp)


    print(product_unchanged , product_changed)

    finalo = list(zip(OrderID, product_changed , Qty, FrontMockup, FrontDesign, Width, Height  ,FrontDesignPos))
    final = [list(ele) for ele in finalo]

    wksMasterShopifySheetCh.insert_rows(lastRow, values = final)



    # print(type(product_unchanged))







    



