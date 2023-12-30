import re

def check_statement_crypto(statement):
    regex = r"#SIGNAL"
    match = re.search(regex, statement,re.IGNORECASE)
    print('matc', match)
    if match:
        return True
    else:
        return False
    
def extract_data(statement):
    data = {}

    # Extracting coin symbol
    coin_regex = r"(?:#SIGNAL)\s+\W(\w+)"
    coin_match = re.search(coin_regex, statement, re.IGNORECASE)
    data['coin'] = coin_match.group(1) if coin_match else None

    # Extracting Price
    price_regex = r"(?:Between)\s+(\d+.\d+|\d+)\D+(\d+.\d+|\d+)"
    price_match = re.search(price_regex, statement, re.IGNORECASE)
    if price_match:
        data['price'] = {"price1": price_match.group(1), "price2": price_match.group(2)}
    else:
        data['price'] = None

    # Extracting targets
    targets_regex = r"(?:Targets)\s+\D+(\d+\.\d+|\d+)\D+(\d+\.\d+|\d+)"
    targets_match = re.search(targets_regex, statement, re.IGNORECASE)
    if targets_match:
        data['targets'] = {"tp1": targets_match.group(1), "tp2": targets_match.group(2)}
    else:
        data['targets'] = None

    # Extracting stop loss
    sl_regex = r"(?:Stop Loss)\D+(\d+\.\d+|\d+)"
    sl_match = re.search(sl_regex, statement, re.IGNORECASE)
    data['stop_loss'] = sl_match.group(1) if sl_match else None

    return data