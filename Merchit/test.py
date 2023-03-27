# str = 'Celeb-NidhiKumar-FanBox04-JG/M-HD/M'
# if 'FanBox' in str:
#     print("CONTAINS")
# lista = str.split('-')
# designcode1 = lista[0:3]
# designcode = []
# designcode.append(designcode1)

# print(type(designcode) , designcode , len(designcode))

# for i in range(0 , len(designcode)):
#     designcode[i] = '-'.join(designcode[i])

# print(designcode)


    

# print(lista , lista[0:3])
# print(lista[3:])
# percentage_split = '80'
# percentage_split_f = int(percentage_split)/100
# print(percentage_split_f)

# CreatorOrdersDF_Profit = ['75.61',' 230.91',' 220.74',' 116.96',' 360.61',' 56.85',' 157.47',' 23.23',' 382.89',' 209.42',' 204.74',' 320.11',' 197.47',' 618.33',' 255.93',' 90.54',' 204.74',' 90.54',' 320.11',' 209.42',' 220.74',' 364.06',' 376.23',' 255.93',' 255.93',' 281.04',' 291.65',' 56.85',' 291.65',' 281.04',' 189.92',' 192.18',' 116.96',' 23.23',' 157.47',' 23.23',' 178.48',' 197.47',' 197.47',' 204.74',' 209.42',' 458.34',' 75.61',' 263.18',' 90.54',' 255.93',' 618.33',' 197.47',' 90.54',' 230.91',' 204.74',' 230.91',' 178.32',' 90.54',' 209.42',' 204.74',' 218.48',' 320.11',' 204.74',' 56.85',' 382.89',' 90.54',' 360.23',' 455.36',' 195.01',' 263.09',' 145.53',' 331.66',' 189.92',' 90.54',' 23.23',' 123.61',' 455.36',' 330.47',' 251.65',' 204.74',' 204.74',' 204.74',' 330.47',' 220.74',' 255.93',' 90.54',' 255.93',' 178.48',' 178.48',' 56.85',' 204.74',' 230.91',' 204.74',' 220.74',' 251.65',' 23.23',' 116.96',' 197.47',' 271.93',' 56.85',' 145.53',' 204.74',' 230.91',' 230.91',' 75.61',' 195.01',' 246.91',' 255.93',' 255.93',' 291.65',' 225.04',' 255.93',' 232.63',' 246.91',' 230.91',' 197.47',' 291.65',' 455.36','271.93',' 330.47',' 223.09',' 255.93',' 271.93',' 255.93',' 255.93',' 251.65',' 255.93',' 75.61',' 251.65',' 255.93',' 232.63',' 255.93',' 251.65',' 255.93',' 291.65',' 255.93',' 215.03',' 271.93',' 194.5',' 142.43',' 291.65',' 163.85',' 194.5']

# def return_unpaid_creator_profit(CreatorOrdersDF_Profit):
#     CreatorOrdersDF_Profit = [float(i) for i in CreatorOrdersDF_Profit]
#     creator_payable_amount = sum(CreatorOrdersDF_Profit)
#     rounded_creator_payable_amount = "{:.2f}".format(float(creator_payable_amount))

# #     return rounded_creator_payable_amount

# # print(return_unpaid_creator_profit(CreatorOrdersDF_Profit))
# import datetime

# a = "2022-09-23T15:26:29+05:30"
# # order_date = datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ").date()

# # print(order_date , type(order_date))
# current_date = datetime.date.today()
# print(current_date)

# sep = 'T'
# b = a.split(sep, 1)[0]
# order_date = datetime.datetime.strptime(b, "%Y-%m-%d").date()
# print(order_date , type(order_date))

channel_orderID = "1"
OrderDate = "2"
days_delayed = "3"
row_to_append = [channel_orderID, OrderDate, days_delayed]

print(row_to_append)