from asset import Asset
from api import get_current_price

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

        if coin_id not in self._assets:
            new_asset = Asset(coin_id, quantity, get_current_price(coin_id, self._currency_type))
            self._assets[coin_id] = new_asset
            return
        
        self._assets[coin_id].buy(quantity, get_current_price(coin_id, self._currency_type))

    # Sell a crypto asset
    def sell(self, coin_id: str, quantity: float):
        if coin_id not in self._assets:
            raise ValueError(f"Portfolio does not contain any {coin_id} to sell")

        if quantity <= 0:
            raise ValueError("Sell quantity must be positive")
        
        if quantity > self._assets[coin_id].quantity:
            raise ValueError("Sell quantity cannot exceed asset holding")
        
        self._assets[coin_id].sell(quantity, get_current_price(coin_id, self._currency_type))