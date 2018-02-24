from flask import Flask, request
import requests
import sys
import os
import json
from Credentials import *


# ____________________________________________________________________
# price getter
# prep
import urllib.request, json
URL = "https://api.coinmarketcap.com/v1/ticker/?limit=300"

with urllib.request.urlopen(URL) as url:
    s = url.read()
data = json.loads(s)

portfolioList = [['NEO', 42.1], ['WTC', 67.94], ['VEN', 226.13], ['ETH', 0.895], ['NET', 173.2], ['LTC', 3.49], ['JNT', 1297.0], ['OMG', 27.4], ['MOD', 95.8], ['LSK', 8.0], ['STRAT', 20.4], ['ICX', 26.18], ['FCT', 3.7], ['REQ', 327.7], ['MIOTA', 49.5], ['BTC', 0.00912], ['NANO', 10.04], ['SALT', 11.0], ['TRX', 500.0]]




# defs
def refreshPrices():
    with urllib.request.urlopen(URL) as url:
        global s, data
        s = url.read()
        data = json.loads(s)
        
def getCoinUSDPrice(ticker):
    coin_info = next(coin for coin in data if coin[u'symbol'] == ticker)
    return (coin_info[u'price_usd'])

def getCoinList():
    coinList = []
    for coinDetails in data:
        coinName = coinDetails[u'symbol']
        coinList += [coinName]
    return coinList



# _______________________________________________________________________
# messenger bot
app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        return request.args.get('hub.challenge', 200)
    else:
        return 'Error, wrong validation token lol'


@app.route('/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]
                        
                    send_message(sender_id, 'confirmation 1')
                    
                    if message_text in getCoinList():
                        send_message(sender_id, 'confirmation 2')
                        refreshPrices()
                        send_message(sender_id, 'confirmation 3')
                        botReply = getCoinUSDPrice(message_text)
                        send_message(sender_id, 'confirmation 4')
                        send_message(sender_id, botReply)
                        send_message(sender_id, 'confirmation 5')
                    
                    else:
                        send_message(sender_id, 'confirmation 6')
                        send_message(sender_id, 'Coin not found, try again.')

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port )
