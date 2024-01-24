# Import Modules
from Modules.NSE.NSE_Holidays import get_json_user_agent_Holidays as nse_holiday
from Modules.NSE.NSE_FNO import get_json_cookie_bypass_FNO as nse_fno
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
		res=nse_fno.index_optionchain('NIFTY')
		st.dataframe(res)

	with tab2:
		res=nse_fno.index_optionchain('BANKNIFTY')
		st.dataframe(res)

	with tab3:
		allstock_json=nse_fno.underlying_fnolist()
		allstock_list=[]

		for stock in allstock_json:
			allstock_list.append(stock['symbol'])

		# st.write(allstock_list)
			
		# allstock_list.append('None')
		st.write("Total Stock List: ",len(allstock_list))
		# default_ix = allstock_list.index("ACC")
		default_ix=0
		option = st.selectbox(
			"Select the Stock",
			options=allstock_list,
			index=default_ix
		)

		res=nse_fno.stock_optionchain(option)
		st.dataframe(res)

	with tab4:
		st.header("Holidays:")
		res=nse_holiday.fno_holiday_list()

		st.dataframe(res)

	# st.markdown(res)
	# button_clicked = st.button("Click me!")

	# # Check if the button is clicked
	# if button_clicked:
	#   st.write("Button clicked!")
		
elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')
	
