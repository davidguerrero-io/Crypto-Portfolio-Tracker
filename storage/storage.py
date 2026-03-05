from models.portfolio import Portfolio
import json

# loads the serialized portfolio and converts it to a Portfolio Object
def load_portfolio(file_name: str) -> Portfolio:
    with open(file_name, "r") as read_file:
        serialized_portfolio = json.load(read_file) # converts file data into a python object (dictionary in this case) and stores it in serialized_portfolio
        portfolio_name = serialized_portfolio["portfolio_name"]
        owner_name = serialized_portfolio["owner"]
        currency_type = serialized_portfolio["currency_type"]
        assets = serialized_portfolio["assets"] # list of dictionaries
        transactions = serialized_portfolio["transactions"] # dictionary of dictionaries

        portfolio = Portfolio(portfolio_name, owner_name, currency_type)
        portfolio._load_assets_from_storage(assets)
        portfolio._load_transactions_from_storage(transactions)

        return portfolio


# Converts a Portfolio Object into JSON format and saves it to a file
def save_portfolio(portfolio: Portfolio, storage_file: str):
    with open(storage_file, "w") as write_file:
        json.dump(portfolio.to_dict(), write_file, indent=4)