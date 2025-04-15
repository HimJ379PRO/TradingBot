# Import libraries and modules
import requests
import json
from config import API_KEY, SECRET_KEY

# Connect to SmartAPI


# Get RELIANCE - OHLC - D - 2020 to NOW()


url = "https://apiconnect.angelone.in/rest/secure/angelbroking/historical/v1/getCandleData"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "X-PrivateKey": "YOUR_API_KEY",
    "X-ClientLocalIP": "192.168.1.2",
    "X-ClientPublicIP": "123.45.67.89",
    "X-MACAddress": "AA:BB:CC:DD:EE:FF",
    "X-UserType": "USER",
    "X-SourceID": "WEB",
    "Content-Type": "application/json"
}
payload = {
    "exchange": "NSE",
    "symboltoken": "3045",
    "interval": "ONE_MINUTE",
    "fromdate": "2021-02-08 09:00",
    "todate": "2021-02-08 09:16"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json())