import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

with open('service_account.json') as source:
    info = json.load(source )
credentials = service_account.Credentials.from_service_account_info(info)

# client = pygsheets.authorize(service_account_file='/home/info/autolog/service_account.json')
client = pygsheets.authorize(service_account_file='service_account.json')

Color_Sheet = client.open('Automation Color Sheet')
wks_apparel_automation = Color_Sheet.worksheet_by_title('Automation - Apparel')
wks_DSD = Color_Sheet.worksheet_by_title('DSD')
wks_product_listing = Color_Sheet.worksheet_by_title('Product Listing')

Product_Listing_DF = wks_product_listing.get_as_df()
Accessories = Product_Listing_DF['All Accessories Types'].tolist()
Accessories.append('Phone Cover')
Accessories = list(filter(None, Accessories))

print(Accessories)

apparel_automation_df = wks_apparel_automation.get_as_df()

Design_Code = []
Placement = []
Design_URL = []
Dimensions = []
Branding = []
Front_Mockup_URL = []
Back_Mockup = []
Back_URL = []
Back_Dimensions = []

# Pop Grip	Mug	Tote Bag	Black Tote Bag	Phone Cover	Black Mug


for idx in apparel_automation_df.index:
    flag_accessory = False
    accessory = ''
    
    for accessory_type in Accessories:
        # print(accessory_type)
        # print(idx , accessory_type ,type(apparel_automation_df[accessory_type][idx]))
        if apparel_automation_df[accessory_type][idx] == "TRUE":
            # print("HELLO" , idx , accessory_type)
            flag_accessory = True
            accessory = accessory_type
            break


    print(flag_accessory , accessory)
    if flag_accessory:
        print("ENTERING HERE")
        # accessory = apparel_automation_df[accessory_type][idx].replace(" " , "")
        accessory = accessory.replace(" " , "")
        design_code_temp = 'Celeb-' + apparel_automation_df['Creator Name'][idx] + '-'+ accessory + "-"+ str(apparel_automation_df['Design Number'][idx])
        Design_Code.append(design_code_temp)
    else:
        print("ENTERING THERE")
        design_code_temp = 'Celeb-' + apparel_automation_df['Creator Name'][idx] + '-'+ str(apparel_automation_df['Design Number'][idx])
        Design_Code.append(design_code_temp)
        

    placement_temp = apparel_automation_df['PLACEMENT'][idx]
    if placement_temp != '':
        Placement.append(placement_temp)
    else:
        Placement.append('-')

    design_url_temp = apparel_automation_df['CMYK'][idx]
    if design_url_temp != '':
        Design_URL.append(design_url_temp)
    else:
        Design_URL.append('-')

    dimensions_temp = apparel_automation_df['W X H'][idx]
    if dimensions_temp != '':
        Dimensions.append(dimensions_temp)
    else:
        Dimensions.append('-')

    branding_temp = apparel_automation_df['Branding'][idx]
    if branding_temp != '':
        Branding.append(branding_temp)
    else:
        Branding.append('-')

    front_mockup_temp = apparel_automation_df['Front Mockup URL'][idx]
    if front_mockup_temp != '':
        Front_Mockup_URL.append(front_mockup_temp)
    else:
        Front_Mockup_URL.append('-')

    back_mockup = apparel_automation_df['Back Mockup URL'][idx]
    if back_mockup != '':
        Back_Mockup.append(back_mockup)
    else:
        Back_Mockup.append('-')

    back_url_temp = apparel_automation_df['Back CMYK'][idx]
    if back_url_temp != '':
        Back_URL.append(back_url_temp)
    else:
        Back_URL.append('-')

    back_dimension_temp = apparel_automation_df['BACK W X H'][idx]
    if back_dimension_temp != '':
        Back_Dimensions.append(back_dimension_temp)
    else:
        Back_Dimensions.append('-')


finalo = list(zip(Design_Code , Placement , Design_URL, Dimensions, Branding, Front_Mockup_URL, Back_Mockup, Back_URL, Back_Dimensions))
final = [list(ele) for ele in finalo]

DSD_DF=wks_DSD.get_as_df()

lastRow = DSD_DF.shape[0]
lastRow = lastRow + 1

wks_DSD.insert_rows(lastRow, values=final)