from config import *
import requests
import hmac
import hashlib
import time
import logging
from forex_service import *
import datetime

endpoint = 'https://api.binance.com/api/v3/'
logging.basicConfig(level=logging.INFO)

def make_signed_request( method, endpoint, params=None):
    logging.info('Making A request...')
    timestamp = int(time.time() * 1000)
    query_params = params or {}
    logging.info('time', timestamp)
    query_params['timestamp'] = timestamp
    query_string = '&'.join([f"{key}={query_params[key]}" for key in query_params])
    signature = hmac.new(bytes(Binance_sceret_key, 'utf-8'), msg=bytes(query_string, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
    query_params['signature'] = signature

    headers = {"X-MBX-APIKEY": Binance_api_key}
    if method == 'GET':
        response = requests.get(endpoint, headers=headers, params=query_params)
    elif method == 'POST':
        response = requests.post(endpoint, headers=headers, params=query_params)
    else:
        raise ValueError("Invalid HTTP method")
    try:
        json_response = response.json()
        return json_response
    except ValueError as e:
        logging.error("Error decoding JSON on Trade:", e)
        return None

def get_symbol_price(symbol):
    try:
        url = f'{endpoint}ticker/price'
        response = requests.get(url, params={'symbol': symbol})
        response = response.json()
        if response['symbol'] == symbol:
            if 'price' in response:
                return float(response['price'])
        return None
    except ValueError as e:
        logging.error("Error decoding JSON on symbol price:", e)
        return None

def set_leverage(symbol):
    try:
        timestamp = int(time.time() * 1000)
        param = {
            "symbol": symbol,
            "leverage": 5,
            "timestamp": timestamp
        }
        query_string = '&'.join([f"{key}={param[key]}" for key in param])
        signature = hmac.new(bytes(Binance_sceret_key, 'utf-8'), msg=bytes(query_string, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
        param['signature'] = signature

        headers = {"X-MBX-APIKEY": Binance_api_key}

        response = requests.post(f'{endpoint}leverage', headers=headers, params=param)
        json_response = response.json()
        if json_response['symbol'] == symbol:
            return json_response
        return None
    except ValueError as e:
        logging.error("Error decoding JSON on leverage:", e)
        return None

def set_margin_type(symbol):
    try:
        timestamp = int(time.time() * 1000)
        param = {
            "symbol": symbol,
            "marginType": "ISOLATED",
            "timestamp": timestamp
        }
        query_string = '&'.join([f"{key}={param[key]}" for key in param])
        signature = hmac.new(bytes(Binance_sceret_key, 'utf-8'), msg=bytes(query_string, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
        param['signature'] = signature

        headers = {"X-MBX-APIKEY": Binance_api_key}

        response = requests.post(f'{endpoint}marginType', headers=headers, params=param)
        json_response = response.json()
        print('js', json_response)
        if json_response['code'] == 200 or json_response['code'] == -4046:
            return True
        return None
    except ValueError as e:
        logging.error("Error decoding JSON on Margin Type:", e)
        return None

async def place_orders_crypto(symbol, price1, price2, tp1, tp2, sl):
    logging.info('Signal processing...')
    try:
        current_price = get_symbol_price(symbol)
        price1 = float(price1.strip("$"))
        price2 = float(price2.strip("$"))

        # current_price_float = float(current_price)

        if current_price is not None and price1 <= current_price <= price2:
            quantity = round(10 / current_price, 1)
            params = {
                'symbol': symbol,
                'side': 'BUY',
                'type': 'MARKET',
                'quantity': quantity,
            }

            params_sl = {
                'symbol': symbol,
                'side': 'SELL',
                'type': 'STOP_MARKET',
                'quantity': quantity,
                'stopPrice': sl
            }

            params_tp1 = {
                'symbol': symbol,
                'side': 'SELL',
                'type': 'TAKE_PROFIT_MARKET',
                'quantity': round(10 / current_price)/2,
                'stopPrice': tp1
            }

            params_tp2 = {
                'symbol': symbol,
                'side': 'SELL',
                'type': 'TAKE_PROFIT_MARKET',
                'quantity': round(10 / current_price)/2,
                'stopPrice': tp2
            }

            # leverage = set_leverage(symbol)
            # if leverage is not None:
            #     print('lev', leverage)
            #     position = set_margin_type(symbol)
            #     print('po1', position)
            #     if position is not None:
            #         print('po', position)
            orderData = make_signed_request('POST', f'{endpoint}order', params=params)
            if orderData is not None:
                orderDataSl = make_signed_request('POST', f'{endpoint}order', params=params_sl)
                orderDataTp1 = make_signed_request('POST', f'{endpoint}order', params=params_tp1)
                orderDataTp2 = make_signed_request('POST', f'{endpoint}order', params=params_tp2)
                log_data = {
                    "result": {
                        "trade": orderData,
                        "stopLoss": orderDataSl,
                        "takeProfit1": orderDataTp1,
                        "takeProfit2": orderDataTp2
                    }
                }
                logging.info(f'Trade deatils: {str(log_data)}')
                trade={}
                current_datetime = datetime.datetime.now()
                trade['trade'] = log_data
                trade['date'] = current_datetime
                crypto_trade_details(trade)
        else:
            logging.info(f"Price not available or not within the desired range for {symbol}")
    except Exception as e:
        logging.error(f"An error occurred on Place order: {e}")
