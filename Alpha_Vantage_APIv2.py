#pip install requests
import requests 
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


#Set API webpage URL
API_URL = "https://www.alphavantage.co/query"

Stockcode = input("Please enter a ticker: " )

#------------------TIME SERIES DAILY---------------------------------------------#
#define API key
API_Key = "ORJAFG25JUSOOEAI"
parameters = {
   "apikey" : API_Key,
   "function" : "TIME_SERIES_DAILY",
   "symbol" : Stockcode}

#request URL - response code shows success or not. 
api_data = requests.get(API_URL, params=parameters)

#test successful connection
print(api_data.status_code)

# function to convert json to usable text 
def jprint(obj):
	text = json.dumps(obj, sort_keys=True, indent=4)
	print (text)


def bytespdate2num(fmt, encoding='utf-8'):
    def bytesconverter(b):
        s = b.decode(encoding)
        return (mdates.datestr2num(s))
    return bytesconverter

# program to rum- all data
#jprint(api_data.json())
#Daily values 
#jprint(api_data.json()["Time Series (Daily)"])

#Ticker name
jprint(api_data.json()["Meta Data"]["2. Symbol"])
ticker = json.dumps(api_data.json()["Meta Data"]["2. Symbol"],
                    sort_keys=True, indent=4).replace('"','')


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
#convert date text to time, numbers to numbers 
dailyStock_Table['date'] = dailyStock_Table['date'].astype('datetime64[ns]')

#convert objects floats
dailyStock_Table['high'] = [float(line) for line in dailyStock_Table['high']]
dailyStock_Table['low'] = [float(line) for line in dailyStock_Table['low']]
dailyStock_Table['volume'] = [float(line) for line in dailyStock_Table['volume']]

print(dailyStock_Table.dtypes)

#save PD as excel 
dailyStock_Table.to_excel((ticker+"DailyPricing.xlsx"))


fig, axs = plt.subplots(3,1)

ax1 = plt.subplot2grid((3,1), (0,0), rowspan=2)


x1 = dailyStock_Table['date']
y1 = dailyStock_Table['high']

x2 = dailyStock_Table['date']
y2 = dailyStock_Table['low']

x3 = dailyStock_Table['date']
y3 = dailyStock_Table['volume']

ax1.plot(x1, y1, label = 'High', color='g')
ax1.plot(x2, y2, label = 'Low', color='r')
# plt.locator_params(axis='y', nbins='10')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.title(Stockcode + ' Daily Pricing')

ax2 = plt.subplot2grid((3,1), (2,0), rowspan=1)
ax2.plot(x3, y3, label = 'Volume', color='b')
plt.xlabel('Date')
ax2.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.draw()
plt.ylabel('Volume')
plt.title(Stockcode + ' Daily Volume')
plt.legend()

plt.subplots_adjust(left=0.09, bottom=0.10, right=0.94, top=0.93, wspace=0.2, hspace=0.95)
plt.show()


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
print(requests.get(API_URL, params=parameters).status_code)

filename = "FXdata.csv"
f = open(filename , "w")  

f.write(fx_data)
f.close()
