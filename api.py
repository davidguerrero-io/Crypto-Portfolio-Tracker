# contains API logic 
from dotenv import load_dotenv
import requests
import os

ROOT_API_URL = "https://api.coingecko.com/api/v3"


def get_api_key(): 
    # loading environment variables
    load_dotenv()
    api_key = os.getenv("coingecko_api_key")

    if not api_key:
        raise ValueError("Missing API key")
    
    return api_key


# Requires a crypto ID (slug) - Example -> "bitcoin", "ethereum". Returns the current price of the crypto asset.
def get_current_price(coin_id: str, currency_type: str) -> float:
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

    data = response.json()
    coin_data = data.get(coin_id)

    if not coin_data:
        raise ValueError(f"Invalid Coin ID: {coin_id}")

    coin_price = coin_data.get(currency_type.lower())
    if coin_price is None:
        raise ValueError(f"Invalid Currency Type: {currency_type} for {coin_id}")

    return coin_price
