from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, Any
from ..database.db_connection import DatabaseConnection

class Asset(ABC):
    def __init__(self, name: str, purchase_date: date = None):
        self.asset_id = None  # Will be set when saved to database
        self.name = name
        self.purchase_date = purchase_date or date.today()
        self.db = DatabaseConnection()

    @abstractmethod
    def calculate_value(self) -> float:
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return asset-specific data for database storage"""
        pass

class Stock(Asset):
    def __init__(self, name: str, ticker: str, shares: float, purchase_price: float, purchase_date: date = None):
        super().__init__(name, purchase_date)
        self.ticker = ticker
        self.shares = shares
        self.purchase_price = purchase_price

    def calculate_value(self) -> float:
        # TODO: Implement real-time stock price fetching
        return self.shares * self.purchase_price

    def get_metadata(self) -> Dict[str, Any]:
        return {
            'ticker': self.ticker,
            'shares': self.shares,
            'purchase_price': self.purchase_price
        }

class RealEstate(Asset):
    def __init__(self, name: str, address: str, purchase_price: float, 
                 current_value: float, purchase_date: date = None):
        super().__init__(name, purchase_date)
        self.address = address
        self.purchase_price = purchase_price
        self.current_value = current_value

    def calculate_value(self) -> float:
        # TODO: Implement real estate value API integration
        return self.current_value

    def get_metadata(self) -> Dict[str, Any]:
        return {
            'address': self.address,
            'purchase_price': self.purchase_price,
            'current_value': self.current_value
        }

class Crypto(Asset):
    def __init__(self, name: str, ticker: str, units_held: float, 
                 purchase_price: float, purchase_date: date = None):
        super().__init__(name, purchase_date)
        self.ticker = ticker
        self.units_held = units_held
        self.purchase_price = purchase_price

    def calculate_value(self) -> float:
        # TODO: Implement crypto price API integration
        return self.units_held * self.purchase_price

    def get_metadata(self) -> Dict[str, Any]:
        return {
            'ticker': self.ticker,
            'units_held': self.units_held,
            'purchase_price': self.purchase_price
        }

class Cash(Asset):
    def __init__(self, amount: float, name: str = "Cash"):
        super().__init__(name)
        self.amount = amount

    def calculate_value(self) -> float:
        return self.amount

    def get_metadata(self) -> Dict[str, Any]:
        return {
            'amount': self.amount
        }

    def update_amount(self, new_amount: float):
        """Update cash amount and database record"""
        self.amount = new_amount
        if self.asset_id:
            query = """
            UPDATE Assets 
            SET current_value = %s,
                metadata = jsonb_set(metadata, '{type_specific_data}', %s)
            WHERE asset_id = %s;
            """
            self.db.execute_query(
                query, 
                (self.amount, {'amount': self.amount}, self.asset_id)
            )