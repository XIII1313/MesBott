from flask import Flask, request
import requests
import sys
import os
import json
from Credentials import *
import random



#trigger lists 
coinUSDValueTrigger = ["in USD", "USD price", "USD price of", "to USD", "USD",
                       "in usd", "usd price", "usd price of", "to usd", "usd",
                       "Usd price", "Usd price of"]

coinBTCValueTrigger = ["in BTC", "BTC price", "BTC price of", "to BTC", "BTC",
                       "in btc", "btc price", "btc price of", "to btc", "btc",
                       "Btc price", "Btc price of"]

portfolioUSDTrigger = ["p", "port", "portfolio", "portfolio in usd", "portfolio in USD",
                       "P", "Port", "Portfolio", "Portfolio in usd", "Portfolio in USD"]

portfolioBTCTrigger = ["p btc", "port btc", "portfolio btc", "p in btc", "port in btc", "portfolio in btc"
                        "p BTC", "port BTC", "portfolio BTC", "p in BTC", "port in BTC", "portfolio in BTC"
                        "P btc", "Port btc", "Portfolio btc", "P in btc", "Port in btc", "Portfolio in btc" 
                        "P BTC", "Port BTC", "Portfolio BTC", "P in BTC", "Port in BTC", "Portfolio in BTC"]

cmcLinkTriggerOne = ["cmc", "coinmarketcap",
                    "Cmc", "Coinmarketcap"]

cmcLinkTriggerTwo = ["cmc of", "coinmarketcap of",
                    "Cmc of", "Coinmarketcap of"]

allInTrigger = ["all in", "all-in",
                "All in", "All-in"]

addressTriger = ["address", "adres", "search address",
                 "Address", "Adres", "Search address"]

allInTriggerPercentage = ["%"]

deleteQuickReplyTrigger = ["delete quick reply", "del q r",
                           "Delete quick reply", "Del q r"]

addQuickReplyTrigger = ["add quick reply", "add q r",
                        "Add quick reply", "Add q r"]

helloTrigger = ["hey", "hello", "hi",
               "Hey", "Hello", "Hi"]



# outputs
helloOutput = ["Hey, human.", "Hello!", "Hi!", "Hey!"]



# ____________________________________________________________________
# price getter
# prep

import urllib.request, json
URL = "https://api.coinmarketcap.com/v1/ticker/?limit=400"

with urllib.request.urlopen(URL) as url:
    s = url.read()
data = json.loads(s)

# var
portfolioList = [['NEO', 42.1], ['WTC', 67.94], ['VEN', 226.13], ['ETH', 0.895], ['NET', 173.2], ['LTC', 3.49], ['JNT', 1297.0], ['OMG', 27.4], ['MOD', 95.8], ['LSK', 8.0], ['STRAT', 20.4], ['ICX', 26.18], ['FCT', 3.7], ['REQ', 327.7], ['MIOTA', 49.5], ['BTC', 0.00912], ['NANO', 10.04], ['SALT', 11.0], ['TRX', 500.0]]

quick_replies_list = [{
    "content_type":"text",
    "title":"BTC",
    "payload":"btc",
},
{
    "content_type":"text",
    "title":"WTC",
    "payload":"WTC",
},
{
    "content_type":"text",
    "title":"Portfolio",
    "payload":"Portfolio",
},
{
    "content_type":"text",
    "title":"donate",
    "payload":"donate",
},
{
    "content_type": "text",
    "title": "help",
    "payload": "help",
}
]

# _____________________________________________________________________
# defs for API
def refreshPrices():
    with urllib.request.urlopen(URL) as url:
        global s, data
        s = url.read()
    data = json.loads(s)

        

def getCoinUSDPrice(ticker):
    coin_info = next(coin for coin in data if coin[u'symbol'] == ticker)
    return (coin_info[u'price_usd'])



def getCoinBTCPrice(ticker):
    coin_info = next(coin for coin in data if coin[u'symbol'] == ticker)
    return (coin_info[u'price_btc'])
  
  
  
def getCoinID(ticker):
    coin_info = next(coin for coin in data if coin[u'symbol'] == ticker)
    return (coin_info[u'id'])



def getCoinList():
    coinList = []
    for coinDetails in data:
        coinName = coinDetails[u'symbol']
        coinList += [coinName]
    return coinList



