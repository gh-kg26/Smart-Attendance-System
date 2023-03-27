import json
import csv
from google.oauth2 import service_account
import pygsheets
list_skus_1 = []
list_skus_2 = []
list_skus_3 = []
list_skus_4 = []
size1_list = ['S' , 'M' , 'L' , 'XL' , 'XXL']
size2_list = ['S' , 'M' , 'L' , 'XL' , 'XXL']

for size1 in size1_list:
    for size2 in size2_list:
        # str1 = 'Celeb-NidhiKumar-FanBox01-JG/{0}-SB/{1}'.format(size1 , size2)
        # list_skus_1.append(str1)

        # str2 = 'Celeb-NidhiKumar-FanBox02-JG/{0}-CT/{1}'.format(size1 , size2)
        # list_skus_2.append(str2)

        # str3 = 'Celeb-NidhiKumar-FanBox03-JG/{0}-CT/{1}'.format(size1 , size2)
        # list_skus_3.append(str3)

        # str4 = 'Celeb-NidhiKumar-FanBox04-JG/{0}-HD/{1}'.format(size1 , size2)
        # list_skus_4.append(str4)
        str1 = 'Celeb-NidhiKumar-Combo01-JG/{0}-SB/{1}'.format(size1 , size2)
        list_skus_1.append(str1)

        str2 = 'Celeb-NidhiKumar-Combo02-JG/{0}-CT/{1}'.format(size1 , size2)
        list_skus_2.append(str2)

        str3 = 'Celeb-NidhiKumar-Combo03-JG/{0}-CT/{1}'.format(size1 , size2)
        list_skus_3.append(str3)

        str4 = 'Celeb-NidhiKumar-Combo04-JG/{0}-HD/{1}'.format(size1 , size2)
        list_skus_4.append(str4)

with open('service_account.json') as source:
    info = json.load(source )
credentials = service_account.Credentials.from_service_account_info(info)
client = pygsheets.authorize(service_account_file='service_account.json')

scratch_pad_sheet = client.open('Scratch Pad Sheet')
nkd_fanbox = scratch_pad_sheet.worksheet_by_title('NKD Sets')

nkd_fanbox_df = nkd_fanbox.get_as_df()

lastRow = nkd_fanbox_df.shape[0]
lastRow = lastRow + 1

COIS = list(zip(list_skus_1, list_skus_2 , list_skus_3, list_skus_4))
final = [list(ele) for ele in COIS]

nkd_fanbox.insert_rows(lastRow, values=final)