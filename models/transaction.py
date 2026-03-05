from datetime import datetime


class Transaction:
    def __init__(self, transaction_type: str, coin_id: str, quantity: float, purchase_price: float, currency_type: str, timestamp: datetime):
        if not transaction_type.split():
            raise ValueError("Transaction type must be a valid string")
        if not coin_id.split():
            raise ValueError("Coin ID must be a valid string")
        if quantity <= 0:
            raise ValueError("Quantity must be a positive value")
        if purchase_price <= 0:
            raise ValueError("Purchase price must be a positive value")
        if not currency_type.split():
            raise ValueError("Currency type must be a valid string")
        if not isinstance(timestamp, datetime):
            raise ValueError("Timestamp must be a valid datetime instance")

        self._transaction_type = transaction_type
        self._coin_id = coin_id
        self._quantity = quantity
        self._purchase_price = purchase_price
        self._currency_type = currency_type
        self._timestamp = timestamp
    
    @property
    def transaction_type(self):
        return self._transaction_type
    
    @property
    def coin_id(self):
        return self._coin_id

    @property
    def quantity(self):
        return self._quantity
    
    @property
    def purchase_price(self):
        return self._purchase_price
    
    @property
    def currency_type(self):
        return self._currency_type

    @property
    def timestamp(self):
        return self._timestamp.isoformat()

    # String representation of a Transaction instance
    def __str__(self):
        return (
            f"{self._transaction_type.upper()} | "
            f"{self._coin_id} | "
            f"Qty: {self._quantity} | "
            f"@: {self._purchase_price} {self._currency_type} | "
            #f"{self._timestamp}"
        )

    # Returns a dictionary representation of the transaction for serialization (e.g., JSON storage)
    def to_dict(self) -> dict:
        return {
            "transaction_type": self._transaction_type,
            "coin_id": self._coin_id,
            "quantity": self._quantity,
            "purchase_price": self._purchase_price,
            "currency_type": self._currency_type,
            "timestamp": self._timestamp.isoformat()
        }