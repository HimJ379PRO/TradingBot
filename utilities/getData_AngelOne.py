# Import libraries and modules
import requests
import json
from config import API_KEY, SECRET_KEY

# Connect to SmartAPI
obj = SmartConnect(api_key = API_KEY)

#login api call
data = obj.generateSession("Your Client ID","Your Password","Your totp")

# Get RELIANCE - OHLC - D - 2020 to NOW()
url = "https://apiconnect.angelone.in/rest/secure/angelbroking/historical/v1/getCandleData"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "X-PrivateKey": "API_KEY",
    "X-ClientLocalIP": "192.168.1.2",
    "X-ClientPublicIP": "123.45.67.89",
    "X-MACAddress": "AA:BB:CC:DD:EE:FF",
    "X-UserType": "USER",
    "X-SourceID": "WEB",
    "Content-Type": "application/json"
}
payload = {
    "exchange": "NSE",
    "symboltoken": "2885",
    "interval": "ONE_DAY",
    "fromdate": "2025-04-01 09:00",
    "todate": "2025-04-11 22:00"
}

'''
NOTE:
In Get Candle Data Request fromdate and todate format should be "yyyy-MM-dd hh:mm"
The response is an array of records, where each record in turn is an array of the following values — [timestamp, open, high, low, close, volume].
'''

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json())