def coin1ToCoin2(message_text): 
#
# input: "10 VEN to NEO"
# output: "With 10 you can buy x amount of NEO"
#
    coin1 = sliceWords(message_text, 1, 2)
    amountOfCoin1 = sliceWords(message_text, 0, 1)
    coin2 = sliceWords(message_text, 3, 4)
    amountOfCoin2 = (float(getCoinUSDPrice(coin1)) * float(amountOfCoin1)) / float(getCoinUSDPrice(coin2))
    reply = "With {} {} you can buy {} {}.".format(amountOfCoin1, coin1, round(amountOfCoin2, 4), coin2)
    return reply



def coin1ToUSD(message):
#
# input: "10 VEN to USD"
# output: "10 VEN is $x"
#
    coin1 = sliceWords(message, 1, 2)
    amountOfCoin1 = sliceWords(message, 0, 1)
    amountOfUSD = float(getCoinUSDPrice(coin1)) * float(amountOfCoin1)
    reply = "{} {} is ${}.".format(amountOfCoin1, coin1, round(amountOfUSD, 2))
    return reply
  
  
  
def USDTocoin1(message):
#
# input: "10 USD to VEN"
# output: "10 USD is x VEN"
#
    coin1 = sliceWords(message, 3, 4)
    amountOfUSD = sliceWords(message, 0, 1)
    amountOfCoin1 = float(amountOfUSD) / float(getCoinUSDPrice(coin1))
    reply = "${} is {} {}.".format(amountOfUSD, round(amountOfCoin1, 8), coin1)
    return reply



def getPortfolioUSDPrice(portfoliolist):
    portfolioUSDValue = 0.0
    for sublist in portfoliolist:

        totalCoinValue = float(getCoinUSDPrice(sublist[0])) * sublist[1]
        portfolioUSDValue += totalCoinValue

    return round(portfolioUSDValue, 2)



def getPortfolioBTCPrice(portfoliolist):

    portfolioBTCValue = 0.0

    for sublist in portfoliolist:

        totalCoinValue = float(getCoinBTCPrice(sublist[0])) * sublist[1]
        portfolioBTCValue += totalCoinValue

    return round(portfolioBTCValue, 8)
  
  
  
def allIn(portfoliolist, coinTicker):
    userPortfolio = getPortfolioUSDPrice(portfoliolist)
    coinprice = getCoinUSDPrice(coinTicker)
    amountOfCoinsIfAllIn = round(float(userPortfolio) / float(coinprice), 4)
    return [amountOfCoinsIfAllIn, userPortfolio]



def allInPercent(portfoliolist, coinTicker, percentageNumberString):
    userPortfolio = getPortfolioUSDPrice(portfoliolist)

    percentageNumberFloat = float(percentageNumberString)
    percentage = percentageNumberFloat / 100

    userPortfolioPercentage = userPortfolio * percentage

    coinprice = getCoinUSDPrice(coinTicker)
    amountOfCoinsIfAllInPercentage = round(float(userPortfolioPercentage) / float(coinprice), 4)
    return [amountOfCoinsIfAllInPercentage, round(userPortfolioPercentage, 2)]
  
  
  
def addressLinkGiver(addressString):
    address = sliceWords(addressString, -1, None)

    # NEO
    if address[0] ==  "A" and len(address) > 10:
        baseLink = "https://neotracker.io/address/"
        completeLink =  baseLink + address
        return [completeLink, "Neo"]

    # LTC
    elif address[0] ==  "L" and len(address) > 10:
        baseLink = "https://live.blockcypher.com/ltc/address/"
        completeLink = baseLink + address + "/"
        return [completeLink, "Litecoin"]

    # ETH
    elif address[0:2] ==  "0x" and len(address) > 10:
        baseLink = "https://etherscan.io/address/"
        completeLink = baseLink + address
        return [completeLink, "Ethereum"]

    # BTC
    elif (address[0] == "1" or address[0] == "3" or address[0:3] == "bc1") and len(address) > 10:
        baseLink = "https://live.blockcypher.com/btc/address/"
        completeLink = baseLink + address + "/"
        return [completeLink, "Bitcoin"]

    else:
        reply = "Sorry, it seems that this isn't a supported address. At the moment only the addresses of the following blockchains are supported: \n-Bitcoin \n-Ethereum \n-Litecoin \n-Neo"
        return [reply]

      

