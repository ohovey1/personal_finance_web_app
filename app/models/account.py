from abc import ABC, abstractmethod
from ..database.db_connection import DatabaseConnection
from typing import Dict, Any

class Account(ABC):
    def __init__(self, name: str, institution: str = None):
        self.account_id = None
        self.name = name
        self.institution = institution
        self.account_type = None  # Will be set by child classes
        self.holdings: Dict[int, Any] = {}  # Dictionary of assets
        self.db = DatabaseConnection()

    @abstractmethod
    def calculate_value(self):
        pass

    @abstractmethod
    def add_asset(self, asset):
        pass

    @abstractmethod
    def remove_asset(self, asset_id):
        pass

    def save_asset(self, asset):
        """Save asset to database"""

        query = """
        INSERT INTO Assets (account_id, name, asset_type, purchase_price, 
                          current_value, purchase_date, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING asset_id;
        """

        metadata = {
            'type_specific_data': asset.get_metadata()  # New method needed in asset classes
        }
        result = self.db.execute_query(
            query,
            (self.account_id, asset.name, asset.__class__.__name__.lower(),
             asset.purchase_price, asset.calculate_value(), 
             asset.purchase_date, metadata)
        )
        if result:
            return result[0]['asset_id']
        return None

    def get_assets(self):
        """Get all assets for this account from database"""

        query = "SELECT * FROM Assets WHERE account_id = %s;"

        results = self.db.execute_query(query, (self.account_id,))
        self.holdings = {}
        if results:
            from ..factories.asset_factory import AssetFactory
            for result in results:
                asset = AssetFactory.create_asset(
                    result['asset_type'],
                    result['name'],
                    **result['metadata']['type_specific_data']
                )
                self.holdings[result['asset_id']] = asset
        return self.holdings

    def view_account(self):
        """Display account details"""
        self.get_assets()  # Refresh assets from database
        print(f"Account Name: {self.name}")
        print(f"Account Type: {self.account_type}")
        print(f"Total Value: {self.calculate_value()}")
        print("\n")
        for asset_id, asset in self.holdings.items():
            print(f"Asset ID: {asset_id}")
            print(f"Asset Name: {asset.name}")
            print(f"Purchase Date: {asset.purchase_date}")
            print(f"Value: {asset.calculate_value()}")
            print("\n")

class StockAccount(Account):
    def __init__(self, name: str, brokerage: str):
        super().__init__(name, brokerage)
        self.account_type = "stock"
        self.brokerage = brokerage

    def calculate_value(self):
        total_value = 0
        assets = self.get_assets()  # Refresh from database
        for asset in assets.values():
            total_value += asset.calculate_value()
        return total_value

    def add_asset(self, asset):
        if not asset.__class__.__name__.lower() == "stock":
            raise ValueError("Can only add stock assets to stock account")
        asset_id = self.save_asset(asset)
        if asset_id:
            self.holdings[asset_id] = asset
            return asset_id
        return None

    def remove_asset(self, asset_id):
        query = "DELETE FROM Assets WHERE asset_id = %s AND account_id = %s;"
        self.db.execute_query(query, (asset_id, self.account_id))
        if asset_id in self.holdings:
            del self.holdings[asset_id]

class RealEstateAccount(Account):
    def __init__(self, name: str):
        super().__init__(name)
        self.account_type = "realestate"

    def calculate_value(self):
        total_value = 0
        assets = self.get_assets()
        for asset in assets.values():
            total_value += asset.calculate_value()
        return total_value

    def add_asset(self, asset):
        if not asset.__class__.__name__.lower() == "realestate":
            raise ValueError("Can only add real estate assets to real estate account")
        asset_id = self.save_asset(asset)
        if asset_id:
            self.holdings[asset_id] = asset
            return asset_id
        return None

    def remove_asset(self, asset_id):
        query = "DELETE FROM Assets WHERE asset_id = %s AND account_id = %s;"
        self.db.execute_query(query, (asset_id, self.account_id))
        if asset_id in self.holdings:
            del self.holdings[asset_id]

class CryptoAccount(Account):
    def __init__(self, name: str, exchange: str):
        super().__init__(name, exchange)
        self.account_type = "crypto"
        self.exchange = exchange

    def calculate_value(self):
        total_value = 0
        assets = self.get_assets()
        for asset in assets.values():
            total_value += asset.calculate_value()
        return total_value

    def add_asset(self, asset):
        if not asset.__class__.__name__.lower() == "crypto":
            raise ValueError("Can only add crypto assets to crypto account")
        asset_id = self.save_asset(asset)
        if asset_id:
            self.holdings[asset_id] = asset
            return asset_id
        return None

    def remove_asset(self, asset_id):
        query = "DELETE FROM Assets WHERE asset_id = %s AND account_id = %s;"
        self.db.execute_query(query, (asset_id, self.account_id))
        if asset_id in self.holdings:
            del self.holdings[asset_id]

class BankAccount(Account):
    def __init__(self, name: str, bank_name: str):
        super().__init__(name, bank_name)
        self.account_type = "bank"
        self.bank_name = bank_name
        self.balance = 0

    def calculate_value(self):
        return self.balance

    def add_asset(self, asset):
        if not asset.__class__.__name__.lower() == "cash":
            raise ValueError("Bank accounts can only hold cash assets")
        asset_id = self.save_asset(asset)
        if asset_id:
            self.holdings[asset_id] = asset
            self.balance = asset.amount
            return asset_id
        return None

    def remove_asset(self, asset_id):
        query = "DELETE FROM Assets WHERE asset_id = %s AND account_id = %s;"
        self.db.execute_query(query, (asset_id, self.account_id))
        if asset_id in self.holdings:
            del self.holdings[asset_id]
            self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        # Update cash asset in database

        query = """
        UPDATE Assets 
        SET current_value = %s 
        WHERE account_id = %s AND asset_type = 'cash';
        """

        self.db.execute_query(query, (self.balance, self.account_id))
        if self.holdings:
            asset_id = list(self.holdings.keys())[0]
            self.holdings[asset_id].amount = self.balance

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            # Update cash asset in database
            query = """
            UPDATE Assets 
            SET current_value = %s 
            WHERE account_id = %s AND asset_type = 'cash';
            """
            self.db.execute_query(query, (self.balance, self.account_id))

            if self.holdings:
                asset_id = list(self.holdings.keys())[0]
                self.holdings[asset_id].amount = self.balance

            return True
        
        print("Insufficient funds.")
        return False

class CheckingAccount(BankAccount):
    def __init__(self, name: str, bank_name: str, overdraft_limit: float):
        super().__init__(name, bank_name)
        self.account_type = "checking"
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            # Update cash asset in database
            query = """
            UPDATE Assets 
            SET current_value = %s 
            WHERE account_id = %s AND asset_type = 'cash';
            """
            self.db.execute_query(query, (self.balance, self.account_id))

            if self.holdings:
                asset_id = list(self.holdings.keys())[0]
                self.holdings[asset_id].amount = self.balance
            return True
        
        print("Insufficient funds.")
        return False

class SavingsAccount(BankAccount):
    def __init__(self, name: str, bank_name: str, interest_rate: float):
        super().__init__(name, bank_name)
        self.account_type = "savings"
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance = self.balance * (1 + self.interest_rate)
        
        # Update cash asset in database
        query = """
        UPDATE Assets 
        SET current_value = %s 
        WHERE account_id = %s AND asset_type = 'cash';
        """

        self.db.execute_query(query, (self.balance, self.account_id))
        if self.holdings:
            asset_id = list(self.holdings.keys())[0]
            self.holdings[asset_id].amount = self.balance