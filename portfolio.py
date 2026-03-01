from asset import Asset
from api import get_current_price, is_valid_cache_data

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
        
        price = get_current_price(coin_id, self._currency_type)

        if coin_id not in self._assets:
            self._assets[coin_id] = Asset(coin_id, quantity, price)
        else:
            self._assets[coin_id].buy(quantity, price)

    # Sell a crypto asset
    def sell(self, coin_id: str, quantity: float) -> float:
        if coin_id not in self._assets:
            raise ValueError(f"Portfolio does not contain any {coin_id} to sell")

        if quantity <= 0:
            raise ValueError("Sell quantity must be positive")
        
        if quantity > self._assets[coin_id].quantity:
            raise ValueError("Sell quantity cannot exceed asset holding")
        
        return self._assets[coin_id].sell(quantity, get_current_price(coin_id, self._currency_type))

    # Displays all crypto assets currently owned/used to own
    def display_assets(self):
        if not self._assets:
            print("There are no assets in portfolio")
        for asset in self._assets.values():
           asset.display_info(self._currency_type)
    # Returns total portfolio value
    def total_value(self):
        total = 0
        for asset in self._assets.values():
            total += asset.owned_value(self._currency_type)
        return total