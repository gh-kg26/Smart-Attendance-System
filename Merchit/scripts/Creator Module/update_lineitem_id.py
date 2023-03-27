def update_lineitemID(wksCreatorOrders , wksConfirmed):
    CreatorOrdersDF = wksCreatorOrders.get_as_df()
    ConfirmedOrdersDF = wksConfirmed.get_as_df()
    for idx in CreatorOrdersDF.index:
        for index in ConfirmedOrdersDF.index:
            if CreatorOrdersDF['OrderName'][idx] == ConfirmedOrdersDF['OrderName'][index] and CreatorOrdersDF['SKU'][idx] == ConfirmedOrdersDF['SKU'][index]:
                print(CreatorOrdersDF['OrderName'][idx])
                lineitem_ID =  ConfirmedOrdersDF['LineItem_ID'][index]
                cell_to_update = 'A' + str(idx+2)
                wksCreatorOrders.update_value(addr=cell_to_update , val=lineitem_ID)               