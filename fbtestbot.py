from flask import Flask, request
import requests
import sys
import os
import json
from Credentials import *
import random

# trigger lists
coinUSDValueTrigger = ["in USD", "USD price", "USD price of", "to USD", "USD",
                       "in usd", "usd price", "usd price of", "to usd", "usd",
                       "Usd price", "Usd price of"]

coinBTCValueTrigger = ["in BTC", "BTC price", "BTC price of", "to BTC", "BTC",
                       "in btc", "btc price", "btc price of", "to btc", "btc",
                       "Btc price", "Btc price of"]

portfolioUSDTrigger = ["p", "port", "portfolio", "portfolio in usd", "portfolio in USD",
                       "P", "Port", "Portfolio", "Portfolio in usd", "Portfolio in USD"]

portfolioBTCTrigger = ["p btc", "port btc", "portfolio btc", "p in btc", "port in btc", "portfolio in btc",
                       "p BTC", "port BTC", "portfolio BTC", "p in BTC", "port in BTC", "portfolio in BTC",
                       "P btc", "Port btc", "Portfolio btc", "P in btc", "Port in btc", "Portfolio in btc",
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

donateTriggers = ["donate", "donation",
                  "Donate", "Donation"]

supplyTrigger = ["supply", "supply of",
                 "Supply", "Supply of"]

marketCapTrigger = ["market cap", "mc", "m c", "market capitalization", "market cap of", "market capitalization of",
                    "Market cap", "Mc", "M c", "Market capitalization", "Market cap of", "Market capitalization of"]

volumeTrigger = ["volume", "24h volume", "volume of", "24h volume of",
                 "Volume", "24 Volume of"]

rankTrigger = ["rank", "rank of",
               "Rank", "Rank of"]

changeTrigger = ["change", "change of",
                 "Change", "Change of"]

specificChangeTrigger = ["24h change", "7d change", "1h change", "24 hour change", "7 day chage", "1 hour change",
                         "24h change of", "7d change of", "1h change of", "24 hour change of", "7 day chage of",
                         "1 hour change of"]

h24ChangeTrigger = ["24h change", "24 hour change",
                    "24h change of", "24 hour change of"]

h1ChangeTrigger = ["1h change", "24 hour change", "1 hour change",
                   "1h change of", "1 hour change of"]

d7ChangeTrigger = ["7d change", "7 day chage",
                   "7d change of", "7 day chage of"]

USDValueTrigger = ["USD price", "USD price of",
                   "usd price", "usd price of", "price",
                   "Usd price", "Usd price of", "Price"]

BTCValueTrigger = ["BTC price", "BTC price of", "price BTC", "price BTC of",
                   "btc price", "btc price of", "price btc", "price btc of",
                   "Btc price", "Btc price of", "Price btc", "Price BTC", "Price btc of", "Price BTC of"]

coinInfoCombinedTrigger = supplyTrigger + marketCapTrigger + volumeTrigger + rankTrigger + changeTrigger + specificChangeTrigger + USDValueTrigger + BTCValueTrigger

ATHPriceTrigger = ["ath", "ath of", "all time high", "all time high of",
                   "ath price", "ath price of", "all time high price", "all time high price of"]

ATHDateTrigger = ["ath date", "ath date of", "all time high date", "all time high date of"]

daysSinceATHTrigger = ["days sice ath", "days since ath of", "number of days since ath", "number of days since ath of", "amount of days since ath", "amount of days since ath of",
                       "days sice all time high", "days since all time high of", "number of days since all time high", "number of days since all time high of", "amount of days since all time high", "amount of days since all time high of"]

percentageToATHTrigger = ["percentage to ath", "percentage to ath of", "percentage to all time high", "percentage to all time high of"]

percentageFromATHTrigger = ["percentage from ath", "percentage from ath of", "percentage from all time high", "percentage from all time high of",
                            "percentage away from ath", "percentage away from ath of", "percentage away from all time high", "percentage away from all time high of",
                            "% from ath", "% from ath of", "% from all time high", "% from all time high of",
                            "% away from ath", "% away from ath of", "% away from all time high", "% away from all time high of"]

coinATHInfoCombinedTrigger = ATHPriceTrigger + ATHDateTrigger + daysSinceATHTrigger + percentageToATHTrigger + percentageFromATHTrigger

# outputs
helloOutput = ["Hey, human.", "Hello!", "Hi!", "Hey!"]

# ____________________________________________________________________
# price getter
# prep

import urllib.request, json

CMC_URL = "https://api.coinmarketcap.com/v1/ticker/?limit=300"

with urllib.request.urlopen(CMC_URL) as cmc_url:
    s = cmc_url.read()
CMCdata = json.loads(s)

# var
# portfolioList = [['NEO', 42.1], ['WTC', 67.94], ['VEN', 226.13], ['ETH', 0.895], ['NET', 173.2], ['LTC', 3.49],
#                  ['JNT', 1297.0], ['OMG', 27.4], ['MOD', 95.8], ['LSK', 8.0], ['STRAT', 20.4], ['ICX', 26.18],
#                  ['FCT', 3.7], ['REQ', 327.7], ['MIOTA', 49.5], ['BTC', 0.00912], ['NANO', 10.04], ['SALT', 11.0],
#                  ['TRX', 500.0]]

quick_replies_list = [{
    "content_type": "text",
    "title": "BTC",
    "payload": "btc",
},
    {
        "content_type": "text",
        "title": "WTC",
        "payload": "WTC",
    },
    {
        "content_type": "text",
        "title": "Portfolio",
        "payload": "Portfolio",
    },
    {
        "content_type": "text",
        "title": "donate",
        "payload": "donate",
    },
    {
        "content_type": "text",
        "title": "help",
        "payload": "help",
    }
]


# _____________________________________________________________________
# defs for API
def refreshCMCData():
    with urllib.request.urlopen(CMC_URL) as url:
        global s, CMCData
        s = url.read()
    CMCData = json.loads(s)


def getCoinUSDPrice(ticker):
    coin_info = next(coin for coin in CMCdata if coin[u'symbol'] == ticker)
    return (coin_info[u'price_usd'])


def getCoinBTCPrice(ticker):
    coin_info = next(coin for coin in CMCdata if coin[u'symbol'] == ticker)
    return (coin_info[u'price_btc'])


def getCoinID(ticker):
    coin_info = next(coin for coin in CMCdata if coin[u'symbol'] == ticker)
    return (coin_info[u'id'])


def getCoinTickerList(dataList):
    coinList = []
    for coinDetails in dataList:
        coinName = coinDetails[u'symbol']
        coinList += [coinName]
    return coinList


def getCoinNameList(dataList):
    coinNameList = []
    for coinDetails in dataList:
        coinName = coinDetails[u'id']
        coinNameList += [coinName]
    return coinNameList

coinTickerList = getCoinTickerList(CMCdata)
coinNameList = getCoinNameList(CMCdata)


def getCoinInfo(tickerOrName, data):
    if tickerOrName in coinTickerList:
        coin_info = next(coin for coin in data if coin[u'symbol'] == tickerOrName)
        return coin_info

    elif tickerOrName in coinNameList:
        coin_info = next(coin for coin in data if coin[u'id'] == tickerOrName)
        return coin_info


def getCoinInfoElement(ticker, aspect, data):
    coininfo = getCoinInfo(ticker, data)
    coininfoelement = coininfo[aspect]
    return coininfoelement


def getCoinTicker(id):
    coin_info = next(coin for coin in CMCdata if coin[u'id'] == id)
    return (coin_info[u'symbol'])


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
    if address[0] == "A" and len(address) > 10:
        baseLink = "https://neotracker.io/address/"
        completeLink = baseLink + address
        return [completeLink, "Neo"]

    # LTC
    elif address[0] == "L" and len(address) > 10:
        baseLink = "https://live.blockcypher.com/ltc/address/"
        completeLink = baseLink + address + "/"
        return [completeLink, "Litecoin"]

    # ETH
    elif address[0:2] == "0x" and len(address) > 10:
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



# ath prep______________________________________________________________________________________________________________________________
ATH_URL = 'https://athcoinindex.com/price/page/1'
wantedElements = [b'class="col_Rank">1</td>', b'data-currency="bitcoin"', b'alt="Bitcoin"', b'class="col_ATHPrice"', b'data-text="20089.000">$20,089.00</td>', b'class="col_ATHDate"', b'2017/12/17</td>', b'class="col_DaysSinceATH"', b'data-text="91">91</td>', b'class="col_ToATH"', b'data-text="169.75">169.75%</td>', b'class="col_FromATH"', b'data-text="-62.93">-62.93%</td>']
wantedIndexes = [1, 7, 13, 20, 24, 28, 35, 38]

dictionaryKeys = ["rank", "id", "name", "ath_price", "ath_date", "days_since_ath", "%_to_ath", "%_from_ath"]



# get ath data defs______________________________________________________________________________________________________________________________
def createSubList(mainlist, characterOne, characterTwo):
    newList = []
    index = 0
    firstCounter = True

    while index < (len(mainlist)):
        if mainlist[index] == characterOne:
            if mainlist[index + 1] == characterTwo:
                if firstCounter:
                    newList += [mainlist[0:index]]
                    firstCounter = False

                for subIndex in range(len(mainlist) - (index + 1)):

                    if subIndex != 0 and mainlist[index + subIndex] == characterOne:
                        nextIndex = index + subIndex
                        break

                    else:
                        nextIndex = len(mainlist)

                sublist = mainlist[index+2:nextIndex]
                newList += [(sublist)]
                index = nextIndex

            else:
                index += 1

        else:
            index += 1

    return newList



def fixReadableFirstLine(read):
    read.insert(0, createSubList(read[0], b'class="text-nowrap">', b'<tr>')[1])
    read.pop(1)
    return read



def getIndexForObject(list, object):
    for index in range(len(list)):
        if list[index] == object:
            return index
            break

        else:
            None



def createEssentialSubListsList(mainlist, indexlist):
    essentialmainlist = []

    for mainindex in range(len(mainlist)):
        essentialsublist = []
        corrector = 0
        counter = 0
        for subindex in indexlist:

            if counter == 3:
                i = 0
                while getStringBetweenCharacters(mainlist[mainindex][subindex + corrector].decode("utf-8"), ">", "<") == "":
                    i += 1
                    corrector = 2 * i

            essentialsublist += [mainlist[mainindex][subindex + corrector].decode("utf-8")]
            counter += 1

        essentialmainlist += [essentialsublist]

    return essentialmainlist



def filterATHSublist(originalsublist):
    filteredsublist = []

    for index in range(len(originalsublist)):
        if index in [0, 3, 5, 6, 7]:
            filteredsublist += [getStringBetweenCharacters(originalsublist[index], ">", "<")]
        elif index in [1, 2]:
            filteredsublist += [getStringBetweenCharacters(originalsublist[index], '"', '"')]
        else:
            filteredsublist += [originalsublist[4][:-5]]

    return filteredsublist



def createFilteredATHMainList(originalmainlist):
    filteredmainlist = []

    for sublist in originalmainlist:
        filteredmainlist += [filterATHSublist(sublist)]

    return filteredmainlist



def createdictlist(mainlist, dictkeys):
    mainlistdict = []

    for sublist in mainlist:
        subdictionary = {}

        for index in range(len(sublist)):
            subdictionary[dictkeys[index]] = sublist[index]

        mainlistdict += [subdictionary]

    return mainlistdict


def getReadableATHData(urlstring):
    request = urllib.request.Request(urlstring)
    response = urllib.request.urlopen(request)
    ath_data = response.read()
    ath_data_splitted = ath_data.split()
    ath_data_sublist = createSubList(ath_data_splitted, b'</tr>', b'<tr>')
    ath_data_fixed = fixReadableFirstLine(ath_data_sublist)
    essential_ath_data = createEssentialSubListsList(ath_data_fixed, wantedIndexes)
    filtered_ath_data = createFilteredATHMainList(essential_ath_data)
    dictionary_list = createdictlist(filtered_ath_data, dictionaryKeys)
    return dictionary_list



def getATHDataTopCoins(cmc_data, numberofcoins=200):
    base_url = 'https://athcoinindex.com/price/page/'
    amount_of_pages = int(numberofcoins / 50)
    main_dictionary_list = []

    for page_counter in range(amount_of_pages):
        main_dictionary_list += getReadableATHData(base_url + str(page_counter + 1))

    addSymbolToATHData(main_dictionary_list, cmc_data)

    return main_dictionary_list



def addSymbolToATHData(ath_data, cmc_data):
    for ath_coin_ditcionary in ath_data:
        ath_coin_name = ath_coin_ditcionary['id'].lower()

        for cmc_coin_dictionary in cmc_data:
            cmc_coin_name = removeSpaces(cmc_coin_dictionary['name'].lower())
            ath_coin_ditcionary['symbol'] = ''

            if ath_coin_name == cmc_coin_name:
                cmc_coin_symbol = cmc_coin_dictionary['symbol']
                ath_coin_ditcionary['symbol'] = cmc_coin_symbol
                break

    return ath_data



def refreshATHData():
    global ATHData
    ATHData = getATHDataTopCoins(CMCData, 200)



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



def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False



def makeLargeNumberReadable(originalstring):
    if isFloat(originalstring):
        intstring = str(int(float(originalstring) + 0.5))
        intstringlist = list(intstring)
        firstcommaindex = len(intstring) % 3
        amountofcommas = (len(intstring) // 3)

        if firstcommaindex == 0:
            amountofcommas -= 1

        for commaindex in range(amountofcommas):
            intstringlist.insert((-3 * (commaindex + 1)) - commaindex, ',')

        newstring = ''.join(intstringlist)
        return newstring

    else:
        return "Error converting large number to readable number."



def slideObjectInList(newObject, oldList, index=2):
    if newObject in oldList:
        None
    else:
        oldList.pop(index)
        oldList.insert(0, newObject)



def createQuickReplyWithGivenText(quickreplytext):
    quickreply = {
        "content_type": "text",
        "title": quickreplytext,
        "payload": quickreplytext,
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

            if index in [0, 1, 2]:
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
    randomObject = list[index]
    return randomObject



def removeSpaces(original_string):
    wordList = original_string.split()
    new_string = ''

    for word in wordList:
        new_string += word

    return new_string


def getStringBetweenCharacters(originalstring, firstchar, lastchar):
    try:
        start = originalstring.index(firstchar) + len(firstchar)
        end = originalstring.index(lastchar, start)
        return originalstring[start:end]
    except ValueError:
        return ""



def changeATHDateToString(ATHDate):
    ATHDateStringList = ATHDate.split("/")
    year = ATHDateStringList[0]
    day = ATHDateStringList[2]
    monthDigit = ATHDateStringList[1]

    if monthDigit == "01":
        month = "January"
    elif monthDigit == "02":
        month = "Febraury"
    elif monthDigit == "03":
        month = "March"
    elif monthDigit == "04":
        month = "April"
    elif monthDigit == "05":
        month = "May"
    elif monthDigit == "06":
        month = "June"
    elif monthDigit == "07":
        month = "July"
    elif monthDigit == "08":
        month = "August"
    elif monthDigit == "09":
        month = "September"
    elif monthDigit == "10":
        month = "October"
    elif monthDigit == "11":
        month = "November"
    else:
        month = "December"

    ATHDateSting = "{} {} {}".format(day, month, year)
    return ATHDateSting



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

                    refreshCMCData()
                    coinTickerList = getCoinTickerList(CMCdata)
                    coinNameList = getCoinNameList(CMCdata)

#                     # Portfolio usd
#                     if message_text in portfolioUSDTrigger:
#                         refreshQuickreplyList(message_text, quick_replies_list)
#                         botReply = getPortfolioUSDPrice(portfolioList)
#                         send_message(sender_id, "Your portfolio is valued at ${}.".format(botReply))


#                     # Portfolio btc
#                     elif message_text in portfolioBTCTrigger:
#                         refreshQuickreplyList(message_text, quick_replies_list)
#                         botReply = getPortfolioBTCPrice(portfolioList)
#                         send_message(sender_id, "Your portfolio is valued at {} BTC.".format(botReply))


                    # x coinName to usd, x coinName1 to coinName 2
                    elif (isFloat(sliceWords(message_text, 0, 1)) or isInt(
                            sliceWords(message_text, 0, 1))) and sliceWords(message_text, 2, 3) in ["to", "in"]:

                        if sliceWords(message_text, 3, 4) in ['usd', 'USD']:

                            if sliceWords(message_text, 1, 2) in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                botReply = coin1ToUSD(message_text)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems like that coin isn't included"
                                send_message(sender_id, botReply)

                        elif sliceWords(message_text, 1, 2) in coinTickerList and sliceWords(message_text, 3,
                                                                                             4) in coinTickerList:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            botReply = coin1ToCoin2(message_text)
                            send_message(sender_id, botReply)

                        elif sliceWords(message_text, 1, 2) in ['usd', 'USD']:
                            if sliceWords(message_text, 3, 4) in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                botReply = USDTocoin1(message_text)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems like that coin isn't included"
                                send_message(sender_id, botReply)

                        else:
                            botReply = "Sorry, it seems that a coin is not on coinmarketcap."
                            send_message(sender_id, botReply)


                    # coin info elements
                    elif sliceWords(message_text, 0, -1) in coinInfoCombinedTrigger:
                        coinTickerOrName = sliceWords(message_text, -1, None)

                        if sliceWords(message_text, 0, -1) in USDValueTrigger:

                            if coinTickerOrName.upper() in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                USDPrice = getCoinInfoElement(coinTickerOrName.upper(), "price_usd", CMCdata)
                                botReply = "${}".format(USDPrice)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in coinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                USDPrice = getCoinInfoElement(coinTickerOrName.lower(), "price_usd", CMCdata)
                                botReply = "${}".format(USDPrice)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1) in BTCValueTrigger:

                            if coinTickerOrName.upper() in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                BTCPrice = getCoinInfoElement(coinTickerOrName.upper(), "price_btc", CMCdata)
                                botReply = "{} BTC".format(BTCPrice)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in coinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                BTCPrice = getCoinInfoElement(coinTickerOrName.lower(), "price_btc", CMCdata)
                                botReply = "{} BTC".format(BTCPrice)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1) in supplyTrigger:

                            if coinTickerOrName.upper() in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                availableSupply = makeLargeNumberReadable(
                                    (getCoinInfoElement(coinTickerOrName.upper(), "available_supply", CMCdata)))
                                maxSupply = getCoinInfoElement(coinTickerOrName.upper(), "max_supply", CMCdata)

                                if maxSupply == None:
                                    maxSupply = "not available"

                                else:
                                    maxSupply = makeLargeNumberReadable(
                                        getCoinInfoElement(coinTickerOrName.upper(), "max_supply", CMCdata))

                                botReply = "The available supply of {} is {}. \nThe max supply is {}.".format(
                                    coinTickerOrName.upper(), availableSupply, maxSupply)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in coinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                availableSupply = makeLargeNumberReadable(
                                    (getCoinInfoElement(coinTickerOrName.lower(), "available_supply", CMCdata)))
                                maxSupply = getCoinInfoElement(coinTickerOrName.lower(), "max_supply")

                                if maxSupply == None:
                                    maxSupply = "not available"

                                else:
                                    maxSupply = makeLargeNumberReadable(
                                        getCoinInfoElement(coinTickerOrName.lower(), "max_supply", CMCdata))

                                coinTicker = getCoinInfoElement(coinTickerOrName.lower(), "symbol", CMCdata)
                                botReply = "The available supply of {} is {}. \nThe max supply is {}.".format(
                                    coinTicker, availableSupply, maxSupply)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1) in marketCapTrigger:

                            if coinTickerOrName.upper() in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                marketCap = makeLargeNumberReadable(
                                    getCoinInfoElement(coinTickerOrName.upper(), "market_cap_usd", CMCdata))
                                botReply = "The market cap of {} is ${}.".format(coinTickerOrName.upper(), marketCap)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in coinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                marketCap = makeLargeNumberReadable(
                                    getCoinInfoElement(coinTickerOrName.lower(), "market_cap_usd", CMCdata))
                                coinTicker = getCoinInfoElement(coinTickerOrName.lower(), "symbol")
                                botReply = "The market cap of {} is ${}.".format(coinTicker, marketCap)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1) in volumeTrigger:

                            if coinTickerOrName.upper() in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                volume = makeLargeNumberReadable(
                                    getCoinInfoElement(coinTickerOrName.upper(), "24h_volume_usd", CMCdata))
                                botReply = "The volume of {} is ${}.".format(coinTickerOrName.upper(), volume)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in coinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                volume = makeLargeNumberReadable(
                                    getCoinInfoElement(coinTickerOrName.lower(), "24h_volume_usd", CMCdata))
                                coinTicker = getCoinInfoElement(coinTickerOrName.lower(), "symbol", CMCdata)
                                botReply = "The volume of {} is ${}.".format(coinTicker, volume)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1) in rankTrigger:

                            if coinTickerOrName.upper() in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                rank = getCoinInfoElement(coinTickerOrName.upper(), "rank", CMCdata)
                                botReply = "{} is placed at rank number {}.".format(coinTickerOrName.upper(), rank)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in coinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                rank = getCoinInfoElement(coinTickerOrName.lower(), "rank", CMCdata)
                                coinTicker = getCoinInfoElement(coinTickerOrName.lower(), "symbol", CMCdata)
                                botReply = "{} is placed at rank number {}.".format(coinTicker, rank)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1) in changeTrigger:

                            if coinTickerOrName.upper() in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                change = getCoinInfoElement(coinTickerOrName.upper(), "percent_change_24h", CMCdata)
                                botReply = "{} changed {}% the past 24 hours.".format(coinTickerOrName.upper(), change)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in coinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                change = getCoinInfoElement(coinTickerOrName.lower(), "percent_change_24h", CMCdata)
                                coinTicker = getCoinInfoElement(coinTickerOrName.lower(), "symbol", CMCdata)
                                botReply = "{} changed {}% the past 24 hours.".format(coinTicker, change)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1) in specificChangeTrigger:

                            if coinTickerOrName.upper() in coinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                if sliceWords(message_text, 0, -1) in h24ChangeTrigger:
                                    change = getCoinInfoElement(coinTickerOrName.upper(), "percent_change_24h", CMCdata)
                                    botReply = "{} changed {}% the past 24 hours.".format(coinTickerOrName.upper(),
                                                                                          change)
                                    send_message(sender_id, botReply)

                                elif sliceWords(message_text, 0, -1) in h1ChangeTrigger:
                                    change = getCoinInfoElement(coinTickerOrName.upper(), "percent_change_1h", CMCdata)
                                    botReply = "{} changed {}% the past hour.".format(coinTickerOrName.upper(), change)
                                    send_message(sender_id, botReply)

                                elif sliceWords(message_text, 0, -1) in d7ChangeTrigger:
                                    change = getCoinInfoElement(coinTickerOrName.upper(), "percent_change_7d", CMCdata)
                                    botReply = "{} changed {}% the pas 7 days.".format(coinTickerOrName.upper(), change)
                                    send_message(sender_id, botReply)


                            elif coinTickerOrName.lower() in coinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                coinTicker = getCoinInfoElement(coinTickerOrName.lower(), "symbol", CMCdata)

                                if sliceWords(message_text, 0, -1) in h24ChangeTrigger:
                                    change = getCoinInfoElement(coinTickerOrName.lower(), "percent_change_24h", CMCdata)
                                    botReply = "{} changed {}% the past 24 hours.".format(coinTicker, change)
                                    send_message(sender_id, botReply)

                                elif sliceWords(message_text, 0, -1) in h1ChangeTrigger:
                                    change = getCoinInfoElement(coinTickerOrName.lower(), "percent_change_1h", CMCdata)
                                    botReply = "{} changed {}% the past hour.".format(coinTicker, change)
                                    send_message(sender_id, botReply)

                                elif sliceWords(message_text, 0, -1) in d7ChangeTrigger:
                                    change = getCoinInfoElement(coinTickerOrName.lower(), "percent_change_7d", CMCdata)
                                    botReply = "{} changed {}% the pas 7 days.".format(coinTicker, change)
                                    send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                    # ath data
                    elif sliceWords(message_text, 0, -1).lower() in coinATHInfoCombinedTrigger:
                        refreshATHData()
                        ATHCoinTickerList = getCoinTickerList(ATHData)
                        ATHCoinNameList = getCoinNameList(ATHData)
                        coinTickerOrName = sliceWords(message_text, -1, None)



                        if sliceWords(message_text, 0, -1).lower() in ATHPriceTrigger:

                            if coinTickerOrName.upper() in ATHCoinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                ATHPrice = getCoinInfoElement(coinTickerOrName.upper(), "ath_price", ATHData)
                                botReply = "The all time high of {} is {}.".format(coinTickerOrName, ATHPrice)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in ATHCoinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                ATHPrice = getCoinInfoElement(coinTickerOrName.lower(), "ath_price", ATHData)
                                botReply = "The all time high of {} is {}.".format(coinTickerOrName, ATHPrice)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1).lower() in ATHDateTrigger:

                            if coinTickerOrName.upper() in ATHCoinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                ATHDate = changeATHDateToString(getCoinInfoElement(coinTickerOrName.upper(), "ath_date", ATHData))
                                botReply = "On {} {} reached its all time high.".format(ATHDate, coinTickerOrName)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in ATHCoinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                ATHDate = changeATHDateToString(getCoinInfoElement(coinTickerOrName.lower(), "ath_date", ATHData))
                                botReply = "On {} {} reached its all time high.".format(ATHDate, coinTickerOrName)
                                send_message(sender_id, botReply)


                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1).lower() in daysSinceATHTrigger:

                            if coinTickerOrName.upper() in ATHCoinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                daysSinceATH = getCoinInfoElement(coinTickerOrName.upper(), "days_since_ath", ATHData)
                                botReply = "{} days ago {} had its all time high.".format(daysSinceATH, coinTickerOrName)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in ATHCoinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                daysSinceATH = getCoinInfoElement(coinTickerOrName.lower(), "days_since_ath", ATHData)
                                botReply = "{} days ago {} had its all time high.".format(daysSinceATH, coinTickerOrName)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1).lower() in percentageToATHTrigger:

                            if coinTickerOrName.upper() in ATHCoinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                percentageToATH = getCoinInfoElement(coinTickerOrName.upper(), "%_to_ath", ATHData)
                                botReply = "{} needs to go up by {} to reach its all time high".format(coinTickerOrName, percentageToATH)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in ATHCoinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                percentageToATH = getCoinInfoElement(coinTickerOrName.lower(), "%_to_ath", ATHData)
                                botReply = "{} needs to go up by {} to reach its all time high".format(coinTickerOrName, percentageToATH)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                send_message(sender_id, botReply)



                        elif sliceWords(message_text, 0, -1).lower() in percentageFromATHTrigger:

                            if coinTickerOrName.upper() in ATHCoinTickerList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                percentageFromATH = getCoinInfoElement(coinTickerOrName.upper(), "%_from_ath", ATHData)
                                botReply = "{} dropped {} under its all time high".format(coinTickerOrName, percentageFromATH)
                                send_message(sender_id, botReply)

                            elif coinTickerOrName.lower() in ATHCoinNameList:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                percentageFromATH = getCoinInfoElement(coinTickerOrName.lower(), "%_from_ath", ATHData)
                                botReply = "{} dropped {} under its all time high".format(coinTickerOrName, percentageFromATH)
                                send_message(sender_id, botReply)

                            else:
                                botReply = "Oops, it seems that I can't find this coin."
                                print(botReply)

                                
                                
                    # Price of coin
                    elif message_text.upper() in coinTickerList:
                        refreshQuickreplyList(message_text, quick_replies_list)
                        botReply = "${}".format(round(float(getCoinUSDPrice(message_text.upper())), 2))
                        send_message(sender_id, botReply)


                    # Price of coin lowercase
                    elif message_text in coinTickerList:
                        refreshQuickreplyList(message_text, quick_replies_list)
                        botReply = "${}".format(round(float(getCoinUSDPrice(message_text)), 2))
                        send_message(sender_id, botReply)


                    # USD price of coin 1
                    elif sliceWords(message_text, 0, len(message_text.split()) - 1) in coinUSDValueTrigger:
                        if sliceWords(message_text, -1, None) in coinTickerList:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            botReply = "${}".format(
                                round(float(getCoinUSDPrice(sliceWords(message_text, -1, None))), 2))
                            send_message(sender_id, botReply)

                        else:
                            botReply = "Oops, it seems like that coin isn't included"
                            send_message(sender_id, botReply)


                    # USD price of coin 2
                    elif sliceWords(message_text, 1, len(message_text.split())) in coinUSDValueTrigger:
                        if sliceWords(message_text, 0, 1) in coinTickerList:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            botReply = "${}".format(round(float(getCoinUSDPrice(sliceWords(message_text, 0, 1))), 2))
                            send_message(sender_id, botReply)

                        else:
                            botReply = "Oops, it seems like that coin isn't included"
                            send_message(sender_id, botReply)


                    # x coinname
                    elif len(message_text.split()) == 2 and isFloat(sliceWords(message_text, 0, 1)):

                        inputCoin = sliceWords(message_text, 1, 2)

                        if inputCoin in coinTickerList:
                            amountOfCoin = sliceWords(message_text, 0, 1)
                            totalUSDValue = float(getCoinUSDPrice(inputCoin)) * float(amountOfCoin)
                            botReply = "{} {} = ${}.".format(amountOfCoin, inputCoin, totalUSDValue)
                            send_message(sender_id, botReply)

                        elif inputCoin.upper() in coinTickerList:
                            amountOfCoin = sliceWords(message_text, 0, 1)
                            totalUSDValue = float(getCoinUSDPrice(inputCoin.upper())) * float(amountOfCoin)
                            botReply = "{} {} = ${}.".format(amountOfCoin, inputCoin.upper(), totalUSDValue)
                            send_message(sender_id, botReply)

                        else:
                            botReply = "Oops, it seems like that coin isn't included"
                            send_message(sender_id, botReply)


                    # Cmc of coin
                    elif sliceWords(message_text, 0, 2) in cmcLinkTriggerTwo:

                        if sliceWords(message_text, 2, 3) in coinTickerList:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            inputCoin = sliceWords(message_text, 2, 3)
                            botReply = "Here is the link to coinmarketcap of {}. \n \nLink: https://coinmarketcap.com/currencies/{}/".format(
                                inputCoin, getCoinID(inputCoin))
                            send_message(sender_id, botReply)

                        else:
                            botReply = "Oops, it seems like that coin isn't included"
                            send_message(sender_id, botReply)


                    # cmc coin
                    elif sliceWords(message_text, 0, 1) in cmcLinkTriggerOne:

                        if sliceWords(message_text, 1, 2) in coinTickerList:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            inputCoin = sliceWords(message_text, 1, 2)
                            botReply = "Here is the link to coinmarketcap of {}. \n \nLink: https://coinmarketcap.com/currencies/{}/".format(
                                inputCoin, getCoinID(inputCoin))
                            send_message(sender_id, botReply)

                        else:
                            botReply = "Oops, it seems like that coin isn't included"
                            send_message(sender_id, botReply)


                    # BTC price of coin 1
                    elif sliceWords(message_text, 0, len(message_text.split()) - 1) in coinBTCValueTrigger:
                        if sliceWords(message_text, -1, None) in coinTickerList:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            botReply = "{} BTC".format(
                                round(float(getCoinBTCPrice(sliceWords(message_text, -1, None))), 8))
                            send_message(sender_id, botReply)

                        else:
                            botReply = "Oops, it seems like that coin isn't included"
                            send_message(sender_id, botReply)


                    # BTC price of coin 2
                    elif sliceWords(message_text, 1, len(message_text.split())) in coinBTCValueTrigger:
                        if sliceWords(message_text, 0, 1) in coinTickerList:
                            refreshQuickreplyList(message_text, quick_replies_list)
                            botReply = "{} BTC".format(round(float(getCoinBTCPrice(sliceWords(message_text, 0, 1))), 8))
                            send_message(sender_id, botReply)

                        else:
                            botReply = "Oops, it seems like that coin isn't included"
                            send_message(sender_id, botReply)


