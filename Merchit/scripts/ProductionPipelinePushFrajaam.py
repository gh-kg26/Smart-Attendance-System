import pandas as pd
import logging

from scripts.makeAccessoriesSheet import makeWksAutoAccessories
from scripts.makeApparelSheet import makeWksAutoApparel
from scripts.makeProductSegregation import SegregateProducts

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def PipelineFrajaam(wksConfirmed , wksMasterShopifySheet, wksMasterOrders , wksMasterOrdersCOD ,wksDSD):

    logging.info('Passing Control to makeProductSegregation')
    SKUaccessories , SKUapparels, OrderIDaccessories , OrderIDapparels, OrderIDphonecovers , ConfirmedDFPrepaidono, ConfirmedDFCODono , ConfirmedOrdersDF = SegregateProducts(wksConfirmed , wksMasterShopifySheet)
    # logging.info("data")
    # logging.info(SKUaccessories)
    # logging.info(SKUapparels)
    # logging.info(OrderIDaccessories)
    # logging.info(OrderIDapparels)

    logging.info('Passing Control to makeWksAutoApparel')
    finalApparels = makeWksAutoApparel(ConfirmedOrdersDF , wksMasterShopifySheet , wksDSD , SKUapparels , OrderIDapparels)
    logging.info("Apparels" , OrderIDapparels , "Count is" , len(OrderIDapparels))
    logging.info('Passing Control to makeWksAutoAccessories')
    finalAccessories = makeWksAutoAccessories(ConfirmedOrdersDF , wksDSD , SKUaccessories , OrderIDaccessories)
    logging.info("Accessories" , OrderIDaccessories , "Count is" , len(OrderIDaccessories))
    # logging.info(ConfirmedOrdersDF)
    # logging.info(finalAccessories)


    #finalSheet = finalApparels + finalAccessories
    finalSheet = finalApparels + finalAccessories
    # logging.info(finalSheet)

    # finalDF = pd.DataFrame(finalSheet)


    finalSheetSorted = sorted(finalSheet, key=lambda x : x[1])
    finalDF = pd.DataFrame.from_records(finalSheetSorted)

    dfCOD = finalDF[finalDF[1].isin(ConfirmedDFCODono)]
    dfPrepaid = finalDF[finalDF[1].isin(ConfirmedDFPrepaidono)]

    ConfirmedDF =wksConfirmed.get_as_df()
    ConfirmedDFCOD = ConfirmedDF[ConfirmedDF['OrderName'].isin(ConfirmedDFCODono)]

    ConfirmedDFCODList = ConfirmedDFCOD.values.tolist()
    ConfirmedDFCODListSorted = sorted(ConfirmedDFCODList, key=lambda x : x[2])
    ConfirmedDFCODSorted = pd.DataFrame.from_records(ConfirmedDFCODListSorted)

    # logging.info(ConfirmedDFCODSorted)

    if(ConfirmedDFCODSorted.shape[0] !=0):

        ContactNumber = ConfirmedDFCODSorted[15].tolist()
        ContactName = ConfirmedDFCODSorted[9].tolist()

        dfCOD['15'] = ContactName
        dfCOD['16'] = ContactNumber


    # logging.info(dfCOD)

    

    
    #ConfirmedDFCOD.sort_values('OrderName')
    # final_df = ConfirmedDFCOD.sort_values(by=['OrderName'], ascending=True)


    # logging.info(dfCOD)
    # logging.info(ContactName)


    dfCODlist = dfCOD.values.tolist()
    dfPrepaidlist = dfPrepaid.values.tolist()
    
    ShopifyMasterSheetDf = wksMasterShopifySheet.get_as_df()
    MasterOrdersSheetDF = wksMasterOrders.get_as_df()
    MasterOrdersCODSheetDF = wksMasterOrdersCOD.get_as_df()
    
    lastRow1 = ShopifyMasterSheetDf.shape[0] + 1
    lastRow2 = MasterOrdersSheetDF.shape[0] + 1
    lastRow3 = MasterOrdersCODSheetDF.shape[0] + 1

    wksMasterShopifySheet.insert_rows(lastRow1, values = finalSheet)
    wksMasterOrders.insert_rows(lastRow2 , values = dfPrepaidlist)
    wksMasterOrdersCOD.insert_rows(lastRow3 , values = dfCODlist)




    #wksMasterShopifySheet.insert_rows(750, values=finalSheetSorted)
    logging.info('Execution Complete : Pushed into all the sheets')
    # logging.info(finalSheet)


