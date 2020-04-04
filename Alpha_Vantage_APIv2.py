#pip install requests
import requests 
import json
import pandas as pd
import matplotlib.pyplot as plt


#Set API webpage URL
API_URL = "https://www.alphavantage.co/query"


#------------------TIME SERIES DAILY---------------------------------------------#
#define API key
API_Key = "ORJAFG25JUSOOEAI"
parameters = {
   "apikey" : API_Key,
   "function" : "TIME_SERIES_DAILY",
   "symbol" : "MSFT"}

#request URL - response code shows success or not. 
api_data = requests.get(API_URL, params=parameters)

#test successful connection
print(api_data.status_code)

# function to convert json to usable text 
def jprint(obj):
	text = json.dumps(obj, sort_keys=True, indent=4)
	print (text)

# program to rum- all data
#jprint(api_data.json())

#Ticker name
jprint(api_data.json()["Meta Data"]["2. Symbol"])
ticker = json.dumps(api_data.json()["Meta Data"]["2. Symbol"],
                    sort_keys=True, indent=4).replace('"','')

#Daily values 
#jprint(api_data.json()["Time Series (Daily)"])

new_dict= {}
date_list = []
open_list = []
high_list = []
low_list = []
close_list = []
volume_list = []

daily_values = api_data.json()["Time Series (Daily)"]
for date, values in daily_values.items():
    date_dict, date_values = date, values
    new_dict[date_dict] = date_values
    #print(new_dict) - used to check dictionary
    
for key in new_dict.keys():
    #dates list
    k = str(key)
    date_list.append(k)
    #open list
    o = new_dict[k]["1. open"]
    open_list.append(o)
    #high list
    h = new_dict[k]["2. high"]
    high_list.append(h)
    # low list
    l = new_dict[k]["3. low"]
    low_list.append(l)
    #close list
    c = new_dict[k]["4. close"]
    close_list.append(c)
    #volume list 
    v = new_dict[k]["5. volume"]
    volume_list.append(v)

dailyStock_Table = pd.DataFrame(
    {"date":date_list, "open":open_list, "close": close_list,
    "high": high_list, "low": low_list, "volume":volume_list}
    ) 

dailyStock_Table.to_excel((ticker+"DailyPricing.xlsx"))


#---------------------FOREX CSV VERSION-----------------------------------------#

#define API key
API_Key = "ORJAFG25JUSOOEAI"
parameters = {
   "apikey" : API_Key,
   "function" : "FX_DAILY",
   "from_symbol" : "GBP",
   "to_symbol" : "USD",
   "datatype": "csv"}

#request URL - response code shows success or not. 
fx_data = requests.get(API_URL, params=parameters).text

#test successful connection
print(fx_data)

filename = "FXdata.csv"
f = open(filename , "w")  

f.write(fx_data)
f.close()

