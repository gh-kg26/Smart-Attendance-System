import requests
import json


def generateSRToken():
    url = "https://apiv2.shiprocket.in/v1/external/auth/login"

    payload = json.dumps({
    "email": "nandurimail99@gmail.com",
    "password": "shipm123"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    bearer_token = response.text

    return bearer_token
# print(response.text)

def generateSRStatusList(channel_order_id, bearer_token):
    #channel_order_id = ["#1840" , "#1839" , "#1730" , "#1669" , "#1482-C" , '']
    #channel_order_id = ['1498', '1497', '1495', '1494', '1492', '1485', '1484', '1482-C', '1482-C', '1482-C', '1483', '1481', '1479', '1478', '1476', '1474', '1474', '1469', '1466', '1463', '1463', '1463', '1463', '1457', '1455', '1456', '1454', '1453', '1451', '1451', '1451', '1449', '1449', '1447', '1443', '1442', '1441', '1431', '1431', '1428', '1421', '1420', '1420', '1419', '1415', '1414', '1411', '1410', '1403', '1395', '1388', '1389', '1384', '1380', '1372', '1373', '1374', '1376', '1368', '1368', '1367', '1360', '1355', '1350', '1348', '1347', '1346', '1345', '1345', '1343', '1341', '1340', '1337', '1328', '1322', '1316', '1303', '1283', '1283', '1268', '1269', '1265', '1263', '1258', '1257', '1253', '1255', '1255', '1252', '1250', '1251', '1249', '1248', '1245', '1241', '1244', '1239', '1239', '1239', '1239', '1240', '1237', '1238', '1233', '1234', '1235', '1232', '1230', '1228', '1224', '1224', '1224', '1225', '1225', '1226', '1226', '1227', '1218', '1219', '1220', '1220', '1221', '1221', '1221', '1222', '1223', '1217', '1215', '1500', '1507', '1512', '1511', '1524', '1523', '1522', '1521', '1519', '1520', '1518', '1514', '1515', '1516', '1517', '1538', '1540', '1535', '1525', '1526', '1527', '1528', '1529', '1530', '1546', '1545', '1543', '1551', '1547', '1548', '1550', '1596', '1594', '1593', '1592', '1590', '1588', '1496', '1598', '1597', '1624', '1618', '1628', '1645', '1662', '1651', '1666', '1686', '1680', '', '', '', '', '', '1705', '1704', '1702', '1701', '1700', '1707', '1715', '1718', '1726', '', '', '']
    # channel_order_id = ['#2540']

    channel_order_id = [i[1:] for i in channel_order_id]

    print(channel_order_id)

    Shipping_Status = []

    for i in range(0 , len(channel_order_id)):

        url = "https://apiv2.shiprocket.in/v1/external/orders?search={0}".format(channel_order_id[i])

        payload={
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(bearer_token),
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        json_object = json.loads(response.text)
        with open('data.json' , 'w') as outfile:
            json.dump(json_object , outfile)
        try:
            Shipping_Status.append(json_object["data"][0]["status"])
        except:
            Shipping_Status.append(" ")
            print(channel_order_id[i] , " Error")

    #print(Shipping_Status)
    return Shipping_Status

def return_shipping_status(channel_order_id, bearer_token):
    channel_order_id = channel_order_id[1:]
    url = "https://apiv2.shiprocket.in/v1/external/orders?search={0}".format(channel_order_id)
    payload={
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(bearer_token),
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)

    try:
        shipping_status = json_object["data"][0]["status"]
    except:
        shipping_status = " "
        print(channel_order_id, " Error")

    return shipping_status


def runner_function_list(channel_order_id):
    bearer_token_string = generateSRToken()
    bearer_token = json.loads(bearer_token_string)
    # print(bearer_token ,  type(bearer_token) , bearer_token['token'])

    # channel_order_id = ['#2540']
    Shipping_Status = generateSRStatusList(channel_order_id, bearer_token['token'])
    # print(Shipping_Status)

    return Shipping_Status

# a = runner_function(["#2397" , "#2398" , "#2521"])
# print(a)

def runner_function(channel_order_id):
    bearer_token_string = generateSRToken()
    bearer_token = json.loads(bearer_token_string)
    # print(bearer_token ,  type(bearer_token) , bearer_token['token'])

    # channel_order_id = ['#2540']
    Shipping_Status = return_shipping_status(channel_order_id, bearer_token['token'])
    # print(Shipping_Status)

    return Shipping_Status