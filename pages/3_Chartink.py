# Import Modules
from Modules.Chartink import get_chart
from Helpers import helper_functions_adv as help_function_adv

import streamlit as st  # pip install streamlit

# from google.oauth2.credentials import Credentials

# not working with google-auth-oauthlib==0.8.0
# pip install google-auth-oauthlib==0.4.6


# Authenticators
import streamlit_authenticator as stauth
import yaml
# import SafeLoader


# Running streamlit
st.set_page_config(page_title="TradeX", page_icon=":books:", 
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

	allstock_list=help_function_adv.fetch_allstocknames()

	# st.write(allstock_list)
	
	allstock_list.append('None')
	st.write("Total Stock List: ",len(allstock_list))
	default_ix = allstock_list.index("None")
	option = st.selectbox(
		"Select the Stock",
		options=allstock_list,
		index=default_ix
	)

	first_column, second_column = st.columns(2)
	with first_column:
		st.subheader("Chartink EMA:")

		# 	# Separate fields
		emalabel = 'ema 20'
		emavalue='Ema(  Close , 20 )'
		use_live = "1"
		limit = "1"
		size = "200"
		widget_id = "-1"
		end_time = "-1"
		timeframe = "Daily"
		symbol = "HEROMOTOCO"
		scan_link = "null"
		query = f"select open, high, low, close, volume, {emavalue} as '{emalabel}' where symbol='{symbol}'"
		res=get_chart.getchart_indicators(emalabel,emavalue,query,use_live,limit,size,widget_id,end_time,timeframe,symbol,scan_link)
		# # Traverse the data
		# groupdata=res['groupData'][0]['results']
		# for data in groupdata:
		# 	# print(data)
		# 	if data.get(emalabel) is not None:
		# 		print(data[emalabel])
		# 	print("---")
		st.write(res)


	with second_column:
		st.subheader("Chartink SMA:")

		# 	# Separate fields
		emalabel = 'sma 20'
		emavalue='Sma(  Close , 20 )'
		use_live = "1"
		limit = "1"
		size = "200"
		widget_id = "-1"
		end_time = "-1"
		timeframe = "Daily"
		symbol = "HEROMOTOCO"
		scan_link = "null"
		query = f"select open, high, low, close, volume, {emavalue} as '{emalabel}' where symbol='{symbol}'"
		res=get_chart.getchart_indicators(emalabel,emavalue,query,use_live,limit,size,widget_id,end_time,timeframe,symbol,scan_link)
		# # Traverse the data
		# groupdata=res['groupData'][0]['results']
		# for data in groupdata:
		# 	# print(data)
		# 	if data.get(emalabel) is not None:
		# 		print(data[emalabel])
		# 	print("---")
		st.write(res)

		
elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')
	
