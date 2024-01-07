from telethon import TelegramClient, events
import re
from config import *
from metatrade import place_order
from forex_helper import *
from bin import place_orders_crypto
from helper import *

client = TelegramClient('session_read', api_id, api_hash)

print('Listening...')

@client.on(events.NewMessage(chats=-1001447871772))
async def my_event_handler(event):
    statement = event.raw_text
    if check_statement_forex(statement):
        print('new from MMFX')
        data = capture_trade_info(statement)
        symbol = data['symbol']
        price = data['price']
        sl = data['stop_loss']
        direction = data['direction']
        target = data['take_profit_1']
        print(symbol, target)
        await place_order(symbol, direction, price, target, sl, None,None, False)

@client.on(events.NewMessage(chats=-4026560717))
async def my_event_handler(event):
    statement = event.raw_text
    if check_statement_crypto(statement):
        print('Got New crypto Signal...')
        data = extract_data(statement)
        coin = data['coin']
        price1 = data['price']['price1']
        price2 =data['price']['price2']
        tp1 = data['targets']['tp1']
        tp2 = data['targets']['tp2']
        sl = data['stop_loss']
        print(tp1, sl)
        await place_orders_crypto(coin, price1, price2, tp1, tp2, sl)
    elif check_statement_forex(statement):
        print('new from MMFX')
        data = capture_trade_info(statement)
        symbol = data['symbol']
        price = data['price']
        sl = data['stop_loss']
        direction = data['direction']
        target = data['take_profit_1']
        print(symbol, target)
        await place_order(symbol, direction, price, target, sl, None,None, False)
    elif check_statement_gold(statement):
        print('Signal from XAUUSD')
        data = capture_trade_xauusd(statement)
        symbol = 'XAUUSD'
        price = data['price']
        sl = data['stop_loss']
        direction = data['direction']
        tp1 = data['take_profit_1']
        tp2 = data['take_profit_2']
        tp3 = data['take_profit_3']
        await place_order(symbol, direction, price, tp1, sl, tp2, tp3, True)

@client.on(events.NewMessage(chats=-1001459607851))
async def my_event_handler(event):
    statement = event.raw_text
    if check_statement_crypto(statement):
        print('Got New crypto Signal...')
        data = extract_data(statement)
        coin = data['coin']
        price1 = data['price']['price1']
        price2 =data['price']['price2']
        tp1 = data['targets']['tp1']
        tp2 = data['targets']['tp2']
        sl = data['stop_loss']
        print(tp1, sl)
        await place_orders_crypto(coin, price1, price2, tp1, tp2, sl)

@client.on(events.NewMessage(chats=-1001464335892))
async def my_event_handler(event):
    statement = event.raw_text
    if check_statement_gold(statement):
        print('Signal from XAUUSD')
        data = capture_trade_xauusd(statement)
        symbol = 'XAUUSD'
        price = data['price']
        sl = data['stop_loss']
        direction = data['direction']
        tp1 = data['take_profit_1']
        tp2 = data['take_profit_2']
        tp3 = data['take_profit_3']
        await place_order(symbol, direction, price, tp1, sl, tp2, tp3, True)


client.start()
client.run_until_disconnected()