# _______________________________________________________________________
# extra def

def sliceWords(string, beginIndex, endIndex):
    stringList = string.split()
    stringList = stringList[beginIndex:endIndex]
    newString = ""
    for word in stringList:
        newString += word
        newString += " "
    newString = newString[0: len(newString) - 1]
    return newString
  

  
def getStringBeforeCharacter(string, character):
    substring = ""

    for index in range(len(string)):

        if string[index] == character:
            break

        else:
            substring += string[index]

    return substring

  
  
def isFloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False



def isInt(value):
    try:
        float(value)
        return True
    except ValueError:
        return False  
      
      

def slideObjectInList(newObject, oldList, index = 2):
    if newObject in oldList:
        None
    else:
        oldList.pop(index)
        oldList.insert(0, newObject)



def createQuickReplyWithGivenText(quickreplytext):
    quickreply = {
    "content_type":"text",
    "title":quickreplytext,
    "payload":quickreplytext,
    }
    return quickreply
  
  
  
def refreshQuickreplyList(messagetext, quickreplylist):
    quickreply = createQuickReplyWithGivenText(messagetext)
    slideObjectInList(quickreply, quickreplylist)



def addQuickReply(quickreply, quickreplylist):
    if len(quickreplylist) == 11:
        return "You have created the max amount of quick replies. You will need to delete a quick reply by typing 'delete quick reply' and the text of the quick reply."

    elif quickreply in quickreplylist[3:]:
        return "You already have this quick reply."

    else:
        quickreplylist.insert(3, quickreply)
        return "I added that quick reply."



def deleteQuickReply(quickreply, quickreplylist):
    counter = 0
    
    if len(quickreplylist) == 5:
        return "You don't have any quick replies to delete. You can't delete default quick replies."

    else:
        lengthOfOldList = len(quickreplylist)
        for index in range(lengthOfOldList - 2):

            if index in [0,1,2]:
                None

            else:
                if quickreplylist[index] == quickreply:
                    quickreplylist.pop(index)
                    break

                else:
                    counter += 1

        if counter == lengthOfOldList - 5:
            return "It seems that you haven't made this quick reply yet. \nRemember that you can't delete default quick replies."

        else:
            return "I deleted that quick reply."



def chooseRandomObjectFromList(list):
    index = random.randint(0, len(list) - 1)
    print(index)
    randomObject = list[index]
    return randomObject
  
  
  
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
# ____________________________________________________________________
                    
                    refreshPrices()
                    coinList = getCoinList()
                
                
# x coinName to usd, x coinName1 to coinName 2               
                    if (isFloat(sliceWords(message_text, 0, 1)) or isInt(sliceWords(message_text, 0, 1))) and sliceWords(message_text, 2, 3) in ["to", "in"]:
                        
                        if sliceWords(message_text, 3, 4) in ['usd', 'USD']:
                      
                            if sliceWords(message_text, 1, 2) in coinList:
                              refreshQuickreplyList(message_text, quick_replies_list)
                              botReply = coin1ToUSD(message_text)
                              send_message(sender_id, botReply)
                              
                            else:
                              botReply = "Oops, it seems like that coin isn't included"
                              send_message(sender_id, botReply)

                        elif sliceWords(message_text, 1, 2) in coinList and sliceWords(message_text, 3, 4) in coinList:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            botReply = coin1ToCoin2(message_text)
                            send_message(sender_id, botReply)
                            
                        elif sliceWords(message_text, 1, 2) in ['usd', 'USD']:
                            if sliceWords(message_text, 3, 4) in coinList:
                              refreshQuickreplyList(message_text, quick_replies_list)
                              botReply = USDTocoin1(message_text)
                              send_message(sender_id, botReply)

                            else:
                              botReply = "Oops, it seems like that coin isn't included"
                              send_message(sender_id, botReply)
                            
                        else:
                            botReply = "Sorry, it seems that a coin is not on coinmarketcap."
                            send_message(sender_id, botReply)

                            
# Portfolio usd                            
                    elif message_text in portfolioUSDTrigger:
                        refreshQuickreplyList(message_text, quick_replies_list)
                        botReply = getPortfolioUSDPrice(portfolioList)
                        send_message(sender_id, "Your portfolio is valued at ${}.".format(botReply))
                            
                  
