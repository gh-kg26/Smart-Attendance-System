import pandas as pd
import logging

from scripts.makeAccessoriesSheet import makeWksAutoAccessories
from scripts.makeApparelSheet import makeWksAutoApparel
from scripts.makePhoneCoversSheet import makeWksAutoPhoneCovers
from scripts.makeProductSegregation import SegregateProducts
from scripts.push_line_itemID_to_sheet import makeDumpSheet

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def Pipeline(wksConfirmed , wksMasterShopifySheet, wksMasterOrders , wksMasterOrdersCOD ,wksDSD , wksErrorSKUs):

    logging.info('Passing Control to makeProductSegregation')
    SKUaccessories , SKUapparels, LineItemIDaccesories , LineItemIDapparels, LineItemIDphonecovers, LineItemID_nidhi_dump , ConfirmedDFPrepaidLineItemID, ConfirmedDFCODLineItemID , ConfirmedOrdersDF = SegregateProducts(wksConfirmed , wksMasterShopifySheet , wksErrorSKUs)
    # '''
    print("Apparels : " , LineItemIDapparels , "\nLENGTH : ", len(LineItemIDapparels))
    print("Accessories : " , LineItemIDaccesories , "\nLENGTH : ", len(LineItemIDaccesories))
    print("Phones Covers : " , LineItemIDphonecovers , "\nLENGTH : ", len(LineItemIDphonecovers))
    print("Dump : " , LineItemID_nidhi_dump , "\nLENGTH : ", len(LineItemID_nidhi_dump))
    logging.info('Passing Control to makeWksAutoApparel')
    finalApparels = makeWksAutoApparel(ConfirmedOrdersDF , wksMasterShopifySheet , wksDSD , SKUapparels , LineItemIDapparels)
    # logging.info("Apparels" , OrderIDapparels , "Count is" , len(OrderIDapparels))
    # logging.info('Passing Control to makeWksAutoAccessories')
    finalAccessories = makeWksAutoAccessories(ConfirmedOrdersDF , wksDSD , SKUaccessories , LineItemIDaccesories)
    # logging.info("Accessories" , OrderIDaccessories , "Count is" , len(OrderIDaccessories))
    # logging.info(ConfirmedOrdersDF)
    # logging.info(finalAccessories)
    finalPhoneCovers = makeWksAutoPhoneCovers(ConfirmedOrdersDF , wksDSD , LineItemIDphonecovers)
    '''

    print("INPUT DUMP : " , LineItemID_nidhi_dump)
    makeDumpSheet(ConfirmedOrdersDF , wksMasterShopifySheet , wksDSD , LineItemID_nidhi_dump)

    '''
    print("finalApparels:",finalApparels)
    finalSheet = finalApparels + finalAccessories + finalPhoneCovers
    
    finalSheetSorted = sorted(finalSheet, key=lambda x : x[1])
    # print(finalSheetSorted)
    finalDF = pd.DataFrame.from_records(finalSheetSorted)
    finalDFList = finalDF.values.tolist()
    # print(finalDF)
    # print("Number of COD Orders : " , len(ConfirmedDFCODLineItemID))
    # print("COD  : ", ConfirmedDFCODLineItemID)
    if len(ConfirmedDFCODLineItemID) != 0:
        dfCOD = finalDF[finalDF[0].isin(ConfirmedDFCODLineItemID)]
        dfCOD.drop(dfCOD.columns[[0]], axis = 1, inplace = True)
    
    # print(dfCOD)
    # print("Number of Prepaid Orders : " , len(ConfirmedDFPrepaidLineItemID))
    print(ConfirmedDFPrepaidLineItemID)
    if len(ConfirmedDFPrepaidLineItemID) != 0:
        dfPrepaid = finalDF[finalDF[0].isin(ConfirmedDFPrepaidLineItemID)]
        dfPrepaid.drop(dfPrepaid.columns[[0]], axis = 1, inplace = True)

    ConfirmedDF = wksConfirmed.get_as_df()
    ConfirmedDFCOD = ConfirmedDF[ConfirmedDF['LineItem_ID'].isin(ConfirmedDFCODLineItemID)]

    ConfirmedDFCODList = ConfirmedDFCOD.values.tolist()
    ConfirmedDFCODListSorted = sorted(ConfirmedDFCODList, key=lambda x : x[2])
    ConfirmedDFCODSorted = pd.DataFrame.from_records(ConfirmedDFCODListSorted)
    # print("COD Sorted : ", ConfirmedDFCODSorted)

    # logging.info(ConfirmedDFCODSorted)
    # print("DFCOD:" , dfCOD)
    if (ConfirmedDFCODSorted.shape[0] !=0):
        # print("Entered")
        ContactNumber = ConfirmedDFCODSorted[15].tolist()
        ContactName = ConfirmedDFCODSorted[9].tolist()
        print(ContactName , ContactNumber)
        # print("HERE")
        dfCOD['21'] = ContactName
        dfCOD['22'] = ContactNumber
        print("COD != 0")
        dfCODlist = dfCOD.values.tolist()

    # print(dfCODlist)
    
    # print("NNNN :", dfPrepaid)
    if len(ConfirmedDFPrepaidLineItemID) != 0:
        dfPrepaidlist = dfPrepaid.values.tolist()
    
    ShopifyMasterSheetDf = wksMasterShopifySheet.get_as_df()
    MasterOrdersSheetDF = wksMasterOrders.get_as_df()
    MasterOrdersCODSheetDF = wksMasterOrdersCOD.get_as_df()
    
    lastRow1 = ShopifyMasterSheetDf.shape[0] + 2
    lastRow2 = MasterOrdersSheetDF.shape[0] + 1
    lastRow3 = MasterOrdersCODSheetDF.shape[0] + 1

    # print(dfCODlist)
    # print("Nikhilesh" , dfPrepaidlist)
    # print("HH",finalDFList)

    # print("HERE" , finalDFList)

    if len(finalSheetSorted) !=0:
        wksMasterShopifySheet.insert_rows(lastRow1, values = finalDFList)
    #if dfPrepaid.shape[0] !=0:
    if len(ConfirmedDFPrepaidLineItemID) != 0:
        wksMasterOrders.insert_rows(lastRow2 , values = dfPrepaidlist)
    if (ConfirmedDFCODSorted.shape[0] !=0):
        wksMasterOrdersCOD.insert_rows(lastRow3 , values = dfCODlist)




    #wksMasterShopifySheet.insert_rows(750, values=finalSheetSorted)
    logging.info('Execution Complete : Pushed into all the sheets')
    # logging.info(finalSheet)
    # '''