#                     # all-in
#                     elif sliceWords(message_text, 0, 1) in allInTrigger:

#                         inputCoin = sliceWords(message_text, 1, 2)

#                         if inputCoin in coinTickerList:
#                             refreshQuickreplyList(message_text, quick_replies_list)
#                             allInList = allIn(portfolioList, inputCoin)
#                             numberOfCoins = allInList[0]
#                             portfolioValue = allInList[1]

#                             botReply = "If you would go all in on {}, you would have {} {}. Which is worth ${}".format(
#                                 inputCoin, numberOfCoins, inputCoin, portfolioValue)
#                             send_message(sender_id, botReply)

#                         else:
#                             botReply = "It seems that I can't find your coin, sorry."
#                             send_message(sender_id, botReply)


#                     # all in
#                     elif sliceWords(message_text, 0, 2) in allInTrigger:
#                         inputCoin = sliceWords(message_text, 2, 3)

#                         if inputCoin in coinTickerList:
#                             refreshQuickreplyList(message_text, quick_replies_list)
#                             allInList = allIn(portfolioList, inputCoin)
#                             numberOfCoins = allInList[0]
#                             portfolioValue = allInList[1]
#                             botReply = "If you would go all in on {}, you would have {} {}. Which is worth ${}".format(
#                                 inputCoin, numberOfCoins, inputCoin, portfolioValue)
#                             send_message(sender_id, botReply)

