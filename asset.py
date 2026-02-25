from api import get_current_price
# Later version implementations: 
# - A transaction list that tracks all transaction types of the asset (buy/sell)

class Asset:
    def __init__(self, coin_id: str, quantity: float, purchase_price: float):
        self._coin_id = coin_id
        self._quantity = quantity
        self._purchase_price = purchase_price

    @property
    def quantity(self):
        if self._quantity < 0:
            raise ValueError("Quantity cannot be negative")
        return self._quantity

    @property
    def coin_id(self):
        return self._coin_id
    
    @property
    def purchase_price(self) -> float:
        if self._purchase_price < 0:
            raise ValueError("Purchase price cannot be negative")
        return self._purchase_price

    @purchase_price.setter
    def purchase_price(self, new_purchase_price: float) -> float:
        if new_purchase_price < 0:
            raise ValueError("Purchase price cannot be negative")
        self._purchase_price = new_purchase_price

    # Calculates new weighted average purchase price
    def _calculate_weighted_average(self, amount: float, new_purchase_price: float) -> float:
        total_cost = (self._quantity * self._purchase_price) + (amount * new_purchase_price)
        return total_cost / (self._quantity + amount)

    # Calculates profit made so far (if profit is negative, it's a loss duh!)
    def profit(self, current_asset_price: float) -> float:
        if current_asset_price < 0:
            raise ValueError(f"{self._coin_id} current price cannot be negative")
        return (current_asset_price - self._purchase_price) * self._quantity
    
    # Updates asset quantity and purchase price
    def buy(self, quantity: float, buy_price: float):
        if quantity <= 0:
            raise ValueError("Purchase amount must be positive.")
        self._purchase_price = self._calculate_weighted_average(quantity, buy_price)
        self._quantity += quantity
    
    # Updates asset quanttiy and returns realized profit (or loss) made on the sell
    def sell(self, quantity: float, sell_price: float) -> float:
        if quantity <= 0:
            raise ValueError("Sell amount must be positive.")
        if quantity > self._quantity:
            raise ValueError(f"Sell amount exceeds {self._coin_id} holdings")

        profit = (sell_price - self._purchase_price) * quantity
        self._quantity -= quantity
        return profit

    


    