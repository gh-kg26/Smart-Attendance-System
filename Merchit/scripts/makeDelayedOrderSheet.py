import datetime
import pygsheets

from scripts.GetSRStatus import *

def find_delayed_days(wksMasterShopifySheet , wksOrderDelays):

    MasterSheetDF = wksMasterShopifySheet.get_as_df()
    # MasterSheetDF_Filtered = MasterSheetDF.loc[MasterSheetDF['Order Status'] == '']
    current_date = datetime.date.today()
    tracking_status_complete = ['DELIVERED' , 'RTO DELIVERED' , 'CANCELLED' , 'CANCELED' , 'REFUNDED' , 'COD ORDER NOT CONFIRMED' , 'CANCELLATION REQUESTED' , 'NO VALUE']
    for idx in MasterSheetDF.index:

        if MasterSheetDF['Order Status'][idx] not in tracking_status_complete:    

            cell_order_status = 'X' + str(idx+2)
            channel_orderID = MasterSheetDF['Order No'][idx]
            order_status = runner_function(channel_orderID)
            wksMasterShopifySheet.update_value(addr=cell_order_status , val=order_status)

    MasterSheetDF_Filtered = MasterSheetDF.loc[MasterSheetDF['Order Status'] == 'NEW'] 
    for ix in MasterSheetDF_Filtered.index:
        cell_order_delayed = 'Y' + str(ix+2)
        cell_flag_delayed = 'Z' + str(ix+2)
        channel_orderID = MasterSheetDF_Filtered['Order No'][ix]
        OrderDate = MasterSheetDF_Filtered['ORDER DATE'][ix]
        print(OrderDate)
        sep = 'T'
        b = OrderDate.split(sep, 1)[0]
        print(b)
        order_date = datetime.datetime.strptime(b, "%Y-%m-%d").date()
        # print(order_date , type(order_date))
        # order_date = datetime.datetime.strptime(OrderDate, "%Y-%m-%dT%H:%M:%SZ").date()
        days_delayed = (current_date - order_date).days
        days_delayed = str(days_delayed)
        
        OrderDate_str = str(OrderDate)

        if int(days_delayed) >= 5:
            wksMasterShopifySheet.update_value(addr=cell_flag_delayed , val='DELAYED SHIPMENT')
            
            dfOrderDelays = wksOrderDelays.get_as_df()
            lastRow = dfOrderDelays.shape[0] + 1

            #New sheet for delayed orders
            # gc = pygsheets.authorize(service_file='service_account.json')
            # sh = gc.open('Delayed Order Sheet')
            # delayed_orders_sheet = sh.worksheet('title', 'Delayed Orders')
            row_to_append = [channel_orderID, OrderDate, days_delayed]
            # row_to_append_list = list(zip(channel_orderID,OrderDate,days_delayed))
            # row_to_append = [list(ele) for ele in row_to_append_list]
            # delayed_orders_sheet.insert_rows(row=len(delayed_orders_sheet.get_all_values())+1, values=row_to_append)
            wksOrderDelays.insert_rows(row=lastRow, values=row_to_append)


        wksMasterShopifySheet.update_value(addr=cell_order_delayed , val=days_delayed)
        

    # order_to_check_delay = MasterSheetDF_Filtered['Order No'].tolist()

    MasterSheetDF_Filtered = MasterSheetDF.loc[MasterSheetDF['Order Status'] == '']    

    for idx in MasterSheetDF_Filtered.index:

        cell_order_status = 'X' + str(idx+2)
        cell_order_delayed = 'Y' + str(idx+2)
        # MasterSheetDF_Filtered['Order Status'][idx]
        channel_orderID = MasterSheetDF_Filtered['Order No'][idx]
        OrderDate = MasterSheetDF_Filtered['ORDER DATE'][idx]
        order_date = datetime.datetime.strptime(OrderDate, '%Y-%m-%d').date()
        days_delayed = (current_date - order_date).days
        days_delayed = str(days_delayed)

        order_status = runner_function(channel_orderID)

        wksMasterShopifySheet.update_value(addr=cell_order_status , val=order_status)
        wksMasterShopifySheet.update_value(addr=cell_order_delayed , val=days_delayed)



# def find_delayed_days1(channel_orderID_column, OrderDate_column, status_column):
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds = ServiceAccountCredentials.from_json_keyfile_name('google-creds.json', scope)
#     client = gspread.authorize(creds)
#     sheet = client.open('Sheet Name').sheet1  
#     current_date = datetime.date.today()
#     num_rows = sheet.row_count
    
#     for i in range(2, num_rows+1):
#         status = sheet.cell(i, status_column).value
#         if status == 'New':
#             channel_orderID = sheet.cell(i, channel_orderID_column).value
#             OrderDate = sheet.cell(i, OrderDate_column).value
#             order_date = datetime.datetime.strptime(OrderDate, '%Y-%m-%d').date()
#             days_delayed = (current_date - order_date).days
            
#             if days_delayed > 5:
#                 print(f"Item {channel_orderID} is dealyed by more than 5 days")