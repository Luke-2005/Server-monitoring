import requests

chat_id = "7028262052"
token = "6873214690:AAHZwUajql2FxWDP4sPfl6MqHhNLjh5gSd0"

# url = f"https://api.telegram.org/bot{token}/getUpdates"
# print(requests.get(url).json()) 

def send_msg(messageText):
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + messageText 
   results = requests.get(url_req)