#                         else:
#                             botReply = "It seems that I can't find your coin, sorry."
#                             send_message(sender_id, botReply)


#                     # all in %
#                     elif "%" in list(message_text):
#                         inputCoin = sliceWords(message_text, -1, None)

#                         if inputCoin in coinTickerList:
#                             refreshQuickreplyList(message_text, quick_replies_list)
#                             percentageNumber = getStringBeforeCharacter(message_text, "%")
#                             allInPercentList = allInPercent(portfolioList, inputCoin, percentageNumber)
#                             numberOfCoins = allInPercentList[0]
#                             value = allInPercentList[1]
#                             botReply = "If you would allocate {}% of your portfolio to {}, you would have {} {}. Which is worth ${}".format(
#                                 percentageNumber, inputCoin, numberOfCoins, inputCoin, value)
#                             send_message(sender_id, botReply)

#                         else:
#                             botReply = "It seems that I can't find your coin, sorry."
#                             send_message(sender_id, botReply)


                    # address search
                    elif sliceWords(message_text, 0, len(message_text.split()) - 1) in addressTriger:
                        address = sliceWords(message_text, -1, None)
                        addressList = addressLinkGiver(address)

                        if len(addressList) == 2:
                            link = addressList[0]
                            addressType = addressList[1]

                            if addressType == "Ethereum":
                                refreshQuickreplyList(message_text, quick_replies_list)
                                botReply = "This is an {} address. \n \nHere is a link to the address: {}".format(
                                    addressType, link)
                                send_message(sender_id, botReply)

                            else:
                                refreshQuickreplyList(message_text, quick_replies_list)
                                botReply = "This is a {} address. \n \nHere is a link to the address: {}".format(
                                    addressType, link)
                                send_message(sender_id, botReply)

                        elif len(addressList) == 1:
                            botReply = addressList[0]
                            send_message(sender_id, botReply)


