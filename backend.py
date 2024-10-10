from abc import ABC, abstractmethod
from datetime import date

# User class
class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.logged_in = False
        self.portfolio = Portfolio()  # type: Portfolio

    def register(self):
        pass

    def login(self, email, password):
        pass

    def update_profile(self, new_name, new_email):
        pass

    def delete_account(self):
        pass

    def view_portfolio(self):
        pass

    def view_asset_portfolio(self, asset):
        pass

    def add_asset_to_portfolio(self, asset_type, *args, **kwargs):
        asset = AssetFactory.create_asset(asset_type, *args, **kwargs)
        self.portfolio.add_asset(asset)

    def remove_asset_from_portfolio(self, asset_id):
        pass

    def get_portfolio_summary(self):
        pass

# Portfolio class
class Portfolio:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset):
        self.assets.append(asset)

    def remove_asset(self, asset_id):
        pass

    def calculate_value(self):
        pass

    def get_asset_breakdown(self):
        pass

    def get_asset_breakdown_by_type(self, asset_type):
        pass


# Abstract Asset class
class Asset(ABC):
    def __init__(self, asset_id, name, value, purchase_date, user_id, owner):
        self.asset_id = asset_id
        self.name = name
        self.value = value
        self.purchase_date = purchase_date
        self.user_id = user_id
        self.owner = owner

    @abstractmethod
    def calculate_value(self):
        pass

    def update_value(self, new_value):
        pass


# Concrete Stock class
class Stock(Asset):
    def __init__(self, asset_id, name, value, purchase_date, user_id, owner, ticker, shares, purchase_price):
        super().__init__(asset_id, name, value, purchase_date, user_id, owner)
        self.ticker = ticker
        self.shares = shares
        self.purchase_price = purchase_price

    def calculate_value(self):
        pass


# Concrete RealEstate class
class RealEstate(Asset):
    def __init__(self, asset_id, name, value, purchase_date, user_id, owner, location, purchase_price, current_value):
        super().__init__(asset_id, name, value, purchase_date, user_id, owner)
        self.location = location
        self.purchase_price = purchase_price
        self.current_value = current_value

    def calculate_value(self):
        pass


# Concrete Crypto class
class Crypto(Asset):
    def __init__(self, asset_id, name, value, purchase_date, user_id, owner, ticker, units_held, purchase_price):
        super().__init__(asset_id, name, value, purchase_date, user_id, owner)
        self.ticker = ticker
        self.units_held = units_held
        self.purchase_price = purchase_price

    def calculate_value(self):
        pass


# Concrete Cash class
class Cash(Asset):
    def __init__(self, asset_id, name, value, purchase_date, user_id, owner, currency, location):
        super().__init__(asset_id, name, value, purchase_date, user_id, owner)
        self.currency = currency
        self.location = location

    def calculate_value(self):
        pass

# AssetFactory class for easy Asset creation
class AssetFactory:
    @staticmethod
    def create_asset(asset_type, *args, **kwargs):
        if asset_type == "stock":
            return Stock(*args, **kwargs)
        elif asset_type == "realestate":
            return RealEstate(*args, **kwargs)
        elif asset_type == "crypto":
            return Crypto(*args, **kwargs)
        elif asset_type == "cash":
            return Cash(*args, **kwargs)
        else:
            raise ValueError(f"Unknown asset type: {asset_type}")


# Abstract Account class
class Account(ABC):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.holdings = []

    @abstractmethod
    def calculate_value(self):
        pass

    @abstractmethod
    def add_asset(self, asset):
        pass

    @abstractmethod
    def remove_asset(self, asset):
        pass


# Concrete BankAccount class
class BankAccount(Account):
    def __init__(self, name, value, account_number, balance, account_holder, bank_name):
        super().__init__(name, value)
        self.account_number = account_number
        self.balance = balance
        self.account_holder = account_holder
        self.bank_name = bank_name

    def get_balance(self):
        pass

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass


# CheckingAccount class, inheriting from BankAccount
class CheckingAccount(BankAccount):
    def __init__(self, name, value, account_number, balance, account_holder, bank_name, overdraft_limit):
        super().__init__(name, value, account_number, balance, account_holder, bank_name)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        pass


# SavingsAccount class, inheriting from BankAccount
class SavingsAccount(BankAccount):
    def __init__(self, name, value, account_number, balance, account_holder, bank_name, interest_rate):
        super().__init__(name, value, account_number, balance, account_holder, bank_name)
        self.interest_rate = interest_rate

    def apply_interest(self):
        pass


# Concrete StockAccount class
class StockAccount(Account):
    def __init__(self, name, value, account_number):
        super().__init__(name, value)
        self.account_number = account_number

    def calculate_value(self):
        pass

    def add_asset(self, asset):
        pass

    def remove_asset(self, asset):
        pass


# Concrete RealEstateAccount class
class RealEstateAccount(Account):
    def __init__(self, name, value, account_type):
        super().__init__(name, value)
        self.account_type = account_type

    def calculate_value(self):
        pass

    def add_asset(self, asset):
        pass

    def remove_asset(self, asset):
        pass


# Concrete CryptoAccount class
class CryptoAccount(Account):
    def __init__(self, name, value, account_number):
        super().__init__(name, value)
        self.account_number = account_number

    def calculate_value(self):
        pass

    def add_asset(self, asset):
        pass

    def remove_asset(self, asset):
        pass


# Singleton DB Connection class, 
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # TODO: add initialization code here
        return cls._instance
