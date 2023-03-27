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
wks_test_automation = Color_Sheet.worksheet_by_title('Test Automation')
wks_product_listing_price = Color_Sheet.worksheet_by_title('Product Listing Price')
wks_product_listing = Color_Sheet.worksheet_by_title('Product Listing')


product_listing_price_df = wks_product_listing_price.get_as_df()
product_listing_df = wks_product_listing.get_as_df()
apparel_automation_df = wks_apparel_automation.get_as_df()

print(product_listing_price_df)
# Handle_list = apparel_automation_df['Title'].tolist()
# Title_list = apparel_automation_df['Title'].tolist()
# Vendor_list = apparel_automation_df['Creator Name'].tolist()
# Custom_Tags = apparel_automation_df['Creator Name'].tolist()
handle=[]
title = []
vendor = []
Custom_Product_Type = []
Option1_value = []
Option2_value = []
Variant_SKU = []
tags = []
body = []
standardized_product_type = []
published = []
option1_name = []
option2_name = []
option3_name = []
option3_value = []
variant_grams = []
variant_inventory_tracker = []
variant_inventory_policy = []
variant_fulfillment_service = []
variant_requires_shipping = []
variant_taxable = []
variant_barcode = []
image_src = []
image_position = []
image_alt_text = []
gift_card = []
seo_title = []
seo_description = []
google_shopping_product_category = []
google_shopping_gender = []
google_shopping_age_group = []
google_shopping_mpn = []
google_shopping_adwords = []
google_shopping_adwords_labels = []
google_shopping_condition = []
google_shopping_custom_product = []
google_shopping_custom_label_0 = []
google_shopping_custom_label_1 = []
google_shopping_custom_label_2 = []
google_shopping_custom_label_3 = []
google_shopping_custom_label_4 = []
variant_image = []
variant_weight_unit = []
variant_tax_code = []
cost_per_item = []
price_international = []
compare_at_price = []
status = []
variant_price = []
variant_compare_at_price = []

#TODO
#1. NAVY BLUE , CROP TOP, POP GRIP,TOTE BAG,PHONE COVER ADD SPACE IN VARIATION
#2. CROP TOP Sizing only till XL

colors = product_listing_df['All Colors'].tolist()
apparels = product_listing_df['All Apparels Types'].tolist()
accessories = product_listing_df['All Accessories Types'].tolist()
sizes = product_listing_df['All Apparel Sizes'].tolist()
phone_models = product_listing_df['All Phone Models'].tolist()

# print(product_listing_df['Prod'].tolist())

colors = list(filter(None, colors))
apparels = list(filter(None, apparels))
accessories = list(filter(None, accessories))
sizes = list(filter(None, sizes))


# print(colors , apparels , accessories, sizes)

# colors = ['WHITE' , 'BLACK' , 'GREY' , 'NAVY BLUE' , 'RED' , 'PINK' , 'OLIVE GREEN' , 'ROYAL BLUE' , 'AQUA BLUE' , 'MINT GREEN']
# apparels = ['Half' , 'Croptop' , 'Hoodie' , 'Sweatshirt']
# accessories = ['PopGrip' , 'Mug' , 'ToteBag' , 'Phone Cover']
# sizes = ['S' , 'M' , 'L' , 'XL' , 'XXL']

