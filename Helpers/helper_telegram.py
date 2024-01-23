
#For invoking http requests
import requests

# Sent notification to telegram group
def update_telegram(title,body):
	#Bot Name: TradeX_bot
	#If you don't have one, create one using botfather
	#Create BOTS using https://t.me/botfather
	#Put a unique profile pic for bot, for uniqueness
	#Get the http api
	http_api="123554:AAAAAAAAAAAAAAA-XXXXXXXX"

	#Add the bot to the group
	#Then go to this link to get the latest updates of the bot
	#https://api.telegram.org/bot<http_api>/getUpdates
	#https://api.telegram.org/bot123554:AAAAAAAAAAAAAAA-XXXXXXXX/getUpdates
	#Find the group id from updates "chat":{"id":-"
	chat_id="-11111111"


	messageurl1="https://api.telegram.org/bot"+http_api+"/sendMessage?chat_id="+chat_id+"&text="

	msg1=messageurl1+title+"\n\n"+body
	requests.get(msg1)
	print("Successfully sent the message")
