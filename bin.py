from config import *
import requests
import hmac
import hashlib
import time

endpoint = 'https://fapi.binance.com/fapi/v1/'

def make_signed_request( method, endpoint, params=None):
    print('Making A request...')
    timestamp = int(time.time() * 1000)
    query_params = params or {}
    print('time', timestamp)
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
        print("Error decoding JSON:", e)
        return None

def get_symbol_price(symbol):
    url = f'{endpoint}ticker/price'
    response = requests.get(url, params={'symbol': symbol})
    response = response.json()
    if response['symbol'] == symbol:
        if 'price' in response:
            return float(response['price'])
    return None

async def place_orders_crypto( symbol, transType, price1, price2, tp, sl):
    print('Signal processing...')
    current_price = get_symbol_price(symbol)
    price1 = float(price1.strip("$"))
    price2 = float(price2.strip("$"))

    # current_price_float = float(current_price)

    print('price: ',current_price)
    if current_price is not None and price1 <= current_price <= price2:
        quantity = round(10 / current_price, 1)
        params = {
            'symbol': symbol,
            'side': transType,
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

        params_tp = {
            'symbol': symbol,
            'side': 'SELL',
            'type': 'TAKE_PROFIT_MARKET',
            'quantity': quantity,
            'stopPrice': tp
        }

        orderData = make_signed_request('POST', f'{endpoint}order', params=params)
        if orderData is not None:
            orderDataSl = make_signed_request('POST', f'{endpoint}order', params=params_sl)
            orderDataTp = make_signed_request('POST', f'{endpoint}order', params=params_tp)
    else:
        print(f"Price not available or not within the desired range for {symbol}")
