from scripts.GetSRStatus import runner_function

print("INSIDE UPDATE SINGLE SHIPROCKET PROFIT 7")


def return_unpaid_creator_profit(CreatorOrdersDF_Profit):
    CreatorOrdersDF_Profit = [float(i) if i != '' else 0.0 for i in CreatorOrdersDF_Profit]
    creator_payable_amount = sum(CreatorOrdersDF_Profit)
    if creator_payable_amount != '':
        rounded_creator_payable_amount = "{:.2f}".format(float(creator_payable_amount))
    else:
            rounded_creator_payable_amount = creator_payable_amount

    return rounded_creator_payable_amount
    
def update_tracking_status(wksCreatorOrders , wks_client_baseprice , wksDSD , checktag , percentage_split):
    CreatorOrdersDF = wksCreatorOrders.get_as_df()
    BasePriceDF = wks_client_baseprice.get_as_df()
    DSD_DF = wksDSD.get_as_df()

    DSD_DF = DSD_DF[DSD_DF['Design Code'].str.contains(checktag)]

    # print(BasePriceDF)

    # CreatorOrdersDF = CreatorOrdersDF[~CreatorOrdersDF['Current Tracking Status'].str.contains('DELIVERED')]
    # print(CreatorOrdersDF)
    # Channel_Order_ID = CreatorOrdersDF['OrderName'].tolist()
    #Shipping_Status = runner_function(Channel_Order_ID)

    #wksCreatorOrders.update_col(13 , Shipping_Status , 1)

    print(type(CreatorOrdersDF))

    # for row in CreatorOrdersDF.iterrows():
    #     print(row[4])

    tracking_status_complete = ['DELIVERED' , 'RTO DELIVERED' , 'CANCELLED' , 'CANCELED' , 'REFUNDED' , 'COD ORDER NOT CONFIRMED' , 'CANCELLATION REQUESTED']

    for idx in CreatorOrdersDF.index:
        # print("ENTERED HERE")
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
        if CreatorOrdersDF['Status'][idx] == 'DELIVERED' and CreatorOrdersDF['Paid'][idx] == 'FALSE' and CreatorOrdersDF['Pipeline Completion Status'][idx] != 'TRUE':
            #14
            cell_to_update = 'P' + str(idx+2)
            cell_to_upadte_product_type = 'M' + str(idx+2)

            val = ''
            effective_sale_price_column = ''
            cell_espc = 'Q' + str(idx+2)
            gst_column = ''
            cell_gc =  'R' + str(idx+2)
            product_cost_column = ''
            cell_pcc = 'S' + str(idx+2)
            back_print_cost_column = ''
            cell_bpcc = 'T' + str(idx+2)
            cod_charges_column= ''
            cell_ccc = 'U' + str(idx+2) 
            prepaid_transaction_charges_column = ''
            cell_ptcc = 'V' + str(idx+2) 

            pipeline_completion_status_column = 'TRUE'
            cell_pcsc = 'W' + str(idx+2)



            for ix in BasePriceDF.index:
                if CreatorOrdersDF['Product Type'][idx].upper() == BasePriceDF['Product Type'][ix].upper() or CreatorOrdersDF['Product Type'][idx].upper() == BasePriceDF['Display Product Type'][ix].upper():
                    val_display_product_type = BasePriceDF['Display Product Type'][ix]
                    wksCreatorOrders.update_value(addr=cell_to_upadte_product_type , val=val_display_product_type)
                    Qty =  int(CreatorOrdersDF['Qty'][idx])

                    if CreatorOrdersDF['Payment Mode'][idx] == 'Cash on Delivery (COD)':
                        SP = float(CreatorOrdersDF['Sale Price'][idx])

                        #Column Q
                        effective_sale_price_column = SP
                        SKU = CreatorOrdersDF['SKU'][idx]
                        SKU_list_split = SKU.split('-')
                        Design_Code_list = SKU_list_split[0:3]
                        Design_code = '-'.join(Design_Code_list)
                        CP = 0
                        for indx in DSD_DF.index:
                            if DSD_DF['Design Code'][indx] == Design_code and DSD_DF['Back URL'][indx] != '-' and DSD_DF['Placement'][indx].lower() == 'pocket':
                                print(Design_code , DSD_DF['Design Code'][indx])
                                print("Entered if block for Back URL Compensated Condition")
                                CP = float(BasePriceDF['Cost Price'][ix]) + BasePriceDF['Back Print Compensated'][0]
                                #Column T
                                back_print_cost_column = BasePriceDF['Back Print Compensated'][0]
                                break
                            elif DSD_DF['Design Code'][indx] == Design_code and DSD_DF['Back URL'][indx] != '-' and DSD_DF['Placement'][indx].lower() != 'pocket':
                                print(Design_code , DSD_DF['Design Code'][indx])
                                print("Entered if block for Back URL Condition")
                                CP = float(BasePriceDF['Cost Price'][ix]) + BasePriceDF['Back Print'][0]
                                #Column T
                                back_print_cost_column = BasePriceDF['Back Print'][0]
                                break
                            else:
                                print("Entered else block for Back URL")
                                CP = float(BasePriceDF['Cost Price'][ix])
                                #Column T
                                back_print_cost_column = 0

                        # transaction_fee = 0.02 * SP
                        gst = float(BasePriceDF['GST'][ix])
                        print("GST " , gst)
                        reverse_gst_multiplier = gst/(gst+100)
                        print("Reverse GST Multiplier " , reverse_gst_multiplier)
                        reverse_gst = SP*reverse_gst_multiplier

                        #Column R
                        gst_column = reverse_gst
                        #Column S
                        product_cost_column = CP


                        print("Reverse GST " , reverse_gst)
                        print("Selling Price ", SP)
                        print("Cost Price ", CP)
                        print("Reverse GST " , reverse_gst)
                        print("Quantity " , Qty)
                        
                        percentage_split_f = int(percentage_split)/100

                        # val = ((SP-CP)*0.8 - reverse_gst)*Qty - 39
                        val = ((SP-CP)*percentage_split_f - reverse_gst)*Qty - 39

                        #Column U
                        cod_charges_column = 39
                        #Column V
                        prepaid_transaction_charges_column = 0

                        print("Value COD ", val)

                    else:
                        SP = float(CreatorOrdersDF['Sale Price'][idx])
                        #COLUMN Q
                        effective_sale_price_column = SP

                        # CP = float(BasePriceDF['Cost Price'][ix])
                        SKU = CreatorOrdersDF['SKU'][idx]
                        SKU_list_split = SKU.split('-')
                        Design_Code_list = SKU_list_split[0:3]
                        Design_code = '-'.join(Design_Code_list)

                        CP = 0
                        for indx in DSD_DF.index:
                            if DSD_DF['Design Code'][indx] == Design_code and DSD_DF['Back URL'][indx] != '-' and DSD_DF['Placement'][indx].lower() == 'pocket':
                                print(Design_code , DSD_DF['Design Code'][indx])
                                print("Entered if block for Back URL Compensated Condition")
                                CP = float(BasePriceDF['Cost Price'][ix]) + BasePriceDF['Back Print Compensated'][0]
                                #Column T
                                back_print_cost_column = BasePriceDF['Back Print Compensated'][0]
                                break
                            elif DSD_DF['Design Code'][indx] == Design_code and DSD_DF['Back URL'][indx] != '-' and DSD_DF['Placement'][indx].lower() != 'pocket':
                                print(Design_code , DSD_DF['Design Code'][indx])
                                print("Entered if block for Back URL Condition")
                                CP = float(BasePriceDF['Cost Price'][ix]) + BasePriceDF['Back Print'][0]
                                #Column T
                                back_print_cost_column = BasePriceDF['Back Print'][0]
                                break
                            else:
                                print("Entered else block for Back URL")
                                CP = float(BasePriceDF['Cost Price'][ix])
                                #Column T
                                back_print_cost_column = 0


                        transaction_fee = 0.02 * SP
                        gst = float(BasePriceDF['GST'][ix])
                        print("GST " , gst)
                        reverse_gst_multiplier = gst/(gst+100)
                        print("Reverse GST Multiplier " , reverse_gst_multiplier)
                        reverse_gst = SP*reverse_gst_multiplier

                        #Column R
                        gst_column = reverse_gst
                        #Column S
                        product_cost_column = CP

                        print("Reverse GST " , reverse_gst)
                        print("Selling Price ", SP)
                        print("Cost Price ", CP)
                        print("Reverse GST " , reverse_gst)
                        print("Quantity " , Qty)
                        
                        percentage_split_f = int(percentage_split)/100

                        # val = ((SP-CP)*0.8 - reverse_gst)*Qty - transaction_fee
                        val = ((SP-CP)*percentage_split_f - reverse_gst)*Qty - transaction_fee
                        print("Value Prepaid ", val)

                        
                        #Column U
                        cod_charges_column = 0
                        #Column V
                        prepaid_transaction_charges_column = transaction_fee

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


            if gst_column != '':
                value_rounded_gst = "{:.2f}".format(float(gst_column))
            else:
                value_rounded_gst = gst_column

            wksCreatorOrders.update_value(addr=cell_espc , val=effective_sale_price_column)
            wksCreatorOrders.update_value(addr=cell_gc , val=value_rounded_gst)
            wksCreatorOrders.update_value(addr=cell_pcc , val=product_cost_column)
            wksCreatorOrders.update_value(addr=cell_bpcc , val=back_print_cost_column)
            wksCreatorOrders.update_value(addr=cell_ccc , val=cod_charges_column)
            wksCreatorOrders.update_value(addr=cell_ptcc , val=prepaid_transaction_charges_column)
            wksCreatorOrders.update_value(addr=cell_pcsc , val=pipeline_completion_status_column)


    CreatorOrdersDF_ProfitCalculation = CreatorOrdersDF[CreatorOrdersDF['Paid'].str.contains('FALSE')]
    CreatorOrdersDF_ProfitCalculation = CreatorOrdersDF_ProfitCalculation.loc[CreatorOrdersDF_ProfitCalculation['Status'] == 'DELIVERED']

    CreatorOrdersDF_Profit = CreatorOrdersDF_ProfitCalculation['Profit'].tolist()

    creator_payable_amount = return_unpaid_creator_profit(CreatorOrdersDF_Profit)

    return creator_payable_amount


 