# Portfolio btc                  
                    elif message_text in portfolioBTCTrigger:
                        refreshQuickreplyList(message_text, quick_replies_list)
                        botReply = getPortfolioBTCPrice(portfolioList)
                        send_message(sender_id, "Your portfolio is valued at {} BTC.".format(botReply))
                  
                  
# Price of coin                  
                    elif message_text.upper() in getCoinList():
                        refreshQuickreplyList(message_text, quick_replies_list)
                        botReply = "${}".format(round(float(getCoinUSDPrice(message_text.upper())), 2))
                        send_message(sender_id, botReply)
        
        
# Price of coin lowercase                 
                    elif message_text in getCoinList():
                        refreshQuickreplyList(message_text, quick_replies_list)
                        botReply = "${}".format(round(float(getCoinUSDPrice(message_text)), 2))
                        send_message(sender_id, botReply)

                          
# USD price of coin 1                             
                    elif sliceWords(message_text, 0, len(message_text.split()) - 1) in coinUSDValueTrigger:
                        if sliceWords(message_text, -1, None) in coinList:
                          refreshQuickreplyList(message_text, quick_replies_list)
                          botReply = "${}".format(round(float(getCoinUSDPrice(sliceWords(message_text, -1, None))), 2))
                          send_message(sender_id, botReply)

                        else:
                          botReply = "Oops, it seems like that coin isn't included"
                          send_message(sender_id, botReply)

                          
# USD price of coin 2                             
                    elif sliceWords(message_text, 1, len(message_text.split())) in coinUSDValueTrigger:
                        if sliceWords(message_text, 0, 1) in coinList:
                          refreshQuickreplyList(message_text, quick_replies_list)
                          botReply = "${}".format(round(float(getCoinUSDPrice(sliceWords(message_text, 0, 1))), 2))
                          send_message(sender_id, botReply)

                        else:
                          botReply = "Oops, it seems like that coin isn't included"
                          send_message(sender_id, botReply)
                    
                    
# Cmc of coin                   
                    elif sliceWords(message_text, 0, 2) in cmcLinkTriggerTwo:
                        
                      if sliceWords(message_text, 2, 3) in coinList: 
                        refreshQuickreplyList(message_text, quick_replies_list)
                        inputCoin = sliceWords(message_text, 2, 3)
                        botReply = "Here is the link to coinmarketcap of {}. \n \nLink: https://coinmarketcap.com/currencies/{}/".format(inputCoin, getCoinID(inputCoin))
                        send_message(sender_id, botReply)
                
                      else:
                        botReply = "Oops, it seems like that coin isn't included"
                        send_message(sender_id, botReply)

                        
# cmc coin                        
                    elif sliceWords(message_text, 0, 1) in cmcLinkTriggerOne:
                      
                      if sliceWords(message_text, 1, 2) in coinList:
                        refreshQuickreplyList(message_text, quick_replies_list)
                        inputCoin = sliceWords(message_text, 1, 2)
                        botReply = "Here is the link to coinmarketcap of {}. \n \nLink: https://coinmarketcap.com/currencies/{}/".format(inputCoin, getCoinID(inputCoin))
                        send_message(sender_id, botReply)
                        
                      else:
                        botReply = "Oops, it seems like that coin isn't included"
                        send_message(sender_id, botReply)
                        
                        
# BTC price of coin 1        
                    elif sliceWords(message_text, 0, len(message_text.split()) - 1) in coinBTCValueTrigger:
                        if sliceWords(message_text, -1, None) in coinList:
                          refreshQuickreplyList(message_text, quick_replies_list)
                          botReply = "{} BTC".format(round(float(getCoinBTCPrice(sliceWords(message_text, -1, None))), 8))
                          send_message(sender_id, botReply)

                        else:
                          botReply = "Oops, it seems like that coin isn't included"
                          send_message(sender_id, botReply)

                          
# BTC price of coin 2                             
                    elif sliceWords(message_text, 1, len(message_text.split())) in coinBTCValueTrigger:
                        if sliceWords(message_text, 0, 1) in coinList:
                          refreshQuickreplyList(message_text, quick_replies_list)
                          botReply = "{} BTC".format(round(float(getCoinBTCPrice(sliceWords(message_text, 0, 1))), 8))
                          send_message(sender_id, botReply)

                        else:
                          botReply = "Oops, it seems like that coin isn't included"
                          send_message(sender_id, botReply)
                        
                        
