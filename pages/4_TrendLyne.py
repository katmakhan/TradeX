# Import Modules
# from Modules.Chartink import get_chart


import streamlit as st  # pip install streamlit
from Modules.Trendlyne import get_json_cookie_bypass_trendlyne as trendlyne 

# from google.oauth2.credentials import Credentials

# not working with google-auth-oauthlib==0.8.0
# pip install google-auth-oauthlib==0.4.6


# Authenticators
import streamlit_authenticator as stauth
import yaml
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

	st.title("Trendlyne")
	# st.markdown("##")


	# ---- SIDEBAR ----
	#Logout Button
	# authenticator.logout("Logout","sidebar")
	# Welcome Name
	# name="User"
	# st.sidebar.title(f"Welcome {name}")
	st.header("Most Active Calls")
	try:
		res=trendlyne.mostactive_calls()
		st.write(res)
	except:
		st.warning("Something went wrong")



		
elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')
	
