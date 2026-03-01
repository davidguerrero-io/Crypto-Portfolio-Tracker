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

    # String representation of a Transaction instance
    def __str__(self):
        return (
            f"{self._transaction_type.upper()} | "
            f"{self._coin_id} | "
            f"Qty: {self._quantity} | "
            f"@: {self._purchase_price} {self._currency_type} | "
            f"{self._timestamp}"
        )