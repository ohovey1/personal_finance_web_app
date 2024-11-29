from abc import ABC, abstractmethod
from typing import Dict, Optional
from ..database.db_connection import DatabaseConnection
from .asset import Asset, Stock, Crypto, Cash

class Account(ABC):
    def __init__(self, name: str):
        self.account_id = None
        self.name = name
        self.holdings: Dict[int, Asset] = {}
        self.account_type = None  # Set by subclasses
        self.db = DatabaseConnection()

    def add_asset(self, asset: Asset) -> Optional[int]:
        """Add asset to account and save to database"""
        query = """
        INSERT INTO Assets (account_id, name, asset_type, units, purchase_price, current_price)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING asset_id;
        """
        result = self.db.execute_query(
            query,
            (self.account_id, asset.name, asset.__class__.__name__.lower(),
             asset.units, asset.purchase_price, asset.current_price)
        )
        if result:
            asset_id = result[0]['asset_id']
            self.holdings[asset_id] = asset
            return asset_id
        return None
    
    def remove_asset(self, asset_id: int) -> bool:
        """Remove asset from account and db"""
        query = "DELETE FROM Assets WHERE asset_id = %s AND account_id = %s;"
        try:
            self.db.execute_query(query, (asset_id, self.account_id))
            if asset_id in self.holdings:
                del self.holdings[asset_id]
            return True
        except Exception as e:
            print(f"Error removing asset: {str(e)}")
            return False

    def get_assets(self):
        """Load assets from database"""
        query = "SELECT * FROM Assets WHERE account_id = %s;"
        results = self.db.execute_query(query, (self.account_id,))
        
        if results:
            for result in results:
                # Create appropriate asset based on type
                if result['asset_type'] == 'stock':
                    asset = Stock(
                        name=result['name'],
                        ticker=result.get('ticker', ''),  # Will add ticker to DB later
                        units=float(result['units']),
                        purchase_price=float(result['purchase_price'])
                    )
                elif result['asset_type'] == 'crypto':
                    asset = Crypto(
                        name=result['name'],
                        ticker=result.get('ticker', ''),
                        units=float(result['units']),
                        purchase_price=float(result['purchase_price'])
                    )
                elif result['asset_type'] == 'cash':
                    asset = Cash(amount=float(result['purchase_price']))
                
                asset.current_price = float(result['current_price'])
                self.holdings[result['asset_id']] = asset

    @abstractmethod
    def calculate_total_value(self) -> float:
        pass

class StockAccount(Account):
    def __init__(self, name: str):
        super().__init__(name)
        self.account_type = 'stock'

    def calculate_total_value(self) -> float:
        return sum(asset.calculate_value() for asset in self.holdings.values())

class CryptoAccount(Account):
    def __init__(self, name: str):
        super().__init__(name)
        self.account_type = 'crypto'

    def calculate_total_value(self) -> float:
        return sum(asset.calculate_value() for asset in self.holdings.values())

class BankAccount(Account):
    def __init__(self, name: str):
        super().__init__(name)
        self.account_type = 'bank'

    def calculate_total_value(self) -> float:
        return sum(asset.calculate_value() for asset in self.holdings.values())