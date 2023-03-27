from operator import truediv
import pygsheets
import copy
from scripts.GetSRStatus import runner_function

# from setOrderStatus import setOrderStatus

# def is_apparel(SKU):
#     apparels = ['HALF' , 'FULL']

#     for apparel in apparels:
#         if SKU.upper.contains(apparel):
#             return True
    


def update_tracking_status(wksCreatorOrders):
    CreatorOrdersDF = wksCreatorOrders.get_as_df()
    # CreatorOrdersDF = CreatorOrdersDF[~CreatorOrdersDF['Current Tracking Status'].str.contains('DELIVERED')]
    # print(CreatorOrdersDF)
    Channel_Order_ID = CreatorOrdersDF['OrderName'].tolist()
    Shipping_Status = runner_function(Channel_Order_ID)

    wksCreatorOrders.update_col(13 , Shipping_Status , 1)


#def generateCreatorSheetList(wksConfirmed , checktag , wksCreatorOrders , wksCreatorQuotation):
def generateCreatorSheetList(wksConfirmed , checktag , wksCreatorOrders):
    # print("Hello")

    ConfirmedOrdersDF = wksConfirmed.get_as_df()
    SKUs = ConfirmedOrdersDF['SKU'].tolist()
    
    #OrderID = ConfirmedOrdersDF['OrderName'].tolist()
    LineItemID = ConfirmedOrdersDF['LineItem_ID'].tolist()

    CreatorOrdersDF = wksCreatorOrders.get_as_df()
    
    #CurrentCreatorOrderID = CreatorOrdersDF['OrderName']
    CurrentCreatorLineItemID = CreatorOrdersDF['LineItem_ID']
    
    CreatorSKUs = []
    #CreatorOrderID = []
    CreatorLineItemID = []

    for i in range(0 , len(SKUs)):
        if checktag.lower() in SKUs[i].lower():
            CreatorSKUs.append(SKUs[i])
            #CreatorOrderID.append(OrderID[i])
            CreatorLineItemID.append(LineItemID[i])

    
    # NewCreatorOrderID = [x for x in CreatorOrderID if x not in CurrentCreatorOrderID]
    #NewCreatorOrderID = copy.deepcopy(CreatorOrderID)
    NewCreatorLineItemID = copy.deepcopy(CreatorLineItemID)
    '''
    for element in CurrentCreatorOrderID:
            if element in NewCreatorOrderID:
                NewCreatorOrderID.remove(element)
    '''
    for element in CurrentCreatorLineItemID:
            if element in NewCreatorLineItemID:
                NewCreatorLineItemID.remove(element)    


    #CreatorSheetDF = ConfirmedOrdersDF[ConfirmedOrdersDF['OrderName'].isin(NewCreatorOrderID)]
    CreatorSheetDF = ConfirmedOrdersDF[ConfirmedOrdersDF['LineItem_ID'].isin(NewCreatorLineItemID)]

    SKUs = CreatorSheetDF['SKU'].tolist()
    Qty = CreatorSheetDF['Qty'].tolist()
    ONo = CreatorSheetDF['OrderName'].tolist()
    LineItemID = CreatorSheetDF['LineItem_ID'].tolist()
    ProductTitle = CreatorSheetDF['Product Title'].tolist()
    SalePrice = CreatorSheetDF['Sale Price'].tolist()
    CustomerName = CreatorSheetDF['Customer Name'].tolist()
    OrderDate = CreatorSheetDF['Order Date'].tolist()
    PaymentMode = CreatorSheetDF['Payment Method'].tolist()
    DiscountAmount = CreatorSheetDF['Discount Amount'].tolist()
    DiscountCode = CreatorSheetDF['Discount Code'].tolist()

    ProductType = []

    # sku = []
    # for i in range(0 , len(SKUs)):
    #     txt = SKUs[i].split('-')
    #     sku.append(txt)

    # for i in range(0, len(sku)):
    #     size1 = sku[i].pop()
    #     style1 = sku[i].pop()
        
    #     if 'PhoneCover' in sku[i]:
    #         ProductType.append('PhoneCover')
    #     else:
    #         ProductType.append(style1)
  

#123123

    accessories = ['PopGrip' , 'ButtonBadge' , 'Coaster' , 'Mug']
    apparels = ['HALF' , 'FULL' , 'HOODIE' , 'TANK' , 'Sweatshirt' , 'CropHoo' , 'WomenHalf' , 'CropTop', 'Jogger' , 'SportsBra' , 'FanBox01' , 'FanBox02' , 'FanBox03' , 'FanBox04' , 'Combo01' , 'Combo02' , 'Combo03' , 'Combo04' , 'OversizedTshirt'] 

    for i in range(0 , len(SKUs)):
        for j in range(0 , len(accessories)):
            if accessories[j].lower() in SKUs[i].lower():
                ProductType.append(accessories[j])
        for j in range(0 , len(apparels)):
            if apparels[j].lower() in SKUs[i].lower():
                if 'white' in SKUs[i].lower():
                    str_temp = "white-"+apparels[j]
                    ProductType.append(str_temp)
                else:
                    ProductType.append(apparels[j])
        
        if 'PhoneCover'.lower() in SKUs[i].lower():
            ProductType.append('PhoneCover')


