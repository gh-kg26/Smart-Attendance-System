def makeWksErrorSKUs(ConfirmedOrdersDF1 , wksErrorSKUs , SKUFlags ,LineItemIDflags):
    
    ErrorOrdersDF = ConfirmedOrdersDF1[ConfirmedOrdersDF1['LineItem_ID'].isin(LineItemIDflags)]
    final = ErrorOrdersDF.values.tolist()


    CurrentErrorsOrdersDF = wksErrorSKUs.get_as_df()
    lastRow = CurrentErrorsOrdersDF.shape[0]
    lastRow = lastRow + 1

    wksErrorSKUs.insert_rows(lastRow, values=final)