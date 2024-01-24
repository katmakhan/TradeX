# Import Modules
from Modules.NSE.NSE_Holidays import get_json_user_agent_Holidays as nse_holiday
from Modules.NSE.NSE_FNO import get_json_cookie_bypass_FNO as nse_fno
from Modules.NSE.NSE_Market_Data import get_json_cookie_bypass_NSEMarketData as nse_market
from Helpers import helper_functions_adv as help_function_adv
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go

# from google.oauth2.credentials import Credentials

# not working with google-auth-oauthlib==0.8.0
# pip install google-auth-oauthlib==0.4.6


# Authenticators
import streamlit_authenticator as stauth
import yaml
import traceback
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
import json

# import SafeLoader
def save_data_as_json(data,which):
	# Convert data to JSON string
	json_data = json.dumps(data, indent=2)

	# Create an in-memory representation of the file
	bytes_data = BytesIO(json_data.encode())

	# Provide the download button
	st.sidebar.download_button(
		label="Download JSON",
		data=bytes_data,
		file_name=f"{which}_option_chain_data.json",
		# key="which",
	)
	# st.success("Option chain data download initiated.")

# Running streamlit
st.set_page_config(page_title="TradeX", page_icon="🔰", 
layout="wide")


#----- CREATE HASHED PASSWORD----
# hashed_passwords = stauth.Hasher(['xxx', 'xxxx']).generate()
# print(hashed_passwords)

#----- LOGIN ------
# with open('./config.yaml') as file:
#   config = yaml.load(file, Loader=yaml.SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# #------ Login Page------
# name, authentication_status, username = authenticator.login('Login', 
# 'main')

authentication_status= True

