
import streamlit as st  # pip install streamlit

from Modules.Nifty_Trader import niftytrader_apis as niftytrader_api
# from google.oauth2.credentials import Credentials

# not working with google-auth-oauthlib==0.8.0
# pip install google-auth-oauthlib==0.4.6


# Authenticators
import streamlit_authenticator as stauth
import yaml
import traceback
import pandas as pd
# import SafeLoader


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

	st.title("Nifty Trader")
	# st.markdown("##")


	# ---- SIDEBAR ----
	#Logout Button
	# authenticator.logout("Logout","sidebar")
	# Welcome Name
	# name="User"
	# st.sidebar.title(f"Welcome {name}")
	# st.sidebar.header("Dashboard")

	try:
		gap_up_stocks,gap_down_stocks=niftytrader_api.gap_analysis()
		first_column, second_column = st.columns(2)

		gap_up_stocks=pd.DataFrame(gap_up_stocks)
		gap_down_stocks=pd.DataFrame(gap_down_stocks)

		# gap_up_stocks.drop(['B', 'C'], axis=1)
		with first_column:
			st.subheader("Gap UP Stocks:")
			if len(gap_up_stocks)!=0:
				st.dataframe(gap_up_stocks[['symbol_name','gap_status','change_percent',
					'today_close',
					'gap_value']])
			else:
				st.warning("No results found")

		with second_column:
			st.subheader("Gap Down Stocks:")
			if len(gap_down_stocks)!=0:
				st.dataframe(gap_down_stocks[['symbol_name','gap_status','change_percent',
					'today_close',
					'gap_value']])
			else:
				st.warning("No results found")
	except Exception as e:
		st.warning("Something went wrong")
		print(traceback.print_exc())

elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')
	
