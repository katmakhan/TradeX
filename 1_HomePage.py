
import streamlit as st  # pip install streamlit

# from google.oauth2.credentials import Credentials

# not working with google-auth-oauthlib==0.8.0
# pip install google-auth-oauthlib==0.4.6
import googletag_inject as googletagm

# Authenticators
import streamlit_authenticator as stauth
import yaml
# import SafeLoader



# Running streamlit
st.set_page_config(page_title="TradeX", page_icon="🔰", 
layout="wide")

# To inject google tag into the file, does not work inside streamlit cloud
# googletagm.inject_ga()

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
		- [TradingView](https://in.tradingview.com/)
		- [Trendlyn](https://trendlyne.com/)
		- [Nifty Trader](https://www.niftytrader.in/)
		- [Grow](https://groww.in/)
		'''
		)
		st.warning("Over using the API might result in IP Restrictions.")

	# with second_column:
	# 	st.subheader("Nifty 50")
	# 	code_minichart_nifty = '''
	# 	<!-- TradingView Widget BEGIN -->
	# 	<iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=NSE%3ANIFTY&locale=in" width="100%" height="100%" frameborder="0" allowtransparency="true" allowfullscreen="true" scrolling="no"></iframe>
	# 	<!-- TradingView Widget END -->
	# 	'''
	# 	st.markdown(code_minichart_nifty, unsafe_allow_html=True)

	# 	st.subheader("BankNifty")
	# 	code_minichart_banknifty = '''
	# 	<!-- TradingView Widget BEGIN -->
	# 	<iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=NSE%3ABANKNIFTY&locale=in" width="100%" height="100%" frameborder="0" allowtransparency="true" allowfullscreen="true" scrolling="no"></iframe>
	# 	<!-- TradingView Widget END -->
	# 	'''
	# 	st.markdown(code_minichart_banknifty, unsafe_allow_html=True)

	# with second_column:

	# 	candles_data=
	# 	# Extracting timestamps and values from the data
	# 	timestamps, values = zip(*candles_data)

	# 	# Convert timestamps to datetime for better formatting on x-axis
	# 	dates = [pd.to_datetime(timestamp, unit='s') for timestamp in timestamps]

	# 	# Create a Plotly line chart
	# 	fig = go.Figure(data=go.Scatter(x=dates, y=values, mode='lines'))

	# 	# Customize the layout
	# 	fig.update_layout(
	# 	    title='Line Chart of Candles',
	# 	    xaxis_title='Timestamp',
	# 	    yaxis_title='Values',
	# 	)

	# 	# Streamlit app
	# 	st.title("Line Chart with Plotly")

	# 	# Display the Plotly chart
	# 	st.plotly_chart(fig)


	with st.expander("Forex"):
		st.subheader("Tradingview")
		tradingview_forex_widget="https://www.tradingview-widget.com/embed-widget/forex-cross-rates/?locale=in#%7B%22width%22%3A%22100%25%22%2C%22height%22%3A%22100%25%22%2C%22isTransparent%22%3Afalse%2C%22currencies%22%3A%5B%22EUR%22%2C%22USD%22%2C%22JPY%22%2C%22GBP%22%2C%22CHF%22%2C%22AUD%22%2C%22CAD%22%2C%22NZD%22%5D%2C%22colorTheme%22%3A%22light%22%2C%22utm_source%22%3A%22in.tradingview.com%22%2C%22utm_medium%22%3A%22widget_new%22%2C%22utm_campaign%22%3A%22forex-cross-rates%22%2C%22page-uri%22%3A%22in.tradingview.com%2Fwidget%2F%22%7D"
		iframe_code = f'<iframe src="{tradingview_forex_widget}" width="100%" height="300" frameborder="0" allowfullscreen></iframe>'
		st.markdown(iframe_code, unsafe_allow_html=True)
		
elif authentication_status == False:
	st.error('Username/password is incorrect')
elif authentication_status == None:
	st.warning('Please enter your username and password')
	
