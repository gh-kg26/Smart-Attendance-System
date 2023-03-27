import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def makeConfirmedOrdersSheetCOD(wksOrders , wksOrderItems , wksConfirmed):

    FinancialStatus = ['refunded' , 'voided']

    CurrentConfirmedOrdersDF = wksConfirmed.get_as_df()
    CurrentConfirmedONo = CurrentConfirmedOrdersDF['OrderName'].tolist()

    OrderItemsDF = wksOrderItems.get_as_df()

    #Getting the last row index
    lastRow = CurrentConfirmedOrdersDF.shape[0]
    
    ##WKS to Dataframe
    OrdersDF1 = wksOrders.get_as_df()

    ##To delete all existing entries
    OrdersDF = OrdersDF1[~OrdersDF1['Name'].isin(CurrentConfirmedONo)]

    #Filtering out Orders on the basis of tags or it being prepaid
    OrdersDF3 = OrdersDF[OrdersDF['Tags'].str.contains('Converted from COD') | OrdersDF['Tags'].str.contains('Confirmed-CODfirm') | OrdersDF['Tags'].str.contains('GIVEAWAY') | OrdersDF['Payment Method'].str.contains('paytm') |OrdersDF['Payment Method'].str.contains('sezzle_in') | OrdersDF['Payment Method'].str.contains('razorpay_cards_upi_netbanking_wallets_') | OrdersDF['Payment Method'].str.contains('cashfree_upi_cards_wallets_paypal_netbanking') | OrdersDF['Payment Method'].str.contains('Razorpay Secure') | OrdersDF['Payment Method'].str.contains('Razorpay Secure (UPI, Cards, Wallets, NetBanking)') | OrdersDF['Payment Method'].str.contains('Paytm Payment Gateway') | OrdersDF['Payment Method'].str.contains('stripe')]

    OrdersDF2 = OrdersDF3[~OrdersDF3['Financial Status'].isin(FinancialStatus)]

    #OrdersDF2 contains all the orders from OrderSheet which are confirmed
    OrdersDFWithPaymentMode = OrdersDF2[['Name' , 'Payment Method' , 'Discount Amount' , 'Discount Code' , 'Billing Phone' , 'Financial Status']]
    OrdersDFWithPaymentMode = OrdersDFWithPaymentMode.values.tolist()

    #Getting order no from ordersDF
    ConfirmedOrdNo = OrdersDF2['Name'].tolist()

    #Filtering Data from Order Items on the basis of the orders numbers retrieved from OrdersDF
    OrderItemsDFA = OrderItemsDF[OrderItemsDF['OrderName'].isin(ConfirmedOrdNo)]
    ConfirmedOrderItemsOno = OrderItemsDFA['OrderName'].tolist()

    PaymentMode = []
    DiscountAmount = []
    DiscountCode = []
    PhoneNumber = []
    FinancialStatus = []


    for i in range(0 , len(ConfirmedOrderItemsOno)):
        for j in range(0, len(OrdersDFWithPaymentMode)):
            if ConfirmedOrderItemsOno[i] == OrdersDFWithPaymentMode[j][0]:
                PaymentMode.append(OrdersDFWithPaymentMode[j][1])
                DiscountAmount.append(OrdersDFWithPaymentMode[j][2])
                DiscountCode.append(OrdersDFWithPaymentMode[j][3])
                PhoneNumber.append(OrdersDFWithPaymentMode[j][4])
                FinancialStatus.append(OrdersDFWithPaymentMode[j][5])
    

    ##DF To List
    
    
    ##Appending to the Confirmed Sheet
    rowsToBeAdded = OrderItemsDFA.shape[0]
    rowsToBeAdded = rowsToBeAdded + 1
    lastRow = lastRow+1
    wksConfirmed.add_rows(rowsToBeAdded)


    #Remove Unncessary Columns from ConfirmedOrderItemsDF
    del OrderItemsDFA['Carrier']
    del OrderItemsDFA['Tracking Number']
    del OrderItemsDFA['Unfulfilled']
    del OrderItemsDFA['New qty of fulfilled item/s']
    del OrderItemsDFA['New Tracking Number']
    del OrderItemsDFA['New Carrier']
    del OrderItemsDFA['Last updated']
    del OrderItemsDFA['Currency']
    del OrderItemsDFA['Status']
    del OrderItemsDFA['Fulfillment status']
    


    COIS = OrderItemsDFA.values.tolist()
    
    a1 = OrderItemsDFA['LineItem_ID'].tolist()
    a2 = OrderItemsDFA['OrderID'].tolist()
    a3 = OrderItemsDFA['OrderName'].tolist()
    a4 = OrderItemsDFA['Product Title'].tolist()
    a5 = OrderItemsDFA['SKU'].tolist()
    a6 = OrderItemsDFA['Property'].tolist()
    a7 = OrderItemsDFA['Price'].tolist()
    a8 = OrderItemsDFA['Sale price'].tolist()
    a9 = OrderItemsDFA['Qty'].tolist()
    a10 = OrderItemsDFA['Customer Name'].tolist()
    a11 = OrderItemsDFA['Shipping Name'].tolist()
    a12 = OrderItemsDFA['Order Date'].tolist()
    

    COIS = list(zip(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12, PaymentMode, DiscountAmount , DiscountCode , PhoneNumber , FinancialStatus))
    final = [list(ele) for ele in COIS]


    wksConfirmed.insert_rows(lastRow, values=final)

    logging.info('Pushed into Confirmed Sheet')
    logging.info('Passing Control from makeConfirmedSheetCOD to Main')

    # return COIS
