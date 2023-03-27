import pygsheets
from scripts.makeCreatorSheetTemplate import *

from scripts.update_single_SR_Profit import *

from scripts.update_lineitem_id import update_lineitemID

def makeCreatorSheet(wksConfirmed , wksSauravSinhaOrders , wksTISOrders, wksPCMBMemesOrders , wksMriDulOrders , wksViditOrders , wksAshwinOrders, wksTirthOrders , wksMemeMandirOrders , wksTMPOrders , wksNaginaOrders , wksItSuchOrders , wksDevJoshiOrders , wksUnfinanceOrders , wksTapeATaleOrders , wksShadabOrders , wksSharmaSistersOrders , wksGuluaOrders):
    # print("hello")

    # SauravSinhaList = generateCreatorSheetList(wksConfirmed , 'SauravSinha' , wksSauravSinhaOrders)
    # VDList = generateCreatorSheetList(wksConfirmed , 'ViditGujrathi' , wksViditOrders)
    # AshwinList = generateCreatorSheetList(wksConfirmed , 'AshwinBhaskar' , wksAshwinOrders)
    # TirthList = generateCreatorSheetList(wksConfirmed , "TirthParsana" , wksTirthOrders )
    # MemeMandirList = generateCreatorSheetList(wksConfirmed , "MemeMandir" , wksMemeMandirOrders )
    # TMPList = generateCreatorSheetList(wksConfirmed , "TMP" , wksTMPOrders)
    # NaginaList = generateCreatorSheetList(wksConfirmed , "Nagina" , wksNaginaOrders)
    # ItSuchList = generateCreatorSheetList(wksConfirmed , "ITSuch" , wksItSuchOrders)
    # DevJoshiList = generateCreatorSheetList(wksConfirmed , "DevJoshi" , wksDevJoshiOrders)
    # UnfinanceList = generateCreatorSheetList(wksConfirmed , "Unfinance", wksUnfinanceOrders)
    # MridulList = generateCreatorSheetList(wksConfirmed , "TheMridul" , wksMriDulOrders)
    # TapeATaleList = generateCreatorSheetList(wksConfirmed, "TAT" ,  wksTapeATaleOrders)
    # ShadabList = generateCreatorSheetList(wksConfirmed , "Shadab" , wksShadabOrders)
    # SharmaSistersList = generateCreatorSheetList(wksConfirmed , "SharmaSisters" , wksSharmaSistersOrders)
    # GuluaOrdersList = generateCreatorSheetList(wksConfirmed , "Gulua" , wksGuluaOrders)

    update_tracking_status(wksSauravSinhaOrders)
    # update_lineitemID(wksSauravSinhaOrders , wksConfirmed)

    # return VDList