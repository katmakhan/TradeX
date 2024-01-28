#For invoking http requests
import requests

#Json Parsing
import json

import base64


from datetime import datetime
from datetime import timedelta

#Convert date object to date string
def convert_to_date_obj(date_str,date_format):
	date_obj = datetime. strptime(date_str,date_format)
	return date_obj

#Convert date string into date object
def convert_to_date_str(date_obj,date_format):
	date_str=date_obj.strftime(date_format)
	return date_str

def gap_analysis():

	# Headers for content Type 
	headers = {"Content-Type":"application/json"}

	curr_day=datetime.today() - timedelta(days=0)
	curr_day_str=convert_to_date_str(curr_day,"%Y-%m-%d")

	data={}
	data['Date']=curr_day_str
	data=json.dumps(data)
	# print(data)

	#Then visit the json page for fetching the json
	actualurl='https://webapi.niftytrader.in/webapi/Resource/gap-analysis'
	res = requests.post(actualurl, data=data,headers=headers)
	# print(res.json())

	if(res.json().get('resultData') is None):
		print("No result fetched")
		return

	#Print gap-up stocks
	gap_up_stocks=res.json()['resultData']["gap_up_stocks"]
	gap_down_stocks=res.json()['resultData']["gap_down_stocks"]

	return gap_up_stocks,gap_down_stocks

def stock_industry_data(symbol):

	# Headers for content Type 
	headers = {"Content-Type":"application/json"}


	data={}
	data['symbol']=symbol
	data=json.dumps(data)
	# print(data)

	#Then visit the json page for fetching the json
	actualurl='https://webapi.niftytrader.in/webapi/Analysis/stock-industry-data'
	# https://webapi.niftytrader.in/webapi/Analysis/stock-financial-data
	
	res = requests.post(actualurl, data=data,headers=headers)
	# print(res.json())
	return res.json()

def getchart_data(symbol):

	# Headers for content Type 
	headers = {"Content-Type":"application/json"}

	#Then visit the json page for fetching the json
	actualurl='https://webapi.niftytrader.in/webapi/Symbol/symbol-ltp-chart?symbol='+symbol
	# https://webapi.niftytrader.in/webapi/Analysis/stock-financial-data
	
	res = requests.get(actualurl,headers=headers)
	# print(res.json())

	if(res.json().get('resultData') is None):
		print("No result fetched")
		return

	chartdata=res.json()['resultData'][0]['chart_data']
	# print(chartdata)
	return chartdata
	
def get_optionchain(symbol):
	# Headers for content Type 
	headers = {"Content-Type":"application/json"}

	#Then visit the json page for fetching the json
	actualurl=f'https://webapi.niftytrader.in/webapi/option/fatch-option-chain?symbol={symbol}&expiryDate='
	# https://webapi.niftytrader.in/webapi/Analysis/stock-financial-data
	
	res = requests.get(actualurl,headers=headers)
	# print(res.json())

	opdata=res.json()['resultData']['opDatas']
	expirydates=res.json()['resultData']['opExpiryDates']
	# print(opdata)
	return opdata,expirydates


def total_stock_details():
	url="https://webapi.niftytrader.in/webapi/symbol/psymbol-list"
	res = requests.get(url)
	# print(res.json())
	return res.json()['resultData']

def nifty_stock_details():
	uid=2110
	username = f"niftyapiuser:niftyapiuser@{uid}#"
	encoded_credentials = base64.b64encode(username.encode("utf-8")).decode("utf-8")
	print(encoded_credentials)
	headers = {"Content-Type":"application/json",
				# "Authorization":"Basic bmlmdHlhcGl1c2VyOm5pZnR5YXBpdXNlckAyMTEwIw==",
				"Authorization":"Basic "+encoded_credentials,
				}
	url='https://services.niftytrader.in/webapi/symbol/nifty50-data'
	res = requests.get(url,headers=headers,timeout=2)
	# print(res.json())
	return res.json()['result']

# nifty_stock_details()

# def main():
# 	gap_up_stocks,gap_down_stocks=gap_analysis()

# 	for stocks in gap_up_stocks:
# 		print(stocks['symbol_name'])
	
# #Main program
# if __name__ == '__main__':
# 	main()