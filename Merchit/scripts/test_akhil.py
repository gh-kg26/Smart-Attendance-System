from pydoc import cli
import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging

def test_akhil(wksConfirmed , wksShadabOrders):
    
    # ShadabOrdersDF = wksShadabOrders.get_as_df()
    # # print(ShadabOrdersDF)
    # paid_status = ['TRUE']

    # # AA = ShadabOrdersDF['Paid'].tolist()
    # # print(AA)
    # # ShadabOrdersDF = ShadabOrdersDF[ShadabOrdersDF['Paid']]

    # # OrdersDF = OrdersDF1[~OrdersDF1['Name'].isin(CurrentConfirmedONo)]

    # ShadabOrdersDF = ShadabOrdersDF[~ShadabOrdersDF['PAID'].isin(paid_status)]

    wksShadabOrders.update_value(addr="P1" , val="HE")


a = 'Celeb-NidhiKumar-PhoneCover-04-Apple-iPhone-12'
b = a.split('-')
# print(b , b[0:3])
b = b[0:3]

print(len(b))

my_str = '-'.join(b)

print(my_str)