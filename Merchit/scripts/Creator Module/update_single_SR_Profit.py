from scripts.GetSRStatus import runner_function

def update_tracking_status(wksCreatorOrders , wks_client_baseprice):
    CreatorOrdersDF = wksCreatorOrders.get_as_df()
    BasePriceDF = wks_client_baseprice.get_as_df()

    print(BasePriceDF)

    # CreatorOrdersDF = CreatorOrdersDF[~CreatorOrdersDF['Current Tracking Status'].str.contains('DELIVERED')]
    # print(CreatorOrdersDF)
    # Channel_Order_ID = CreatorOrdersDF['OrderName'].tolist()
    #Shipping_Status = runner_function(Channel_Order_ID)

    #wksCreatorOrders.update_col(13 , Shipping_Status , 1)

    print(type(CreatorOrdersDF))

    # for row in CreatorOrdersDF.iterrows():
    #     print(row[4])

    tracking_status_complete = ['DELIVERED' , 'RTO DELIVERED' , 'CANCELLED' , 'CANCELED']

    for idx in CreatorOrdersDF.index:
        if CreatorOrdersDF['Status'][idx] not in tracking_status_complete and CreatorOrdersDF['Paid'][idx] == 'FALSE':
            cell_to_update = 'O' + str(idx+2)
            cell_to_update_product_type = 'M' + str(idx+2)
            print("Updating Tracking Status in ", cell_to_update)
            shipping_status_val = runner_function(CreatorOrdersDF['OrderName'][idx])
            for ix in BasePriceDF.index:
                if CreatorOrdersDF['Product Type'][idx].upper() == BasePriceDF['Product Type'][ix].upper():
                    val_display_product_type = BasePriceDF['Display Product Type'][ix]
                    wksCreatorOrders.update_value(addr=cell_to_update_product_type , val=val_display_product_type)

            
            wksCreatorOrders.update_value(addr=cell_to_update , val=shipping_status_val)

    #Update CreatorOrdersDF after shipping status is updated
    CreatorOrdersDF = wksCreatorOrders.get_as_df()

    for idx in CreatorOrdersDF.index:
        if CreatorOrdersDF['Status'][idx] == 'DELIVERED' and CreatorOrdersDF['Paid'][idx] == 'FALSE':
            #14
            cell_to_update = 'P' + str(idx+2)
            cell_to_upadte_product_type = 'M' + str(idx+2)

            val = ''

            for ix in BasePriceDF.index:
                if CreatorOrdersDF['Product Type'][idx].upper() == BasePriceDF['Product Type'][ix].upper() or CreatorOrdersDF['Product Type'][idx].upper() == BasePriceDF['Display Product Type'][ix].upper():
                    val_display_product_type = BasePriceDF['Display Product Type'][ix]
                    wksCreatorOrders.update_value(addr=cell_to_upadte_product_type , val=val_display_product_type)
                    Qty =  int(CreatorOrdersDF['Qty'][idx])

                    if CreatorOrdersDF['Payment Mode'][idx] == 'Cash on Delivery (COD)':
                        SP = float(CreatorOrdersDF['Sale Price'][idx])
                        CP = float(BasePriceDF['Cost Price'][ix])
                        # transaction_fee = 0.02 * SP
                        gst = float(BasePriceDF['GST'][ix])
                        print("GST " , gst)
                        reverse_gst_multiplier = gst/(gst+100)
                        print("Reverse GST Multiplier " , reverse_gst_multiplier)
                        reverse_gst = SP*reverse_gst_multiplier
                        print("Reverse GST " , reverse_gst)
                        print("Selling Price ", SP)
                        print("Cost Price ", CP)
                        print("Reverse GST " , reverse_gst)
                        print("Quantity " , Qty)
                        
                        val = ((SP-CP)*0.8 - reverse_gst)*Qty - 39
                        print("Value COD ", val)

                    else:
                        SP = float(CreatorOrdersDF['Sale Price'][idx])
                        CP = float(BasePriceDF['Cost Price'][ix])


                        transaction_fee = 0.02 * SP
                        gst = float(BasePriceDF['GST'][ix])
                        print("GST " , gst)
                        reverse_gst_multiplier = gst/(gst+100)
                        print("Reverse GST Multiplier " , reverse_gst_multiplier)
                        reverse_gst = SP*reverse_gst_multiplier
                        print("Reverse GST " , reverse_gst)
                        print("Selling Price ", SP)
                        print("Cost Price ", CP)
                        print("Reverse GST " , reverse_gst)
                        print("Quantity " , Qty)
                        
                        val = ((SP-CP)*0.8 - reverse_gst)*Qty - transaction_fee
                        print("Value Prepaid ", val)

            print("ADDING IN " , cell_to_update)
            # print(cell_to_update)
            # Update Product Type            
            # if val == '':
            #     val = 0
            #value_rounded = round(float(val) , 2)
            print(val)
            if val != '':
                value_rounded = "{:.2f}".format(float(val))
            else:
                value_rounded = val
            wksCreatorOrders.update_value(addr=cell_to_update , val=value_rounded)
