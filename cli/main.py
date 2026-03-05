import requests
from services.api import get_current_price
from models.portfolio import Portfolio
from storage.storage import load_portfolio, save_portfolio
from .console import print_error, print_success, print_warning, print_header, print_menu_table
from json import JSONDecodeError
import sys


def main():

    print_header("Welcome to Crypto Portfolio Tracker!")

    try:
        your_portfolio = load_portfolio("storage/portfolio_json.txt")
    except (FileNotFoundError, JSONDecodeError):
        print_error("Portfolio storage file does not exist or is empty. Please create a new portfolio")
        portfolio_name = input("Create a name for your crypto portfolio: ")
        owner_name = input("What is your full name?: ")
        currency_type = input("What currency type do you use? (Ex. USD, CAD, AUD, etc.): ")
        your_portfolio = Portfolio(portfolio_name, owner_name, currency_type)
        print("Crypto Portfolio successfully created\n\n")
    except KeyError:
        print_error("Storage file corrupted x_x... aborting program")
        sys.exit(0)

    
    while True:

        print_menu_table()

        try:
            option = int(input("Enter an option: "))
            if option not in range(1, 7):
                print_warning("User option must be between 1..6")
                continue
        except ValueError:
            print_warning("User option must be a valid integer")
            continue

        if option == 1:
            crypto_coin = input("Enter crypto coin to purchase (Ex. bitcoin, ethereum, xrp): ")
            if not crypto_coin.split():
                print_warning("Please enter a non-empty string")
                continue

            buy_amount = float(input("Enter amount to purchase (amount greater than 0): "))
            if buy_amount <= 0:
                print_warning("Please enter a positive amount")
                continue

            try:
                your_portfolio.buy(crypto_coin, buy_amount)
                print_success(f"Successfully bought {buy_amount} {crypto_coin}")
            except Exception as e:
                print_error(f"Purchase action failed: {e}")
        elif option == 2:
            crypto_coin = input("Enter crypto coin to sell (Ex. bitcoin, ethereum, xrp): ")
            if not crypto_coin.split():
                print_warning("Please enter a non-empty string")
                continue
            
            sell_amount = float(input("Enter amount to sell (amount greater than 0): "))
            if sell_amount <= 0:
                print_warning("Please enter a positive amount")
                continue
            
            try:
                your_portfolio.sell(crypto_coin, sell_amount)
                print_success(f"Successfully sold {sell_amount} {crypto_coin}")
            except Exception as e:
                print_error(f"Sell action failed: {e}")
        elif option == 3:
            your_portfolio.display_assets()
        elif option == 4:
            your_portfolio.show_transactions()
        elif option == 5:
            print(f"\nPortfolio Value: {your_portfolio.total_value()} {your_portfolio.currency_type.upper()}\n")
            
        elif option == 6:
            save_portfolio(your_portfolio, "storage/portfolio_json.txt")
            break

    print_header("Thank you for trying my Crypto Portfolio project! :)")
if __name__ == "__main__":
    main()
