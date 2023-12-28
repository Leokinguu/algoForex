from telethon import TelegramClient, events
import re
from config import *
from metatrade import place_order
from bin import place_orders_crypto
from datetime import datetime, timedelta

client = TelegramClient('session_read', api_id, api_hash)

def check_target(target, sl, price, direction):
    if ':' in target and target == '1:1':
        price = float(price)
        sl = float(sl)
        direction = direction.lower()
        if direction == 'buy' or direction == 'buu':
            dif = price - sl
            newTraget = price + dif
            return round(newTraget, 5)
        if direction == 'sell':
            dif = sl - price
            newTraget = price - dif
            return round(newTraget, 5)
    if ',' in target:
        return float(target.split(',')[0])

def check_statement2(statement):
    if re.search(r'\b(?:GOLD)', statement, re.IGNORECASE):
        return False
    else:
        regex = r'\b(?:SL|TP1|TP2|GOLD|BUY|SELL)'
        match = re.search(regex, statement,re.IGNORECASE)
        if match:
            return True
        else:
            return False

def capture_symbol(statement):
    is_limit = re.findall(r'limit|stop', statement, re.IGNORECASE)
    if is_limit:
        match = re.findall(r"(?:limit|stop)\s+(\w+)", statement, re.IGNORECASE)
        return match[0].upper()
    else:
        regex = r"\b(?:SELL|BUY)\s+(\w+)"
        match = re.findall(regex, statement, re.IGNORECASE)
        if match:
            if match[0].lower() == 'gold':
                return 'XAUUSD'
            else:
                return match[0].upper()
        else:
            return None
    
def capture_price(statement):
    regex = r"(?:limit|stop|sell|buy)\s+\w+\D+(\d+.\d+)"
    match = re.findall(regex, statement, re.IGNORECASE)
    if match:
        if "-" in match[0]:
            new = match[0].split("-")[0]
            return float(new)
        else:
            print(match[0])
            return float(match[0])
    else:
        return None

def capture_sl(statement):
    regex = r"\b(?:SL:|stop loss:)\s(\d+.\d+)"
    match = re.findall(regex, statement, re.IGNORECASE)
    if match:
        return float(match[0])
    else:
        regex = r"\b(?:SL:|stop loss:)(\d+.\d+)"
        match = re.findall(regex, statement, re.IGNORECASE)
        return float(match[0])
    
def capture_tp1(statement):
    regex = r"\b(?:TP1:)\s(\d+.\d+)"
    match = re.findall(regex, statement, re.IGNORECASE)
    if match:
        return float(match[0])
    else:
        regex = r"\b(?:TP1:)(\d+.\d+)"
        match = re.findall(regex, statement, re.IGNORECASE)
        return float(match[0])
    
def capture_tp2(statement):
    regex = r"\b(?:TP2:)\s(\d+.\d+)"
    match = re.findall(regex, statement, re.IGNORECASE)
    if match:
        return float(match[0])
    else:
        regex = r"\b(?:TP2:)(\d+.\d+)"
        match = re.findall(regex, statement, re.IGNORECASE)
        return float(match[0])


def capture_direction(statement):
    regex = r"SELL|BUY"
    match = re.findall(regex, statement, re.IGNORECASE)
    if match:
        return match[0]
    else:
        return None

print('Listening...')

@client.on(events.NewMessage(chats=-1001447871772))
async def my_event_handler(event):
    statement = event.raw_text
    if check_statement2(statement):
        print('new from MMFX')
        symbol = capture_symbol(statement)
        price = capture_price(statement)
        sl = capture_sl(statement)
        direction = capture_direction(statement)
        target = capture_tp1(statement)
        print(symbol, target)
        await place_order(symbol, direction, price, target, sl)

@client.on(events.NewMessage(chats=-4026560717))
async def my_event_handler(event):
    statement = event.raw_text
    splited = statement.split()
    if (splited[0] == "#SIGNAL"):
        print('Got New Signal...')
        coin = splited[1].strip("#")
        price1 = splited[5]
        price2 =splited [7]
        target = splited[10].strip('$')
        sl = splited[18].strip('$')
        print(target, sl)
        await place_orders_crypto(coin, 'BUY', price1, price2, target, sl)
    if check_statement2(statement):
        print('new from MMFX')
        symbol = capture_symbol(statement)
        price = capture_price(statement)
        sl = capture_sl(statement)
        direction = capture_direction(statement)
        target = capture_tp1(statement)
        print(symbol, target)
        await place_order(symbol, direction, price, target, sl)

@client.on(events.NewMessage(chats=-1001459607851))
async def my_event_handler(event):
    statement = event.raw_text
    splited = statement.split()
    if (splited[0] == "#SIGNAL"):
        print('Got New Signal...')
        coin = splited[1].strip("#")
        price1 = splited[5]
        price2 =splited [7]
        target = splited[10].strip('$')
        sl = splited[18].strip('$')
        print(target, sl)
        await place_orders_crypto(coin, 'BUY', price1, price2, target, sl)

client.start()
client.run_until_disconnected()