for idx in apparel_automation_df.index:
    available_colors = []
    available_types = []
    available_types_accessories = []
    # if apparel_automation_df['WHITE'] == 'TRUE':
    #     colors.append('WHITE')
    for color in colors:
        if apparel_automation_df[color][idx] == 'TRUE':
            available_colors.append(color)
        
    for apparel in apparels:
        if apparel_automation_df[apparel][idx] == 'TRUE':
            available_types.append(apparel)

    # print(len(available_types_accessories))
    # print(len(available_types))

    for accessory in accessories:
        if apparel_automation_df[accessory][idx] == 'TRUE':
            available_types_accessories.append(accessory)

    # map = 0
    #First Encounter
    #available_type = ['HALF' , 'HOODIE']
    if len(available_types) != 0:  
        for available_type in available_types:
            for indx in product_listing_price_df.index:
                # print("COMPARING {0} with {1}".format(available_type , product_listing_price_df['Prod'][indx]))
                if product_listing_price_df['Prod'][indx].lower() == available_type.lower():
                    variant_price_value = product_listing_price_df['SP'][indx]
                    variant_compare_at_price_value = product_listing_price_df['Compared price'][indx]
                    display_available_type = product_listing_price_df['Display Product Type'][indx]
            flag = 0
            for available_color in available_colors:
                for size in sizes:

                    # print("PRINTING INDEX : " , idx)

                    temp = 'Celeb-' + apparel_automation_df['Creator Name'][idx] + '-'+ str(apparel_automation_df['Design Number'][idx]) + '-' + available_color + '-'+available_type + '-' + size
                    temp = temp.replace(" " , "")
                    # print(temp)
                    # handle_tmp = apparel_automation_df['Title'][idx] + " - " + available_color + " - " + size

                    title_tmp = apparel_automation_df['Title'][idx] + " " + display_available_type

                    # if idx!=0:
                    #     if apparel_automation_df['Title'][idx] == apparel_automation_df['Title'][idx-1]:
                    #         map = 1

                    #handle_tmp = apparel_automation_df['Title'][idx]
                    handle_tmp = title_tmp
                    handle_tmp = handle_tmp.replace(" ", "-")

                    tags_tmp = 'Celebrity Merchandise , {0}'.format(apparel_automation_df['Creator Name'][idx])
                    # handle_tmp = 
                    # print(handle_tmp)
                    
                    # if size != sizes[0] and available_color != available_colors[0]:
                    #     Custom_Product_Type.append('')
                    
                    if title_tmp not in title:
                        #Add one new line
                        # if flag  == 0 and map == 0:
                        if flag  == 0:
                            Custom_Product_Type.append(display_available_type)
                            vendor.append(apparel_automation_df['Creator Name'][idx])   
                            #title.append(apparel_automation_df['Title'][idx])
                            title.append(title_tmp)
                            tags.append(tags_tmp)
                            # tags.append('Celebrity Merchandise')
                            # tags.append(apparel_automation_df['Creator Name'][idx])
                            published.append('FALSE')
                            option1_name.append('Color')
                            option2_name.append('Size')
                            gift_card.append('FALSE')
                            status.append('draft')
                            flag=1
                        
                        #Pushes all data
                        #Condition to check if title[idx] == title[idx-1] && ____ && ____ && idx !=0
                        # elif idx!=0 and (title[idx] == title[idx-1]) and (apparel_automation_df['Creator Name'][idx] == apparel_automation_df['Creator Name'][idx-1]) and (apparel_automation_df[available_type][idx] == apparel_automation_df[available_type][idx-1]):
                        else:
                            Custom_Product_Type.append('')
                            vendor.append('')   
                            title.append('')
                            tags.append('')
                            published.append('')
                            option1_name.append('')
                            option2_name.append('')
                            gift_card.append('')
                            status.append('')
                        handle.append(handle_tmp)
                        standardized_product_type.append('')
                        Option1_value.append(available_color)
                        Option2_value.append(size)
                        Variant_SKU.append(temp)
                        body.append('')
                        option3_name.append('')
                        option3_value.append('')
                        variant_grams.append('0')
                        variant_inventory_tracker.append('shopify')
                        variant_inventory_policy.append('deny')
                        variant_fulfillment_service.append('manual')
                        variant_price.append(str(variant_price_value))
                        variant_compare_at_price.append(str(variant_compare_at_price_value))
                        #variant_price.append('ENTER HERE')
                        #variant_compare_at_price.append('ENTER HERE')
                        variant_requires_shipping.append('TRUE')
                        variant_taxable.append('TRUE')
                        variant_barcode.append('')
                        image_src.append('')
                        image_position.append('')
                        image_alt_text.append('')
                        seo_title.append('')
                        seo_description.append('')
                        google_shopping_product_category.append('')
                        google_shopping_gender.append('')                
                        google_shopping_age_group.append('')
                        google_shopping_mpn.append('')
                        google_shopping_adwords.append('')
                        google_shopping_adwords_labels.append('')
                        google_shopping_condition.append('')
                        google_shopping_custom_product.append('')
                        google_shopping_custom_label_0.append('')
                        google_shopping_custom_label_1.append('')
                        google_shopping_custom_label_2.append('')
                        google_shopping_custom_label_3.append('')
                        google_shopping_custom_label_4.append('')
                        variant_image.append('')
                        variant_weight_unit.append('kg')
                        variant_tax_code.append('')
                        cost_per_item.append('')
                        price_international.append('')
                        compare_at_price.append('')

                    else : 

                        final_index = max(index for index, item in enumerate(handle) if item == handle_tmp)
                        final_index = final_index + 1
                        Custom_Product_Type.insert(final_index , '')
                        vendor.insert(final_index ,'')   
                        title.insert(final_index ,'')
                        tags.insert(final_index ,'')
                        published.insert(final_index ,'')
                        option1_name.insert(final_index ,'')
                        option2_name.insert(final_index ,'')
                        gift_card.insert(final_index ,'')
                        status.insert(final_index ,'')
                        handle.insert(final_index ,handle_tmp)
                        standardized_product_type.insert(final_index ,'')
                        Option1_value.insert(final_index ,available_color)
                        Option2_value.insert(final_index ,size)
                        Variant_SKU.insert(final_index ,temp)
                        body.insert(final_index ,'')
                        option3_name.insert(final_index ,'')
                        option3_value.insert(final_index ,'')
                        variant_grams.insert(final_index ,'0')
                        variant_inventory_tracker.insert(final_index ,'shopify')
                        variant_inventory_policy.insert(final_index ,'deny')
                        variant_fulfillment_service.insert(final_index ,'manual')
                        variant_price.insert(final_index ,str(variant_price_value))
                        variant_compare_at_price.insert(final_index ,str(variant_compare_at_price_value))
                        #variant_price.append('ENTER HERE')
                        #variant_compare_at_price.append('ENTER HERE')
                        variant_requires_shipping.insert(final_index ,'TRUE')
                        variant_taxable.insert(final_index ,'TRUE')
                        variant_barcode.insert(final_index ,'')
                        image_src.insert(final_index ,'')
                        image_position.insert(final_index ,'')
                        image_alt_text.insert(final_index ,'')
                        seo_title.insert(final_index ,'')
                        seo_description.insert(final_index ,'')
                        google_shopping_product_category.insert(final_index ,'')
                        google_shopping_gender.insert(final_index ,'')                
                        google_shopping_age_group.insert(final_index ,'')
                        google_shopping_mpn.insert(final_index ,'')
                        google_shopping_adwords.insert(final_index ,'')
                        google_shopping_adwords_labels.insert(final_index ,'')
                        google_shopping_condition.insert(final_index ,'')
                        google_shopping_custom_product.insert(final_index ,'')
                        google_shopping_custom_label_0.insert(final_index ,'')
                        google_shopping_custom_label_1.insert(final_index ,'')
                        google_shopping_custom_label_2.insert(final_index ,'')
                        google_shopping_custom_label_3.insert(final_index ,'')
                        google_shopping_custom_label_4.insert(final_index ,'')
                        variant_image.insert(final_index ,'')
                        variant_weight_unit.insert(final_index ,'kg')
                        variant_tax_code.insert(final_index ,'')
                        cost_per_item.insert(final_index ,'')
                        price_international.insert(final_index ,'')
                        compare_at_price.insert(final_index ,'')
    if len(available_types_accessories) != 0:
        for available_type in available_types_accessories:
            for indx in product_listing_price_df.index:
                if product_listing_price_df['Prod'][indx].lower() == available_type.lower():
                    variant_price_value = product_listing_price_df['SP'][indx]
                    variant_compare_at_price_value = product_listing_price_df['Compared price'][indx]
                    display_available_type = product_listing_price_df['Display Product Type'][indx]
            flag = 0
            for available_color in available_colors:
                    
                    # print("PRINTING INDEX : " , idx)

                    temp = 'Celeb-' + apparel_automation_df['Creator Name'][idx]+ '-'+available_type + '-'+ str(apparel_automation_df['Design Number'][idx]) 
                    temp = temp.replace(" " , "")
                    # print(temp)

                    title_tmp = apparel_automation_df['Title'][idx] + " " + display_available_type
                    # if idx!=0:
                    #     if apparel_automation_df['Title'][idx] == apparel_automation_df['Title'][idx+1] and :
                    #         map = 1

                    # handle_tmp = apparel_automation_df['Title'][idx] + " - " + available_color + " - " + size
                    # handle_tmp = apparel_automation_df['Title'][idx]
                    # handle_tmp.replace(" ", "-")
                    # handle_tmp = 

                    handle_tmp = title_tmp
                    handle_tmp = handle_tmp.replace(" ", "-")
                    # print(handle_tmp)
                    
                    tags_tmp = 'Celebrity Merchandise , {0}'.format(apparel_automation_df['Creator Name'][idx])
                    

                    # if size != sizes[0] and available_color != available_colors[0]:
                    #     Custom_Product_Type.append('')

                    if title_tmp not in title:
                        if flag  == 0:
                            Custom_Product_Type.append(display_available_type)
                            vendor.append(apparel_automation_df['Creator Name'][idx])   
                            # title.append(apparel_automation_df['Title'][idx])
                            title.append(title_tmp)
                            #tags.append('Celebrity Merchandise')
                            tags.append(tags_tmp)
                            # tags.append(apparel_automation_df['Creator Name'][idx])
                            published.append('FALSE')
                            option1_name.append('Color')
                            option2_name.append('')
                            gift_card.append('FALSE')
                            status.append('draft')
                            flag=1
                        else:
                            Custom_Product_Type.append('')
                            vendor.append('')   
                            title.append('')
                            tags.append('')
                            published.append('')
                            option1_name.append('')
                            option2_name.append('')
                            gift_card.append('')
                            status.append('')
                        handle.append(handle_tmp)
                        standardized_product_type.append('')
                        Option1_value.append(available_color)
                        Option2_value.append('')
                        Variant_SKU.append(temp)
                        body.append('')
                        option3_name.append('')
                        option3_value.append('')
                        variant_grams.append('0')
                        variant_inventory_tracker.append('shopify')
                        variant_inventory_policy.append('deny')
                        variant_fulfillment_service.append('manual')
                        variant_price.append(str(variant_price_value))
                        variant_compare_at_price.append(str(variant_compare_at_price_value))
                        #variant_price.append('ENTER HERE')
                        #variant_compare_at_price.append('ENTER HERE')
                        variant_requires_shipping.append('TRUE')
                        variant_taxable.append('TRUE')
                        variant_barcode.append('')
                        image_src.append('')
                        image_position.append('')
                        image_alt_text.append('')
                        seo_title.append('')
                        seo_description.append('')
                        google_shopping_product_category.append('')
                        google_shopping_gender.append('')                
                        google_shopping_age_group.append('')
                        google_shopping_mpn.append('')
                        google_shopping_adwords.append('')
                        google_shopping_adwords_labels.append('')
                        google_shopping_condition.append('')
                        google_shopping_custom_product.append('')
                        google_shopping_custom_label_0.append('')
                        google_shopping_custom_label_1.append('')
                        google_shopping_custom_label_2.append('')
                        google_shopping_custom_label_3.append('')
                        google_shopping_custom_label_4.append('')
                        variant_image.append('')
                        variant_weight_unit.append('kg')
                        variant_tax_code.append('')
                        cost_per_item.append('')
                        price_international.append('')
                        compare_at_price.append('')
                    else:

                        final_index = max(index for index, item in enumerate(handle) if item == handle_tmp)
                        final_index = final_index + 1
                        Custom_Product_Type.insert(final_index , '')
                        vendor.insert(final_index ,'')   
                        title.insert(final_index ,'')
                        tags.insert(final_index ,'')
                        published.insert(final_index ,'')
                        option1_name.insert(final_index ,'')
                        option2_name.insert(final_index ,'')
                        gift_card.insert(final_index ,'')
                        status.insert(final_index ,'')
                        handle.insert(final_index ,handle_tmp)
                        standardized_product_type.insert(final_index ,'')
                        Option1_value.insert(final_index ,available_color)
                        Option2_value.insert(final_index ,'')
                        Variant_SKU.insert(final_index ,temp)
                        body.insert(final_index ,'')
                        option3_name.insert(final_index ,'')
                        option3_value.insert(final_index ,'')
                        variant_grams.insert(final_index ,'0')
                        variant_inventory_tracker.insert(final_index ,'shopify')
                        variant_inventory_policy.insert(final_index ,'deny')
                        variant_fulfillment_service.insert(final_index ,'manual')
                        variant_price.insert(final_index ,str(variant_price_value))
                        variant_compare_at_price.insert(final_index ,str(variant_compare_at_price_value))
                        #variant_price.append('ENTER HERE')
                        #variant_compare_at_price.append('ENTER HERE')
                        variant_requires_shipping.insert(final_index ,'TRUE')
                        variant_taxable.insert(final_index ,'TRUE')
                        variant_barcode.insert(final_index ,'')
                        image_src.insert(final_index ,'')
                        image_position.insert(final_index ,'')
                        image_alt_text.insert(final_index ,'')
                        seo_title.insert(final_index ,'')
                        seo_description.insert(final_index ,'')
                        google_shopping_product_category.insert(final_index ,'')
                        google_shopping_gender.insert(final_index ,'')                
                        google_shopping_age_group.insert(final_index ,'')
                        google_shopping_mpn.insert(final_index ,'')
                        google_shopping_adwords.insert(final_index ,'')
                        google_shopping_adwords_labels.insert(final_index ,'')
                        google_shopping_condition.insert(final_index ,'')
                        google_shopping_custom_product.insert(final_index ,'')
                        google_shopping_custom_label_0.insert(final_index ,'')
                        google_shopping_custom_label_1.insert(final_index ,'')
                        google_shopping_custom_label_2.insert(final_index ,'')
                        google_shopping_custom_label_3.insert(final_index ,'')
                        google_shopping_custom_label_4.insert(final_index ,'')
                        variant_image.insert(final_index ,'')
                        variant_weight_unit.insert(final_index ,'kg')
                        variant_tax_code.insert(final_index ,'')
                        cost_per_item.insert(final_index ,'')
                        price_international.insert(final_index ,'')
                        compare_at_price.insert(final_index ,'')


    if apparel_automation_df['Phone Cover'][idx] == 'TRUE':
        # print(phone_models , type(phone_models))

        latitude = 0
        for model in phone_models:
            for indx in product_listing_price_df.index:
                if product_listing_price_df['Prod'][indx].lower() == 'Phone Cover'.lower():
                    variant_price_value = product_listing_price_df['SP'][indx]
                    variant_compare_at_price_value = product_listing_price_df['Compared price'][indx]
                    display_available_type = product_listing_price_df['Display Product Type'][indx]
            # print(model)
            model_hyphen = model.replace(" " , "-")
            # print(model)
            temp = 'Celeb-' + apparel_automation_df['Creator Name'][idx] + '-PhoneCover-' + str(apparel_automation_df['Design Number'][idx]) +"-" + model_hyphen
            temp = temp.replace(" " , "")
            # print(temp)

            title_tmp = apparel_automation_df['Title'][idx] + " Phone Cover"
            handle_tmp = title_tmp
            handle_tmp = handle_tmp.replace(" ", "-")

            tags_tmp = 'Celebrity Merchandise , {0}'.format(apparel_automation_df['Creator Name'][idx])

            if title_tmp not in title:
                if latitude  == 0:
                    Custom_Product_Type.append('Phone Cover')
                    vendor.append(apparel_automation_df['Creator Name'][idx])   
                    # title.append(apparel_automation_df['Title'][idx])
                    title.append(title_tmp)
                    #tags.append('Celebrity Merchandise')
                    tags.append(tags_tmp)
                    # tags.append(apparel_automation_df['Creator Name'][idx])
                    published.append('FALSE')
                    option1_name.append('Model')
                    option2_name.append('')
                    gift_card.append('FALSE')
                    status.append('draft')
                    latitude = 1
                else:
                    Custom_Product_Type.append('')
                    vendor.append('')   
                    title.append('')
                    tags.append('')
                    published.append('')
                    option1_name.append('')
                    option2_name.append('')
                    gift_card.append('')
                    status.append('')
                handle.append(handle_tmp)
                standardized_product_type.append('')
                Option1_value.append(model)
                Option2_value.append('')
                Variant_SKU.append(temp)
                body.append('')
                option3_name.append('')
                option3_value.append('')
                variant_grams.append('0')
                variant_inventory_tracker.append('shopify')
                variant_inventory_policy.append('deny')
                variant_fulfillment_service.append('manual')
                variant_price.append(str(variant_price_value))
                variant_compare_at_price.append(str(variant_compare_at_price_value))
                #variant_price.append('ENTER HERE')
                #variant_compare_at_price.append('ENTER HERE')
                variant_requires_shipping.append('TRUE')
                variant_taxable.append('TRUE')
                variant_barcode.append('')
                image_src.append('')
                image_position.append('')
                image_alt_text.append('')
                seo_title.append('')
                seo_description.append('')
                google_shopping_product_category.append('')
                google_shopping_gender.append('')                
                google_shopping_age_group.append('')
                google_shopping_mpn.append('')
                google_shopping_adwords.append('')
                google_shopping_adwords_labels.append('')
                google_shopping_condition.append('')
                google_shopping_custom_product.append('')
                google_shopping_custom_label_0.append('')
                google_shopping_custom_label_1.append('')
                google_shopping_custom_label_2.append('')
                google_shopping_custom_label_3.append('')
                google_shopping_custom_label_4.append('')
                variant_image.append('')
                variant_weight_unit.append('kg')
                variant_tax_code.append('')
                cost_per_item.append('')
                price_international.append('')
                compare_at_price.append('')
            else:

                final_index = max(index for index, item in enumerate(handle) if item == handle_tmp)
                final_index = final_index + 1
                Custom_Product_Type.insert(final_index , '')
                vendor.insert(final_index ,'')   
                title.insert(final_index ,'')
                tags.insert(final_index ,'')
                published.insert(final_index ,'')
                option1_name.insert(final_index ,'')
                option2_name.insert(final_index ,'')
                gift_card.insert(final_index ,'')
                status.insert(final_index ,'')
                handle.insert(final_index ,handle_tmp)
                standardized_product_type.insert(final_index ,'')
                Option1_value.insert(final_index ,model)
                Option2_value.insert(final_index ,'')
                Variant_SKU.insert(final_index ,temp)
                body.insert(final_index ,'')
                option3_name.insert(final_index ,'')
                option3_value.insert(final_index ,'')
                variant_grams.insert(final_index ,'0')
                variant_inventory_tracker.insert(final_index ,'shopify')
                variant_inventory_policy.insert(final_index ,'deny')
                variant_fulfillment_service.insert(final_index ,'manual')
                variant_price.insert(final_index ,str(variant_price_value))
                variant_compare_at_price.insert(final_index ,str(variant_compare_at_price_value))
                #variant_price.append('ENTER HERE')
                #variant_compare_at_price.append('ENTER HERE')
                variant_requires_shipping.insert(final_index ,'TRUE')
                variant_taxable.insert(final_index ,'TRUE')
                variant_barcode.insert(final_index ,'')
                image_src.insert(final_index ,'')
                image_position.insert(final_index ,'')
                image_alt_text.insert(final_index ,'')
                seo_title.insert(final_index ,'')
                seo_description.insert(final_index ,'')
                google_shopping_product_category.insert(final_index ,'')
                google_shopping_gender.insert(final_index ,'')                
                google_shopping_age_group.insert(final_index ,'')
                google_shopping_mpn.insert(final_index ,'')
                google_shopping_adwords.insert(final_index ,'')
                google_shopping_adwords_labels.insert(final_index ,'')
                google_shopping_condition.insert(final_index ,'')
                google_shopping_custom_product.insert(final_index ,'')
                google_shopping_custom_label_0.insert(final_index ,'')
                google_shopping_custom_label_1.insert(final_index ,'')
                google_shopping_custom_label_2.insert(final_index ,'')
                google_shopping_custom_label_3.insert(final_index ,'')
                google_shopping_custom_label_4.insert(final_index ,'')
                variant_image.insert(final_index ,'')
                variant_weight_unit.insert(final_index ,'kg')
                variant_tax_code.insert(final_index ,'')
                cost_per_item.insert(final_index ,'')
                price_international.insert(final_index ,'')
                compare_at_price.insert(final_index ,'')

            


finalo = list(zip(handle , title , body , vendor, standardized_product_type, Custom_Product_Type, tags, published, option1_name ,Option1_value, option2_name , Option2_value, option3_name , option3_value, Variant_SKU , variant_grams , variant_inventory_tracker , variant_inventory_policy , variant_fulfillment_service , variant_price, variant_compare_at_price , variant_requires_shipping , variant_taxable , variant_barcode , image_src , image_position , image_alt_text , gift_card,seo_title , seo_description  , google_shopping_product_category , google_shopping_gender , google_shopping_age_group , google_shopping_mpn , google_shopping_adwords , google_shopping_adwords_labels , google_shopping_condition , google_shopping_custom_product , google_shopping_custom_label_0 , google_shopping_custom_label_1 , google_shopping_custom_label_2 , google_shopping_custom_label_3 , google_shopping_custom_label_4 , variant_image , variant_weight_unit , variant_tax_code , cost_per_item , price_international , compare_at_price , status ))
final = [list(ele) for ele in finalo]

# print(final)

# print(finalo)

TestAutomationDF=wks_test_automation.get_as_df()

lastRow = TestAutomationDF.shape[0]
lastRow = lastRow + 1

wks_test_automation.insert_rows(lastRow, values=final)