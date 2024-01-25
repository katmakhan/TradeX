#For invoking http requests
import requests

#Json Parsing
import json


def nifty_topoptions():
	
	actualurl='https://groww.in/v1/api/stocks_fo_data/v1/contracts/nifty/top'
	res = requests.get(actualurl,timeout=2)
	fnolistdata=res.json()
	# print(fnolistdata)
	return fnolistdata

# def main():
# 	nifty_topoptions()
	
# #Main program
# if __name__ == '__main__':
# 	main()
