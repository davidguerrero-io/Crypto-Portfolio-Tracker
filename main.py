import requests
from api import get_current_price
from portfolio import Portfolio

def display_menu():
    print("\n\n==================================================")
    print("     1 -> Buy")
    print("     2 -> Sell")
    print("     3 -> Display Assets")
    print("     4 -> Display Portfolio Value")
    print("     5 -> Exit")
    print("======================================================\n\n")

def main():
    print("Hello from crypto-tracker!")


    portfolio_name = input("Create a name for your crypto portfolio: ")
    owner_name = input("What is your full name?: ")
    currency_type = input("What currency type do you use? (Ex. USD, CAD, AUD, etc.): ")

    your_portfolio = Portfolio(portfolio_name, owner_name, currency_type)
    print("Crypto Portfolio successfully created\n\n")

    
    while True:
        display_menu()
        option = int(input("Enter an option (1, 2, 3, 4): "))

        if option == 1:

            crypto_coin = input("Enter crypto coin to purchase (Ex. bitcoin, ethereum, xrp): ")
            if not crypto_coin.split():
                print("Please enter a non-empty string")
                continue

            buy_amount = float(input("Enter amount to purchase (amount greater than 0): "))
            if buy_amount <= 0:
                print("Please enter a positive amount")
                continue

            try:
                your_portfolio.buy(crypto_coin, buy_amount)
                print(f"Successfully bought {buy_amount} {crypto_coin}")
            except Exception as e:
                print(f"Purchase action failed: {e}")
        elif option == 2:

            crypto_coin = input("Enter crypto coin to sell (Ex. bitcoin, ethereum, xrp): ")
            if not crypto_coin.split():
                print("Please enter a non-empty string")
                continue
            
            sell_amount = float(input("Enter amount to sell (amount greater than 0): "))
            if sell_amount <= 0:
                print("Please enter a positive amount")
                continue
            
            try:
                your_portfolio.sell(crypto_coin, sell_amount)
                print(f"Successfully sold {sell_amount} {crypto_coin}")
            except Exception as e:
                print(f"Sell action failed: {e}")
        elif option == 3:

            your_portfolio.display_assets()

        elif option == 4:
            print("Place holder here")
        
        elif option == 5:
            break

    print("Thank you for trying my Crypto Portfolio project! :)")
if __name__ == "__main__":
    main()
