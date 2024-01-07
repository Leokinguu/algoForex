import re

def check_statement_forex(statement):
    if re.search(r'\b(?:GOLD|XAUUSD)', statement, re.IGNORECASE):
        return False
    else:
        regex = r'\b(?:SL|TP1|TP2|GOLD|SELL)'
        match = re.search(regex, statement,re.IGNORECASE)
        if match:
            return True
        else:
            return False

def capture_trade_info(statement):
    trade_info = {}

    # Capture Symbol
    is_limit = re.findall(r'limit|stop', statement, re.IGNORECASE)
    if is_limit:
        match = re.findall(r"(?:limit|stop)\s+(\w+)", statement, re.IGNORECASE)
        trade_info['symbol'] = match[0].upper() if match else None
    else:
        regex = r"\b(?:SELL|BUY)\s+(\w+)"
        match = re.findall(regex, statement, re.IGNORECASE)
        if match:
            trade_info['symbol'] = 'XAUUSD' if match[0].lower() == 'gold' else match[0].upper()
        else:
            trade_info['symbol'] = None

    # Capture Price
    price_regex = r"(?:limit|stop|sell|buy)\s+\w+\D+(\d+\.\d+|\d+)"
    price_match = re.findall(price_regex, statement, re.IGNORECASE)
    if price_match:
        price = float(price_match[0].split("-")[0]) if "-" in price_match[0] else float(price_match[0])
        trade_info['price'] = price
    else:
        trade_info['price'] = None

    # Capture Stop Loss
    sl_regex = r"\b(?:SL:|stop loss:)\s(\d+\.\d+|\d+)"
    sl_match = re.findall(sl_regex, statement, re.IGNORECASE)
    if not sl_match:
        sl_regex = r"\b(?:SL:|stop loss:)(\d+\.\d+|\d+)"
        sl_match = re.findall(tp1_regex, statement, re.IGNORECASE)
    trade_info['stop_loss'] = float(sl_match[0]) if sl_match else None

    # Capture Take Profit 1
    tp1_regex = r"\b(?:TP1:)\s(\d+\.\d+|\d+)"
    tp1_match = re.findall(tp1_regex, statement, re.IGNORECASE)
    if not tp1_match:
        tp1_regex = r"\b(?:TP1:)(\d+\.\d+|\d+)"
        tp1_match = re.findall(tp1_regex, statement, re.IGNORECASE)
    trade_info['take_profit_1'] = float(tp1_match[0]) if tp1_match else None

    # Capture Take Profit 2
    tp2_regex = r"\b(?:TP2:)\s(\d+\.\d+|\d+)"
    tp2_match = re.findall(tp2_regex, statement, re.IGNORECASE)
    if not tp2_match:
        tp2_regex = r"\b(?:TP2:)(\d+\.\d+|\d+)"
        tp2_match = re.findall(tp1_regex, statement, re.IGNORECASE)
    trade_info['take_profit_2'] = float(tp2_match[0]) if tp2_match else None

    # Capture Direction
    direction_regex = r"SELL|BUY"
    direction_match = re.findall(direction_regex, statement, re.IGNORECASE)
    trade_info['direction'] = direction_match[0] if direction_match else None

    return trade_info

def check_statement_gold(statement):
    regex = r'\b(?:XAUUSD)'
    match = re.search(regex, statement,re.IGNORECASE)
    if match:
        return True
    else:
        return False
    
def capture_trade_xauusd(statement):
    trade_info = {}

    # Capture Price
    price_regex = r"(?:limit|stop|sell|buy)\s+(\d+\.\d+|\d+)"
    price_match = re.findall(price_regex, statement, re.IGNORECASE)
    if price_match:
        price = float(price_match[0])
        trade_info['price'] = price
    else:
        trade_info['price'] = None

    # Capture Stop Loss
    sl_regex = r"\b(?:SL:|stop loss:)\s+(\d+\.\d+|\d+)"
    sl_match = re.findall(sl_regex, statement, re.IGNORECASE)
    trade_info['stop_loss'] = float(sl_match[0]) if sl_match else None

    # Capture Take Profit 1
    tp1_regex = r"\b(?:TP1:)\s+(\d+\.\d+|\d+)"
    tp1_match = re.findall(tp1_regex, statement, re.IGNORECASE)
    trade_info['take_profit_1'] = float(tp1_match[0]) if tp1_match else None

    # Capture Take Profit 2
    tp2_regex = r"\b(?:TP2:)\s+(\d+\.\d+|\d+)"
    tp2_match = re.findall(tp2_regex, statement, re.IGNORECASE)
    trade_info['take_profit_2'] = float(tp2_match[0]) if tp2_match else None

    # Capture Take Profit 3
    tp3_regex = r"\b(?:TP3:)\s+(\d+\.\d+|\d+)"
    tp3_match = re.findall(tp3_regex, statement, re.IGNORECASE)
    trade_info['take_profit_3'] = float(tp3_match[0]) if tp3_match else None

    # Capture Direction
    direction_regex = r"SELL|BUY"
    direction_match = re.findall(direction_regex, statement, re.IGNORECASE)
    trade_info['direction'] = direction_match[0] if direction_match else None

    return trade_info
