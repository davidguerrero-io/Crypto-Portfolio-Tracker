import requests
from api import get_current_price

def main():
    print("Hello from crypto-tracker!")
    kaspa_price = get_current_price("kaspa", "USD")
    print(f"Bitcoin price: ${kaspa_price}")


if __name__ == "__main__":
    main()