# @12312  



    # for i in range(0 , len(SKUs)):
        

    # for i in range(0 , len(SKUs)):
    #     for type in type_list:   
    #         if type in apparels:
    #             if 'WHITE'.upper() in SKUs[i].upper():
    #                 temp = apparels + "-" + 'WHITE'
    #                 producttype.append(temp)
    #             else:
    #                 producttype.append(apparels)




    CreatorProfit = []
    TrackingLink = []

    # QuotationSheetDF = wksCreatorQuotation.get_as_df()

    # # QuoteSheetDF = QuotationSheetDF[['Product Name' , 'Prepaid Creator Profit' , 'COD Creator Profit']]
    # QuoteSheetList = QuotationSheetDF.values.tolist()

    # productname = ''
    # precod = ''


    # for i in range(0 , len(SKUs)):
    #     if 'HALF'.lower() in SKUs[i].lower() and 'WHITE'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'DTG Tshirt White'
    #         precod = 'COD Creator Profit'
    #     elif 'HALF'.lower() in SKUs[i].lower() and 'WHITE'.lower() in SKUs[i].lower():
    #         productname = 'DTG Tshirt White'
    #         precod = 'Prepaid Creator Profit'
    #     elif 'HALF'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'DTG Tshirt Multi Colour'
    #         precod = 'COD Creator Profit'
    #     elif 'HALF'.lower() in SKUs[i].lower():
    #         productname = 'DTG Tshirt Multi Colour'
    #         precod = 'Prepaid Creator Profit'
    #     elif 'HOODIE'.lower() in SKUs[i].lower() and 'WHITE'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'DTG Hoodie White'
    #         # productname = 'DTG Hoodie Colour'
    #         precod = 'COD Creator Profit'
    #     elif 'HOODIE'.lower() in SKUs[i].lower() and 'WHITE'.lower() in SKUs[i].lower():
    #         productname = 'DTG Hoodie White'
    #         # productname = 'DTG Hoodie Colour'
    #         precod = 'Prepaid Creator Profit'
    #     elif 'HOODIE'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'DTG Hoodie Colour'
    #         precod = 'COD Creator Profit'
    #     elif 'HOODIE'.lower() in SKUs[i].lower():
    #         productname = 'DTG Hoodie Colour'
    #         precod = 'Prepaid Creator Profit'     
    #     elif 'SWEATSHIRT'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'DTG Sweatshirt'
    #         precod = 'COD Creator Profit'       
    #     elif 'SWEATSHIRT'.lower() in SKUs[i].lower():
    #         productname = 'DTG Sweatshirt'
    #         precod = 'Prepaid Creator Profit' 
    #     elif 'BUTTONBADGE'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'Button Badge'
    #         precod = 'COD Creator Profit'       
    #     elif 'BUTTONBADGE'.lower() in SKUs[i].lower():
    #         productname = 'Button Badge'
    #         precod = 'Prepaid Creator Profit' 
    #     elif 'POPGRIP'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'Pop Grip'
    #         precod = 'COD Creator Profit'   
    #     elif 'POPGRIP'.lower() in SKUs[i].lower():
    #         productname = 'Pop Grip'
    #         precod = 'Prepaid Creator Profit'
    #     elif 'Coaster'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'Coaster'
    #         precod = 'COD Creator Profit'   
    #     elif 'Coaster'.lower() in SKUs[i].lower():
    #         productname = 'Coaster'
    #         precod = 'Prepaid Creator Profit'
    #     elif 'Mug'.lower() in SKUs[i].lower() and 'Cash On Delivery'.lower() in PaymentMode[i].lower():
    #         productname = 'Mug'
    #         precod = 'COD Creator Profit'   
    #     elif 'Mug'.lower() in SKUs[i].lower():
    #         productname = 'Mug'
    #         precod = 'Prepaid Creator Profit'
    #     #elif ''

        # for j in range(0 , len(QuoteSheetList)):
        #     if productname == QuoteSheetList[j][0] and precod == 'Prepaid Creator Profit':
        #         profitmargin1 = (SalePrice[i]- QuoteSheetList[j][3])*0.8
        #         profitmargin2 = profitmargin1 -QuoteSheetList[j][5] - QuoteSheetList[j][6] 
        #         CreatorProfit.append(profitmargin2 *  Qty[i])
        #         #CreatorProfit.append(QuoteSheetList[j][1] * Qty[i])
        #     elif productname == QuoteSheetList[j][0] and precod == 'COD Creator Profit':
        #         profitmargin1 = (SalePrice[i]- QuoteSheetList[j][3])*0.8
        #         profitmargin2 = profitmargin1 - 39 - QuoteSheetList[j][6] 
        #         CreatorProfit.append(profitmargin2 *  Qty[i])
        #         #CreatorProfit.append(QuoteSheetList[j][2] * Qty[i])


    paid = []

    track = 'https://merchit.shiprocket.co/tracking/order/'
    temp = ''
    temp1= ''
    for i in range(0 , len(ONo)):
        temp1 = ONo[i]
        temp1 = temp1[1:]
        temp = track + temp1
        TrackingLink.append(temp)
        paid.append('FALSE')


    #Create order status list
    # ShippingStatus = setOrderStatus(wksCreatorOrders)
    Shipping_Status = runner_function(ONo)

    #finalo = list(zip(OrderDate,ONo,ProductTitle,SKUs,Qty,SalePrice,CustomerName,PaymentMode, DiscountAmount, DiscountCode,CreatorProfit, TrackingLink))
    finalo = list(zip(LineItemID, OrderDate,ONo,ProductTitle,SKUs,Qty,SalePrice,CustomerName,PaymentMode, DiscountAmount, DiscountCode, TrackingLink , ProductType ,paid))
    final = [list(ele) for ele in finalo]

    lastRow = CreatorOrdersDF.shape[0]
    lastRow = lastRow + 1

    wksCreatorOrders.insert_rows(lastRow, values=final)

    # update_tracking_status(wksCreatorOrders)

    return final
    # return ShippingStsatus


        
    
        
    


# for j in range(0 , len(QuoteSheetList)):
#    if accessories[j].lower() in SKUs[i].lower():






