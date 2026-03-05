from .asset import Asset
from services.api import get_current_price, is_valid_cache_data
from .transaction import Transaction
from utils.helpers import generate_number
from datetime import datetime
from cli.console import print_transaction_table, print_asset_table

class Portfolio:
    def __init__(self, portfolio_name: str, owner_name: str, currency_type: str):
        if not portfolio_name.strip():
            raise ValueError("Portfolio name cannot be an empty string")
        if not owner_name.strip():
            raise ValueError("Owner's name cannot be an empty string")
        if not currency_type.strip():
            raise ValueError("Currency type cannot be an empty string")

        self._portfolio_name = portfolio_name
        self._owner_name = owner_name
        self._currency_type = currency_type
        # {"coin_id": Asset}
        self._assets = {}
        # {transaction_id: Transaction}
        self._transactions = {}

    # Property getters

    @property
    def portfolio_name(self):
        return self._portfolio_name

    @property
    def owner_name(self):
        return self._owner_name

    @property
    def currency_type(self):
        return self._currency_type

    @property
    def total_profit(self):
        pass

    
    # Property setters

    @portfolio_name.setter
    def portfolio_name(self, new_portfolio_name: str):
        if not new_portfolio_name.strip():
            raise ValueError("Portfolio name cannot be an empty string.")

        self._portfolio_name = new_portfolio_name


    # Buy a crypto asset
    def buy(self, coin_id: str, quantity: float):
        if quantity <= 0:
            raise ValueError("Buy quantity cannot be zero or a negative value")
        
        price = get_current_price(coin_id, self._currency_type)
        time_now = datetime.now()

        if coin_id not in self._assets:
            self._assets[coin_id] = Asset(coin_id, quantity, price)
        else:
            self._assets[coin_id].buy(quantity, price)

        # Record transaction and store it in a Transaction object (IN PROGRESS)
        transaction = Transaction("BUY", coin_id, quantity, price, self._currency_type, time_now)
        # Generate a unique transaction ID
        transaction_id = generate_number(100000000, 1000000000000)
        while transaction_id in self._transactions:
            transaction_id = generate_number(100000000, 1000000000000)
        
        # Store transaction ID and transaction object
        self._transactions[transaction_id] = transaction


    # Sell a crypto asset
    def sell(self, coin_id: str, quantity: float) -> float:
        if coin_id not in self._assets:
            raise ValueError(f"Portfolio does not contain any {coin_id} to sell")

        if quantity <= 0:
            raise ValueError("Sell quantity must be positive")
        
        if quantity > self._assets[coin_id].quantity:
            raise ValueError("Sell quantity cannot exceed asset holding")

        
        current_price = get_current_price(coin_id, self._currency_type)
        time_now = datetime.now()

        # Record transaction and store it (IN PROGRESS)
        transaction = Transaction("SELL", coin_id, quantity, current_price, self._currency_type, time_now)
        # Generate a unique transaction ID
        transaction_id = generate_number(100000000, 1000000000000)
        while transaction_id in self._transactions:
            transaction_id = generate_number(100000000, 1000000000000)
        
        # Store transaction ID and transaction object
        self._transactions[transaction_id] = transaction

        return self._assets[coin_id].sell(quantity, current_price)

    # Displays all crypto assets currently owned/used to own
    def display_assets(self):
        if not self._assets:
            print("There are no assets in portfolio")
        print_asset_table(self._assets, self._currency_type)
    # Returns total portfolio value
    def total_value(self):
        total = 0
        for asset in self._assets.values():
            total += asset.owned_value(self._currency_type)
        return total

    # Returns a dictionary representation of the Portfolio for serialization (e.g., JSON storage).
    def to_dict(self) -> dict:
        return {
            "portfolio_name": self._portfolio_name,
            "owner": self._owner_name,
            "currency_type": self._currency_type,
            "assets": [asset.to_dict() for asset in self._assets.values()],
            "transactions": {
                transaction_id: transaction.to_dict() for transaction_id, transaction in self._transactions.items()
            }
        }


    # Displays all transactions
    def show_transactions(self):
        if not self._transactions:
            print("No transactions found")
            return
        print_transaction_table(self._transactions)

        

    # internal functions (SHOULD NOT BE USED PUBLICLY)
    
    # loads all assets from storage file into _assets attribute
    def _load_assets_from_storage(self, assets: list):
        for asset_dict in assets:
            coin_id = asset_dict["coin_id"]
            quantity = asset_dict["quantity"]
            purchase_price = asset_dict["purchase_price"]
            self._assets[coin_id] = Asset(coin_id, quantity, purchase_price)

    # loads all transactions from storage file into _transactions attribute
    def _load_transactions_from_storage(self, transactions: dict):
        for transaction_id, transaction_dict in transactions.items():
            transaction_type = transaction_dict["transaction_type"]
            coin_id = transaction_dict["coin_id"]
            quantity = transaction_dict["quantity"]
            purchase_price = transaction_dict["purchase_price"]
            currency_type = transaction_dict["currency_type"]
            timestamp = datetime.fromisoformat(transaction_dict["timestamp"])

            self._transactions[transaction_id] = Transaction(transaction_type, coin_id, quantity, purchase_price, currency_type, timestamp)