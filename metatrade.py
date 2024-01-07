from config import *
import requests
from forex_service import *
import datetime

endpoint = f'https://mt-client-api-v1.singapore-b.agiliumtrade.ai/users/current/accounts/{octa_account_id}/'

def ticker_price(url, headers):
    price_response = requests.get(url, headers=headers)
    return price_response.json()

def get_trade_type(direction, price, price_data):
    if direction == 'buy' or direction == 'buu':
        if price < price_data['ask']:
            return 'ORDER_TYPE_BUY_LIMIT'
        elif price > price_data['ask']:
            return 'ORDER_TYPE_BUY_STOP'
    elif direction == 'sell':
        if price < price_data['bid']:
            return 'ORDER_TYPE_SELL_STOP'
        elif price > price_data['bid']:
            return 'ORDER_TYPE_SELL_LIMIT'

async def place_order(symbol, direction, price, target, sl, tp2, tp3, is_gold):
    try:
        times = 3 if is_gold else 1

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
        price_data = ticker_price(get_price_url, headers)
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
        trade_body["actionType"] = get_trade_type(direction, price, price_data)
        
        # Place trade order
        for i in range(times):

            if i == 1:
                trade_body['takeProfit'] = tp2
                trade_body['trailingStopLoss'] = {"distance": { "distance": 20, "units": "RELATIVE_PIPS" }}
            if i == 2:
                trade_body['takeProfit'] = tp3
                trade_body['trailingStopLoss'] = {"distance": { "distance": 20, "units": "RELATIVE_PIPS" }}

            trade_response = requests.post(take_trade_url, headers=headers, json=trade_body)
            trade_result = trade_response.json()
            print(i, trade_result)

            while trade_result.get('message') == 'Invalid stops':
                price_data = ticker_price(get_price_url, headers)
                trade_body["actionType"] = get_trade_type(direction, price, price_data)
                trade_response = requests.post(take_trade_url, headers=headers, json=trade_body)
                trade_result = trade_response.json()

            if trade_result['message'] == 'No error returned' :
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
