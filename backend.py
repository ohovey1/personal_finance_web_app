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
        self.portfolio = Portfolio()  # Composition: User owns a Portfolio. Stores Account objects which store Assets

    def register(self):
        pass

    def login(self, email, password):
        pass

    def update_profile(self, new_name, new_email):
        pass

    def delete_account(self):
        pass

    def create_account(self, account_type, *args, **kwargs):
        account = AccountFactory.create_account(account_type, *args, **kwargs)
        self.portfolio.add_account(account)
    
    def add_asset_to_account(self, account_type, asset_type, *args, **kwargs):
        account = self.portfolio.get_account(account_type)
        if account:
            asset = AssetFactory.create_asset(asset_type, *args, **kwargs)
            account.add_asset(asset)

    def get_portfolio_summary(self):
        pass


# Portfolio class
class Portfolio:
    def __init__(self):
        self.accounts = {}  # Using a dictionary to store accounts by type

    def add_account(self, account):
        self.accounts[account.__class__.__name__] = account

    def get_account(self, account_type):
        return self.accounts.get(account_type)

    def calculate_total_value(self):
        pass

    def get_asset_breakdown(self):
        pass

# Abstract Account class
class Account(ABC):
    def __init__(self, name):
        self.name = name
        self.holdings = []  # List of assets held by this account

    @abstractmethod
    def calculate_value(self):
        pass

    @abstractmethod
    def add_asset(self, asset):
        pass

    @abstractmethod
    def remove_asset(self, asset):
        pass


# BankAccount class
class BankAccount(Account):
    def __init__(self, name, account_number, balance, bank_name):
        super().__init__(name)
        self.account_number = account_number
        self.balance = balance
        self.bank_name = bank_name

    def calculate_value(self):
        # The total value of a BankAccount could be the balance.
        return self.balance

    def add_asset(self, asset):
        self.holdings.append(asset)

    def remove_asset(self, asset):
        self.holdings.remove(asset)

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount


# CheckingAccount class
class CheckingAccount(BankAccount):
    def __init__(self, name, account_number, balance, bank_name, overdraft_limit):
        super().__init__(name, account_number, balance, bank_name)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= self.balance + self.overdraft_limit:
            self.balance -= amount


# SavingsAccount class
class SavingsAccount(BankAccount):
    def __init__(self, name, account_number, balance, bank_name, interest_rate):
        super().__init__(name, account_number, balance, bank_name)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate


# StockAccount class
class StockAccount(Account):
    def __init__(self, name, account_number):
        super().__init__(name)
        self.account_number = account_number

    def calculate_value(self):
        # Sum the value of all stocks in this account
        return sum(asset.calculate_total_value() for asset in self.holdings)

    def add_asset(self, asset):
        self.holdings.append(asset)

    def remove_asset(self, asset):
        self.holdings.remove(asset)


# RealEstateAccount class
class RealEstateAccount(Account):
    def __init__(self, name, account_type):
        super().__init__(name)
        self.account_type = account_type

    def calculate_value(self):
        # Sum the value of all real estate assets in this account
        return sum(asset.calculate_total_value() for asset in self.holdings)

    def add_asset(self, asset):
        self.holdings.append(asset)

    def remove_asset(self, asset):
        self.holdings.remove(asset)


# CryptoAccount class
class CryptoAccount(Account):
    def __init__(self, name, account_number):
        super().__init__(name)
        self.account_number = account_number

    def calculate_value(self):
        # Sum the value of all crypto assets in this account
        return sum(asset.calculate_total_value() for asset in self.holdings)

    def add_asset(self, asset):
        self.holdings.append(asset)

    def remove_asset(self, asset):
        self.holdings.remove(asset)


# Abstract Asset class
class Asset(ABC):
    def __init__(self, asset_id, name, value, purchase_date):
        self.asset_id = asset_id
        self.name = name
        self.value = value
        self.purchase_date = purchase_date

    @abstractmethod
    def calculate_total_value(self):
        pass

    def update_value(self, new_value):
        pass


# Stock class
class Stock(Asset):
    def __init__(self, asset_id, name, value, purchase_date, ticker, shares, purchase_price):
        super().__init__(asset_id, name, value, purchase_date)
        self.ticker = ticker
        self.shares = shares
        self.purchase_price = purchase_price

    def calculate_total_value(self):
        pass


# RealEstate class
class RealEstate(Asset):
    def __init__(self, asset_id, name, value, purchase_date, location, purchase_price, current_value):
        super().__init__(asset_id, name, value, purchase_date)
        self.location = location
        self.purchase_price = purchase_price
        self.current_value = current_value

    def calculate_total_value(self):
        pass


# Crypto class
class Crypto(Asset):
    def __init__(self, asset_id, name, value, purchase_date, ticker, units_held, purchase_price):
        super().__init__(asset_id, name, value, purchase_date)
        self.ticker = ticker
        self.units_held = units_held
        self.purchase_price = purchase_price

    def calculate_total_value(self):
        pass


# Cash class
class Cash(Asset):
    def __init__(self, asset_id, name, value, purchase_date, currency):
        super().__init__(asset_id, name, value, purchase_date)
        self.currency = currency

    def calculate_total_value(self):
        pass


# AssetFactory class
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


# AccountFactory class
class AccountFactory:
    @staticmethod
    def create_account(account_type, *args, **kwargs):
        if account_type == "stock":
            return StockAccount(*args, **kwargs)
        elif account_type == "realestate":
            return RealEstateAccount(*args, **kwargs)
        elif account_type == "crypto":
            return CryptoAccount(*args, **kwargs)
        elif account_type == "checking":
            return CheckingAccount(*args, **kwargs)
        elif account_type == "savings":
            return SavingsAccount(*args, **kwargs)
        else:
            raise ValueError(f"Unknown account type: {account_type}")


# Singleton DB Connection class, 
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # TODO: add initialization code here
        return cls._instance
