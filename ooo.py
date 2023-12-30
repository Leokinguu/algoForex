import re

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
    trade_info['stop_loss'] = float(sl_match[0]) if sl_match else None

    # Capture Take Profit 1
    tp1_regex = r"\b(?:TP1:)\s(\d+\.\d+|\d+)"
    tp1_match = re.findall(tp1_regex, statement, re.IGNORECASE)
    trade_info['take_profit_1'] = float(tp1_match[0]) if tp1_match else None

    # Capture Take Profit 2
    tp2_regex = r"\b(?:TP2:)\s(\d+\.\d+|\d+)"
    tp2_match = re.findall(tp2_regex, statement, re.IGNORECASE)
    trade_info['take_profit_2'] = float(tp2_match[0]) if tp2_match else None

    # Capture Direction
    direction_regex = r"SELL|BUY"
    direction_match = re.findall(direction_regex, statement, re.IGNORECASE)
    trade_info['direction'] = direction_match[0] if direction_match else None

    return trade_info

# Example usage:
statement = """Small lots! High risk‼️

SELL EURNZD  @ 1.7530
❌SL: 1.7550
✅TP1: 1.7490
✅TP2: 1.7470
✅TP3: 1.7370

Total R:R = 1:3

Do Take Note
Keep to proper risk management as we teach in the Team. Never risk more than 10% on a setup. Multiple TPs do not mean multiple positions, divide your total position and take the partial profits per TP. This is not Financial Advice, but our views of the current market."""
result = capture_trade_info(statement)
print(result)
