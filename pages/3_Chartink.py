# Import Modules
from Modules.Chartink import get_chart
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

# import SafeLoader

import pandas as pd


# Running streamlit
st.set_page_config(page_title="TradeX", page_icon="🔰", 
layout="wide")


#----- CREATE HASHED PASSWORD----
# hashed_passwords = stauth.Hasher(['xxx', 'xxxx']).generate()
# print(hashed_passwords)

#----- LOGIN ------
# with open('./config.yaml') as file:
# 	config = yaml.load(file, Loader=yaml.SafeLoader)

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

	st.title("Chartink Data")
	# st.markdown("##")


	# ---- SIDEBAR ----
	#Logout Button
	# authenticator.logout("Logout","sidebar")
	# Welcome Name
	# name="User"
	# st.sidebar.title(f"Welcome {name}")
	# st.sidebar.header("Dashboard")

	try:
		allstock_list=help_function_adv.fetch_allstocknames()

		# st.write(allstock_list)
		
		# allstock_list.append('NIFTY50')
		# st.write("Total Stock List: ",len(allstock_list))
		default_ix=len(allstock_list)-1
		stockname = st.selectbox(
			"Select the Stock",
			options=allstock_list,
			index=default_ix
		)

		all_indicator_list=['SMA','EMA']
		indicatorname = st.selectbox(
			"Select the Indicator",
			options=all_indicator_list,
			index=0
		)
		all_period_list=['20','30','40','50']
		period = st.selectbox(
			"Select the period",
			options=all_period_list,
			index=0
		)

		first_column, second_column = st.columns(2)
		with first_column:
			# st.subheader(f"Chart : {stockname}")

			# 	# Separate fields
			indicatorlabel =f'{indicatorname} {period}'
			indicatorvalue=f'{indicatorname}(  close , {period} )'
			use_live = "1"
			limit = "1"
			size = "200"
			widget_id = "-1"
			end_time = "-1"
			timeframe = "Daily"
			symbol = stockname
			scan_link = "null"
			query = f"select open, high, low, close, volume, {indicatorvalue} as '{indicatorlabel}' where symbol='{symbol}'"

			try:
				res=get_chart.getchart_indicators(indicatorlabel,indicatorvalue,query,use_live,limit,size,widget_id,end_time,timeframe,symbol,scan_link)
				# # Traverse the data
				# groupdata=res['groupData'][0]['results']
				# for data in groupdata:
				# 	# print(data)
				# 	if data.get(emalabel) is not None:
				# 		print(data[emalabel])
				# 	print("---")
				# st.write(res)

				# Extracting the relevant data from JSON
				df = pd.DataFrame(res)
				# print(df)

				dfopen = pd.DataFrame(res['groupData'][0]["results"][0])
				dfhigh = pd.DataFrame(res['groupData'][0]["results"][1])
				dflow = pd.DataFrame(res['groupData'][0]["results"][2])
				dfclose = pd.DataFrame(res['groupData'][0]["results"][3])
				dfvolume = pd.DataFrame(res['groupData'][0]["results"][4])
				dfindicator = pd.DataFrame(res['groupData'][0]["results"][5])
				total_df = pd.concat([dfopen, dfclose, dflow, dfhigh,dfvolume], axis=1)
				total_df.columns = ['Open', 'High', 'Low', 'Close','Volume']
				# high = res['groupData'][0]["results"][1]


				candlestick=go.Candlestick(x=total_df.index,
				                                     open=total_df['Open'],
				                                     high=total_df['High'],
				                                     low=total_df['Low'],  # Add this line if you have a Low column
				                                     close=total_df['Close'])
				volume_graph = go.Bar(x=total_df.index, y=total_df['Volume'], yaxis='y2', name='Volume', marker=dict(color='rgba(0, 0, 0, 0.3)'))
				indicator_graph = go.Scatter(x=total_df.index, y=dfindicator, mode='lines', name=indicatorname)
				# Create a candlestick chart
				fig = go.Figure(data=[candlestick,volume_graph])

				# Set chart layout
				fig.update_layout(
				title=stockname,
				xaxis_title='Time',
				yaxis_title='Price',
				xaxis_rangeslider_visible=False,
				# yaxis=dict(title='Price'),
				yaxis2=dict(title='Volume', overlaying='y', side='right'),
				yaxis3=dict(title='EMA', overlaying='y', side='left')
				# dragmode='pan'
				)

				# Display the chart using Streamlit
				st.plotly_chart(fig)

				# st.write(res)
			except Exception as e:
				st.warning("Something went wrong")
				# print(e)
				print(traceback.print_exc())
	except:
		st.warning("Something went wrong")
		print(traceback.print_exc())
	# with second_column:
	# 	st.subheader("Chart")




		
elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')
	
