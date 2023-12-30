from config import *
import requests
from forex_service import *
import datetime

endpoint = f'https://mt-client-api-v1.singapore-b.agiliumtrade.ai/users/current/accounts/{octa_account_id}/'

async def place_order(symbol, direction, price, target, sl):
    try:
        # Convert inputs to appropriate types
        direction = direction.lower()
        price = float(price)
        symbol = f'{symbol}'
        sl = float(sl)
        
        # Prepare API endpoint URLs
        get_price_url = f'{endpoint}symbols/{symbol}/current-price'
        take_trade_url = f'{endpoint}trade'
        
        # Set headers for API requests
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "auth-token": octa_token_id
        }
        
        # Fetch current price data
        price_response = requests.get(get_price_url, headers=headers)
        price_data = price_response.json()
        print('mt pice', price_data)

        # Prepare trade parameters
        lot = 0.01
        trade_body = {
            "symbol": symbol,
            "openPrice": price,
            "volume": lot,
            "takeProfit": target,
            "stopLoss": sl
        }
        
        # Determine action type based on direction and price
        if direction == 'buy' or direction == 'buu':
            if price < price_data['ask']:
                trade_body["actionType"] = 'ORDER_TYPE_BUY_LIMIT'
            elif price > price_data['ask']:
                trade_body["actionType"] = 'ORDER_TYPE_BUY_STOP'
        elif direction == 'sell':
            if price < price_data['bid']:
                trade_body["actionType"] = 'ORDER_TYPE_SELL_STOP'
            elif price > price_data['bid']:
                trade_body["actionType"] = 'ORDER_TYPE_SELL_LIMIT'
        
        # Place trade order
        print('tarde',trade_body["actionType"])
        trade_response = requests.post(take_trade_url, headers=headers, json=trade_body)
        trade_result = trade_response.json()

        while trade_result.get('message') == 'Invalid stops':
           trade_response = requests.post(take_trade_url, headers=headers, json=trade_body)
           trade_result = trade_response.json()

        if trade_result:
            print('Trade Successful', trade_result)
            trade ={}
            current_datetime = datetime.datetime.now()

            trade['trade'] = trade_result
            trade['date'] = current_datetime
            forex_trade_details(trade)
        else:
            print('Trade Error', trade_result)
            trade ={}
            current_datetime = datetime.datetime.now()

            trade['trade'] = trade_result
            trade['date'] = current_datetime
            forex_trade_details(trade)
        #add_trade(trade_result)

    except Exception as e:
        print(f"An error occurred: {e}")
