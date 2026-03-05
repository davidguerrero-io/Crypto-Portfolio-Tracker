# contains API logic 
from dotenv import load_dotenv
import requests
import os
import time

ROOT_API_URL = "https://api.coingecko.com/api/v3"

# stores coin prices. Prices are fetched from here if data is valid. Data is only valid for up to 30 seconds. Data is updated if invalid (api request)
_cache = {

}

# Amount of time cache data is considered valid before being discarded and updated (in seconds)
CACHE_TTL = 30 # 30 seconds

def get_current_time():
    return time.time()

def is_valid_cache_data(coin_id: str):
    if coin_id not in _cache:
        return False
    price, timestamp = next(iter(_cache[coin_id].items()))
    return get_current_time() - timestamp < CACHE_TTL

def get_api_key(): 
    # loading environment variables
    load_dotenv()
    api_key = os.getenv("coingecko_api_key")

    if not api_key:
        raise ValueError("Missing API key")
    
    return api_key

# Requires a crypto ID (slug) - Example -> "bitcoin", "ethereum". Returns the current price of the crypto asset via API fetch.
def _fetch_price_from_api(coin_id: str, currency_type: str) -> float:
    price_url = f"{ROOT_API_URL}/simple/price"
    api_key = get_api_key()

    params = {
        "ids": coin_id,
        "vs_currencies": currency_type.lower()
    }

    headers = {
        "Accept": "application/json",
        "x-cg-demo-api-key": api_key
    }

    response = requests.get(price_url, params=params, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise RuntimeError(f"Failed to fetch {coin_id} price from CoinGecko.")

    # data -> {coin_id: {currency_type, price}}
    data = response.json()
    coin_data = data.get(coin_id)

    if not coin_data:
        raise ValueError(f"Invalid Coin ID: {coin_id}")

    coin_price = coin_data.get(currency_type.lower())
    if coin_price is None:
        raise ValueError(f"Invalid Currency Type: {currency_type} for {coin_id}")

    _cache[coin_id] = {coin_price: get_current_time()}

    return coin_price

# Performs a API fetch if stored crypto price is longer than 30 seconds or first time fetching it. 
def get_current_price(coin_id: str, currency_type: str) -> float:
    # If crypto coin price was fetched in the last 30 seconds, return price from cache
    if coin_id in _cache:
       if is_valid_cache_data(coin_id):
            price, last_fetched_time_seconds = next(iter(_cache[coin_id].items()))
            return price

    # Otherwise fetch from CoinGecko API
    
    price = _fetch_price_from_api(coin_id, currency_type)

    # Update price in cache
    _cache[coin_id] = {price: get_current_time()}
    return price
