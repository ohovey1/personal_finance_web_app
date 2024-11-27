from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, Any

from abc import ABC, abstractmethod

class Asset(ABC):
    def __init__(self, name: str, units: float, purchase_price: float):
        self.asset_id = None
        self.name = name
        self.units = units
        self.purchase_price = purchase_price
        self.current_price = purchase_price  # Initially same as purchase price until we add API

    @abstractmethod
    def calculate_value(self) -> float:
        pass

class Stock(Asset):
    def __init__(self, name: str, ticker: str, units: float, purchase_price: float):
        super().__init__(name, units, purchase_price)
        self.ticker = ticker

    def calculate_value(self) -> float:
        return self.units * self.current_price

class Crypto(Asset):
    def __init__(self, name: str, ticker: str, units: float, purchase_price: float):
        super().__init__(name, units, purchase_price)
        self.ticker = ticker

    def calculate_value(self) -> float:
        return self.units * self.current_price

class Cash(Asset):
    def __init__(self, amount: float):
        super().__init__("Cash", 1, amount)  # Cash is always 1 unit

    def calculate_value(self) -> float:
        return self.purchase_price  # For cash, price is the amount