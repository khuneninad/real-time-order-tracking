import requests

def get_crypto_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=inr"
        return requests.get(url).json()['bitcoin']['inr']
    except:
        return 0

def get_weather():
    return "Clear"