# Import Modules
# from Modules.Chartink import get_chart


import streamlit as st  # pip install streamlit

# from google.oauth2.credentials import Credentials

# not working with google-auth-oauthlib==0.8.0
# pip install google-auth-oauthlib==0.4.6

from Modules.Grow import grow_apis as grow_api

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

	st.title("Grow")
	# st.markdown("##")


	# ---- SIDEBAR ----
	#Logout Button
	# authenticator.logout("Logout","sidebar")
	# Welcome Name
	# name="User"
	# st.sidebar.title(f"Welcome {name}")
	st.subheader("Most Active Options")
	try:
		res=grow_api.nifty_topoptions()
		derivatives_data = res["derivatives"]
		df = pd.json_normalize(derivatives_data)

		# Rename columns
		df = df.rename(columns={
			'livePrice.symbol': 'Symbol',
			'livePrice.ltp': 'LTP',
			'livePrice.dayChange': 'Change',
			'livePrice.dayChangePerc': 'Percent',
			'livePrice.volume': 'Volume',
		})


		st.dataframe(df[['Symbol','LTP','Change','Percent','Volume']])

	except:
		st.warning("Something went wrong")
		print(traceback.print_exc())



		
elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')
	