#Checking Status
if authentication_status:
	#Main Page
	# https://www.webfx.com/tools/emoji-cheat-sheet/

	st.title("NSE Data")
	# st.markdown("##")


	# ---- SIDEBAR ----
	#Logout Button
	# authenticator.logout("Logout","sidebar")
	# Welcome Name
	# name="User"
	# st.sidebar.title(f"Welcome {name}")
	# st.sidebar.header("Dashboard")
	# st.header("Nifty Options")
	# res=nse_fno.underlying_info()
	# st.dataframe(res)

	tab1, tab2, tab3, tab4 = st.tabs(["Nifty", "BankNifty", "Stocks","Holidays"])

	
	with tab1:
		try:
			option_chain_data=nse_fno.index_optionchain('NIFTY')
			try:
				res=nse_market.marketstatus()
				res_chart=nse_market.marketChart_indices("NIFTY%2050")
				market_status = res["marketState"][0]["marketStatus"]
				index = res["marketState"][0]["index"]
				last_price = res["marketState"][0]["last"]
				variation = res["marketState"][0]["variation"]
				formatted_variation = "{:.2f}".format(variation)
				percent_change = res["marketState"][0]["percentChange"]
				result_string = f"{index}: {last_price} ({percent_change}%)  {formatted_variation}"

				if variation>0:
					st.success(result_string)
				if variation<0:
					st.warning(result_string)

				# Extracting timestamp and values from the data
				timestamps, values = zip(*res_chart['grapthData'])

				# Convert timestamps to date format
				dates = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in timestamps]

				# Filter out data points after 3:30 pm (15:30)
				filtered_data = [(ts, val, date) for ts, val, date in zip(timestamps, values, dates) if date.time() <= datetime.strptime('15:30:00', '%H:%M:%S').time()]

				# Extract filtered timestamps and values
				filtered_timestamps, filtered_values, filtered_dates = zip(*filtered_data)

				# Create a Plotly line chart
				fig = go.Figure(data=go.Scatter(x=filtered_dates, y=filtered_values, mode='lines'))


				# Customize the layout
				fig.update_layout(
					title="NIFTY 50",
					xaxis_title='Time',
					yaxis_title='LTP',
				)

				# Display the Plotly chart
				st.plotly_chart(fig)

			except Exception as e:
				st.warning("Something went wrong while fetching LTP")
				print(traceback.print_exc())

			# st.dataframe(option_chain_data)
			st.sidebar.subheader("NIFTY Options Data")
			st.sidebar.write(option_chain_data)
			save_data_as_json(option_chain_data,"nifty")

			# df_rows = []
			# for option in res:
			#   strike_price = option["strikePrice"]
			#   expiry_date = option["expiryDate"]
			#   pe_data = option.get("PE", {})
			#   ce_data = option.get("CE", {})
			#   df_rows.append({
			#       "Strike Price": strike_price,
			#       "Expiry Date": expiry_date,
			#       "PE Bid Price": pe_data.get("bidprice", 0),
			#       "PE Ask Price": pe_data.get("askPrice", 0),
			#       "CE Bid Price": ce_data.get("bidprice", 0),
			#       "CE Ask Price": ce_data.get("askPrice", 0),
			#   })

			# option_chain_df = pd.DataFrame(df_rows)

			# # Display the option chain data in a table
			# st.table(option_chain_df)

			today = datetime.today().date()

			# Find the nearest and next nearest expiration dates from today
			expiry_dates = list(set(datetime.strptime(option["expiryDate"], "%d-%b-%Y").date() for option in option_chain_data))
			expiry_dates.sort()
			# print(expiry_dates)

			nearest_expiry = min(filter(lambda date: date >= today, expiry_dates))
			expiry_dates.remove(nearest_expiry)
			next_nearest_expiry = min(filter(lambda date: date >= today, expiry_dates))


			for expiry_date in [nearest_expiry, next_nearest_expiry]:
				st.subheader(f"Expiry Date: {expiry_date.strftime('%d-%b-%Y')}")

				# Create a DataFrame for the specific expiry date
				df_rows = []
				for option in option_chain_data:
					if datetime.strptime(option["expiryDate"], "%d-%b-%Y").date() == expiry_date:
						strike_price = option["strikePrice"]
						pe_data = option.get("PE", {})
						ce_data = option.get("CE", {})
						df_rows.append({
							"CE Bid Price": ce_data.get("bidprice", 0),
							"CE Ask Price": ce_data.get("askPrice", 0),
							"CE OI": ce_data.get("openInterest", 0),
							"CE LTP": round(ce_data.get("lastPrice", 0), 2),
							"Strike Price": "NIFTY "+str(strike_price),
							"PE LTP": round(pe_data.get("lastPrice", 0), 2),
							"PE OI": pe_data.get("openInterest", 0),
							"PE Bid Price": pe_data.get("bidprice", 0),
							"PE Ask Price": pe_data.get("askPrice", 0),
						})

				option_chain_df = pd.DataFrame(df_rows)

				# Display the option chain data in a table
				st.dataframe(option_chain_df)

		except:
			st.warning("Something went wrong")
			print(traceback.print_exc())

	with tab2:
		try:
			option_chain_data=nse_fno.index_optionchain('BANKNIFTY')
			try:
				# res=nse_market.marketstatus()
				res_chart=nse_market.marketChart_indices("NIFTY%20BANK")
				
				# market_status = res["marketState"][0]["marketStatus"]
				# index = res["marketState"][0]["index"]
				# last_price = res["marketState"][0]["last"]
				# variation = res["marketState"][0]["variation"]
				# formatted_variation = "{:.2f}".format(variation)
				# percent_change = res["marketState"][0]["percentChange"]
				# result_string = f"{index}: {last_price} ({percent_change}%)  {formatted_variation}"

				# if variation>0:
				# 	st.success(result_string)
				# if variation<0:
				# 	st.warning(result_string)

				# Extracting timestamp and values from the data
				timestamps, values = zip(*res_chart['grapthData'])

				# Convert timestamps to date format
				dates = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in timestamps]

				# Filter out data points after 3:30 pm (15:30)
				filtered_data = [(ts, val, date) for ts, val, date in zip(timestamps, values, dates) if date.time() <= datetime.strptime('15:30:00', '%H:%M:%S').time()]

				# Extract filtered timestamps and values
				filtered_timestamps, filtered_values, filtered_dates = zip(*filtered_data)

				# Create a Plotly line chart
				fig = go.Figure(data=go.Scatter(x=filtered_dates, y=filtered_values, mode='lines'))


				# Customize the layout
				fig.update_layout(
					title="Bank Nifty",
					xaxis_title='Time',
					yaxis_title='LTP',
				)

				# Display the Plotly chart
				st.plotly_chart(fig)

			except Exception as e:
				st.warning("Something went wrong while fetching LTP")
				print(traceback.print_exc())

			# st.dataframe(option_chain_data)
			st.sidebar.subheader("BANKNIFTY Options Data")
			st.sidebar.write(option_chain_data)
			save_data_as_json(option_chain_data,"banknifty")

			# df_rows = []
			# for option in res:
			#   strike_price = option["strikePrice"]
			#   expiry_date = option["expiryDate"]
			#   pe_data = option.get("PE", {})
			#   ce_data = option.get("CE", {})
			#   df_rows.append({
			#       "Strike Price": strike_price,
			#       "Expiry Date": expiry_date,
			#       "PE Bid Price": pe_data.get("bidprice", 0),
			#       "PE Ask Price": pe_data.get("askPrice", 0),
			#       "CE Bid Price": ce_data.get("bidprice", 0),
			#       "CE Ask Price": ce_data.get("askPrice", 0),
			#   })

			# option_chain_df = pd.DataFrame(df_rows)

			# # Display the option chain data in a table
			# st.table(option_chain_df)

			today = datetime.today().date()

			# Find the nearest and next nearest expiration dates from today
			expiry_dates = list(set(datetime.strptime(option["expiryDate"], "%d-%b-%Y").date() for option in option_chain_data))
			expiry_dates.sort()
			# print(expiry_dates)

			nearest_expiry = min(filter(lambda date: date >= today, expiry_dates))
			expiry_dates.remove(nearest_expiry)
			next_nearest_expiry = min(filter(lambda date: date >= today, expiry_dates))


			for expiry_date in [nearest_expiry, next_nearest_expiry]:
				st.subheader(f"Expiry Date: {expiry_date.strftime('%d-%b-%Y')}")

				# Create a DataFrame for the specific expiry date
				df_rows = []
				for option in option_chain_data:
					if datetime.strptime(option["expiryDate"], "%d-%b-%Y").date() == expiry_date:
						strike_price = option["strikePrice"]
						pe_data = option.get("PE", {})
						ce_data = option.get("CE", {})
						df_rows.append({
							"CE Bid Price": ce_data.get("bidprice", 0),
							"CE Ask Price": ce_data.get("askPrice", 0),
							"CE OI": ce_data.get("openInterest", 0),
							"CE LTP": round(ce_data.get("lastPrice", 0), 2),
							"Strike Price": "BANKNIFTY "+str(strike_price),
							"PE LTP": round(pe_data.get("lastPrice", 0), 2),
							"PE OI": pe_data.get("openInterest", 0),
							"PE Bid Price": pe_data.get("bidprice", 0),
							"PE Ask Price": pe_data.get("askPrice", 0),
						})

				option_chain_df = pd.DataFrame(df_rows)

				# Display the option chain data in a table
				st.dataframe(option_chain_df)

		except:
			st.warning("Something went wrong")
			print(traceback.print_exc())


	with tab4:
		st.header("Holidays:")
		try:
			res=nse_holiday.fno_holiday_list()
			st.dataframe(res)
		except:
			st.warning("Something went wrong")
			print(traceback.print_exc())

	# st.markdown(res)
	# button_clicked = st.button("Click me!")

	# # Check if the button is clicked
	# if button_clicked:
	#   st.write("Button clicked!")
		
elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')


	