#                     # add quick reply
#                     elif sliceWords(message_text, 0, 3) in addQuickReplyTrigger:
#                         textOfQuickReply = sliceWords(message_text, 3, None)
#                         quickReply = createQuickReplyWithGivenText(textOfQuickReply)
#                         botReply = addQuickReply(quickReply, quick_replies_list)
#                         send_message(sender_id, botReply)


#                     # delete quick reply
#                     elif sliceWords(message_text, 0, 3) in deleteQuickReplyTrigger:
#                         textOfQuickReply = sliceWords(message_text, 3, None)
#                         quickReply = createQuickReplyWithGivenText(textOfQuickReply)
#                         botReply = deleteQuickReply(quickReply, quick_replies_list)
#                         send_message(sender_id, botReply)


                    # greet the bot
                    elif message_text in helloTrigger:
                        botReply = chooseRandomObjectFromList(helloOutput)
                        send_message(sender_id, botReply)


                    # donate
                    elif message_text in donateTriggers:
                        botReply = "Thanks for willing to donate! I currently accept BTC, LTC, ETH and NEO. Here are the addresses. \n\n-BTC: \n\n-LTC: \n\n-ETH: \n\n-NEO:"
                        send_message(sender_id, botReply)


                    # last answer
                    else:
                        send_message(sender_id, "Sorry I didn't get that or maybe your coin isn't on coinmarketcap.")

                # _____________________________________________________________________________

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
            "quick_replies": quick_replies_list
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
    app.run(host='0.0.0.0', port=port)
