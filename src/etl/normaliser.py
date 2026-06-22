import re

def normalize_year(value):
    if value is None:
        return None

    value = str(value).strip()

    match = re.search(r'20\d{2}', value)

    if match:
        return int(match.group())

    return None


def normalize_ticker(ticker):
    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")

    return ticker