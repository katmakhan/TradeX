
#For invoking http requests
import requests
import pandas as pd
import io

def fetch_allstocknames():
	url="https://public.fyers.in/sym_details/NSE_CM.csv"
	# Fetch the content of the CSV file
	response = requests.get(url)
	data = response.content

	# Read the CSV content using pandas
	df = pd.read_csv(io.StringIO(data.decode('utf-8')), header=None)
	df = df.sort_values(by=9)
	# Iterate through each row
	total_symbols=[]
	total_symbols_updated=[]
	for index, row in df.iterrows():
		# Access each column value using row[column_name]
		# For example, print the values in the 1st, 2nd, and 3rd columns
		symbol=row[9]
		if ("-BZ" in symbol or "-EQ" in symbol or "-BE" in symbol) and "ETF" not in symbol:
			print(symbol)
			total_symbols.append(symbol)
			# NSE:MCDOWEL-N-EQ
			total_symbols_updated.append(symbol.split("-")[0].split(":")[1])

	print("\n")
	print("Total Symbols: ",len(total_symbols))
	return total_symbols_updated