# all-in                        
                    elif sliceWords(message_text, 0, 1) in allInTrigger:

                      inputCoin = sliceWords(message_text, 1, 2)

                      if inputCoin in coinList:
                        refreshQuickreplyList(message_text, quick_replies_list)
                        allInList = allIn(portfolioList, inputCoin)
                        numberOfCoins = allInList[0]
                        portfolioValue = allInList[1]

                        botReply = "If you would go all in on {}, you would have {} {}. Which is worth ${}".format(inputCoin, numberOfCoins, inputCoin, portfolioValue)
                        send_message(sender_id, botReply)

                      else:
                        botReply = "It seems that I can't find your coin, sorry."
                        send_message(sender_id, botReply)
              
                    
# all in                
                    elif sliceWords(message_text, 0, 2) in allInTrigger:
                      inputCoin = sliceWords(message_text, 2, 3)

                      if inputCoin in coinList:
                        refreshQuickreplyList(message_text, quick_replies_list)
                        allInList = allIn(portfolioList, inputCoin)
                        numberOfCoins = allInList[0]
                        portfolioValue = allInList[1]
                        botReply = "If you would go all in on {}, you would have {} {}. Which is worth ${}".format(inputCoin, numberOfCoins, inputCoin, portfolioValue)
                        send_message(sender_id, botReply)

                      else:
                        botReply = "It seems that I can't find your coin, sorry."
                        send_message(sender_id, botReply)
                
                
# all in %                
                    elif "%" in list(message_text):
                      inputCoin = sliceWords(message_text, -1, None)

                      if inputCoin in coinList:
                        refreshQuickreplyList(message_text, quick_replies_list)
                        percentageNumber = getStringBeforeCharacter(message_text, "%")
                        allInPercentList = allInPercent(portfolioList, inputCoin, percentageNumber)
                        numberOfCoins = allInPercentList[0]
                        value = allInPercentList[1]
                        botReply = "If you would allocate {}% of your portfolio to {}, you would have {} {}. Which is worth ${}".format(percentageNumber, inputCoin, numberOfCoins, inputCoin, value)
                        send_message(sender_id, botReply)

                      else:
                        botReply = "It seems that I can't find your coin, sorry."
                        send_message(sender_id, botReply)
                
                
# address search
                    elif sliceWords(message_text, 0, len(message_text.split()) - 1) in addressTriger:
                      address = sliceWords(message_text, -1, None)
                      addressList = addressLinkGiver(address)

                      if len(addressList) == 2:
                        link = addressList[0]
                        addressType = addressList[1]

                        if addressType == "Ethereum":
                          refreshQuickreplyList(message_text, quick_replies_list)
                          botReply = "This is an {} address. \n \nHere is a link to the address: {}".format(addressType, link)
                          send_message(sender_id, botReply)

                        else:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            botReply = "This is a {} address. \n \nHere is a link to the address: {}".format(addressType, link)
                            send_message(sender_id, botReply)

                      elif len(addressList) == 1:
                        botReply = addressList[0]
                        send_message(sender_id, botReply)
                        
                        
# add quick reply
                    elif sliceWords(message_text, 0, 3) in addQuickReplyTrigger:
                      textOfQuickReply = sliceWords(message_text, 3, None)
                      quickReply = createQuickReplyWithGivenText(textOfQuickReply)
                      botReply = addQuickReply(quickReply, quick_replies_list)
                      send_message(sender_id, botReply)


# delete quick reply
                    elif sliceWords(message_text, 0, 3) in deleteQuickReplyTrigger:
                      textOfQuickReply = sliceWords(message_text, 3, None)
                      quickReply = createQuickReplyWithGivenText(textOfQuickReply)
                      botReply = deleteQuickReply(quickReply, quick_replies_list)
                      send_message(sender_id, botReply)
            
            
# greet the bot
                    elif message_text in helloTrigger:
                      botReply = chooseRandomObjectFromList(helloOutput)
                      send_message(sender_id, botReply)
               
        
        
# last answer                
                    else:
                        send_message(sender_id, "Sorry I didn't get that or maybe your coin isn't on coinmarketcap.")
                  
                  
                        
#_____________________________________________________________________________ 

                  
                  
                  
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
            "text": message_text,
            "quick_replies":quick_replies_list
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
