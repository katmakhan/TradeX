
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

	st.title("TradeX")
	# st.markdown("##")


	# ---- SIDEBAR ----
	#Logout Button
	# authenticator.logout("Logout","sidebar")
	# Welcome Name
	name="Traders"
	st.sidebar.title(f"Welcome {name}")
	st.sidebar.header("Powered By StockEx")


	# options=['Analyse','Fetch']
	# options.append('None')
	# default_ix = options.index("None")
	# option = st.sidebar.selectbox(
	# 	"Select the Option",
	# 	options=options,
	# 	index=default_ix
	# )

	
	# Project or who paid is selected, then show debit and credit columns

	first_column, second_column = st.columns(2)
	with first_column:
		st.subheader("Terms and Conditions:")
		st.success("Educational and personel purpose only")
		st.markdown('''
		The following website have their respective api:
		- [Chartink](https://chartink.com/)
		- [NSE](https://www.nseindia.com/)
		- [Trendlyn](https://trendlyne.com/)
		- [Nifty Trader](https://www.niftytrader.in/)
		'''
		)
		st.warning("Over using the API might result in IP Restrictions.")

	# with second_column:
	# 	st.subheader("Conditions:")
	# 	st.write("Please use the webapp for personel purpose only")
	# 	st.markdown("Donot try to use the code for any type of server attacks")
	# 	st.markdown("Feel free to edit the code and use it for personel educational purpose only")
		
elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')
	
