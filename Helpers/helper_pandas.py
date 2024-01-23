import pandas as pd

#Import helper functions
import helper_functions as help_functions

#For time of execution takes
import time
from datetime import datetime, timedelta

#Convert different types:
def converttoserialiableint(val):
	value_serializable = int(val) if pd.notna(val) else None
	return value_serializable

#Reading pandas data from xls
def getscreenerdatafromexcel(location):
	# Read the Excel file
	df = pd.read_excel(location, skiprows=1,header=0)
	df = df.rename(columns={'Symbol': 'symbol'})
	chartink_stock_names = df.sort_values(by='symbol')['symbol']

	# print(chartink_stock_names)
	return chartink_stock_names.values

#Converting json to pandas, to change later to xls
def converjsontopandas(jsondata):
	dfs = []
	for stockname in jsondata:
		print("Converting to pandas ",stockname)
		for date in jsondata[stockname]:
			# print("date: ",date)
			df = pd.DataFrame.from_dict(jsondata[stockname][date], orient='index').T
			df['stockname'] = stockname
			# Convert the 'date' column to datetime
			df['date'] = pd.to_datetime(df['date'])
			dfs.append(df)
	return dfs


#Saving pandas into xls for faster read
def savetoxls(merged_df,filename):
	# Record the start time
	start_time = time.time()

	# Assuming your DataFrame is named 'df'
	print("Saving the pandas DataFrame to ",filename)
	merged_df.to_excel(filename, index=True)
	print("Saved..")

	# Record the end time
	end_time = time.time()
	help_functions.showelapsedtime(start_time,end_time,"saving pandas")

#Pandas conversion
def pandasconversion(total_data):
	#Convert to pandas
	# Record the start time
	start_time = time.time()

	# Convert JSON data to DataFrame
	dfs=converjsontopandas(total_data)

	# Record the end time
	end_time = time.time()
	help_functions.showelapsedtime(start_time,end_time,"pandas conversion")


	# Record the start time
	start_time = time.time()
	print("Merging....")
	merged_df = pd.concat(dfs)
	print(merged_df)

	# Record the end time
	end_time = time.time()
	help_functions.showelapsedtime(start_time,end_time,"merging")
	

	return merged_df

def adding_newrows_pandas(df,pandas_date):
	new_rows = []
	for stockname, group in df.groupby('stockname'):
	    new_row = group.tail(1).copy()
	    new_row['date'] = pandas_date # Set the date to today's date
	    new_rows.append(new_row)

	# Append the new rows to the DataFrame
	df = pd.concat([df] + new_rows, ignore_index=True)
	return df

def getpandasdate(prev,today = datetime.now()):

	today=today-timedelta(days=prev)
	# Get today's date
	pandas_date = pd.Timestamp(today.date())
	print("Current Day :",today)
	return pandas_date


def checkmissingdate(df):

	# # # Assuming your DataFrame is named 'df'
	unique_stocknames = df['stockname'].unique()

	print("Number of stocks is: ",len(unique_stocknames))

	checkflag=False
	print("\nChecking for data missing....might take some time....")

	
	# print(df)

	return df,checkflag

#Updating the Live data from firebase and updating to Pandas
def updatelivedatainpandas(df,livedata):
	print("Updating the live data.....might take some time.....")
	# print(df)
	unique_stocknames = df['stockname'].unique()

	missingdata={}
	for stockname in unique_stocknames:
		# Before updation the LTP
		# print("Checking ",stockname)######## For not printing
		stockdata=df.loc[df['stockname']==stockname]
		# stockdata = df.loc[(df['stockname'] == stockname) & (df['date'] == pd.to_datetime('today').date())]
		latestdata=stockdata.tail(1)

		if stockname not in livedata:
			print("There is live data missing for ",stockname)############ For not printing
			missingdata[stockname]={}
			missingdata[stockname]=100
		else:
			#Update everything
			idx = latestdata.index[-1] 
			print(df.loc[idx, 'date']," Updating LTP of ",stockname,": ",livedata[stockname]['ltp'])######## For not printing

			# print(idx)

			df.loc[idx, 'close'] = livedata[stockname]['ltp']

			df.loc[idx, 'open'] = livedata[stockname]['o']
			df.loc[idx, 'high'] = livedata[stockname]['h']
			df.loc[idx, 'low'] = livedata[stockname]['l']
			# df.loc[latestdata.index[0], 'pclose'] = livedata[stockname]['pclose']
			df.loc[idx, 'vol'] = livedata[stockname]['v']

		#After updating the LTP
		latestdata=stockdata.tail(1)

		# For debug, only use 1 iteration
		# break

		# print(latestdata)
		# Print latest 3 data
		# savetoxls(df.loc[df['stockname']==stockname],"Data/pandas_"+stockname+".xlsx")
		# break

		# print("-----------------")
	print("Update Sucessfully!!!")
	return df,missingdata


#Updating the Live data from firebase and updating to Pandas
def updatelivedatainpandas2(df,livedata,date):
	# print("Updating the live data.....might take some time.....")
	# print(df)
	unique_stocknames_in_df = df['stockname'].unique()
	unique_stocknames_in_livedata=list(livedata.keys())

	# print(unique_stocknames_in_df)
	# print(unique_stocknames_in_livedata)

	if set(unique_stocknames_in_df) != set(unique_stocknames_in_df):
		print("Both lists have different stocknames.")
		return df,{"missingltp"}

	# Convert ohcl_data to DataFrame
	ohcl_df = pd.DataFrame(livedata).T.reset_index()
	ohcl_df.columns = ['stockname', 'high', 'low', 'close', 'open', 'pc', 'vol']



	today_df = df[df['date'] == date]
	print(today_df)
	# Merge or replace the old data with the new OHCL data
	today_df = pd.merge(today_df, ohcl_df, on='stockname', how='left', suffixes=('_old', ''))
	# print(today_df)
	today_df['open'] = today_df['open'].combine_first(today_df['open_old'])
	today_df['high'] = today_df['high'].combine_first(today_df['high_old'])
	today_df['low'] = today_df['low'].combine_first(today_df['low_old'])
	today_df['close'] = today_df['close'].combine_first(today_df['close_old'])
	today_df['vol'] = today_df['vol'].combine_first(today_df['vol_old'])
	today_df.drop(columns=['high_old', 'low_old', 'close_old', 'open_old', 'vol_old'], inplace=True)


	# Extract the indices of the rows to be updated
	indices_to_update = df.index[df['date'] == date]
	# print(df['date'])
	print("Checking date ",date)

	# Update rows in df where date matches
	df.loc[indices_to_update, :] = today_df[df.columns].values


	# print(df[df['date'] == date])
	print("Update the pandas Sucessfully!!!")
	return df,None

