from abc import ABC, abstractmethod
from datetime import date

'''
User class. Represents a user of the application.

Attributes:
    user_id (int): Unique identifier for user
    name (str): Name of user
    email (str): Email of user
    password (str): Password of user
    logged_in (bool): True if user is logged in, False otherwise
    portfolio (Portfolio): Portfolio object that stores Account objects

Methods:
    register(): Register user to database
    login(email, password): Check if email and password match database. If match, set logged_in to True
    update_profile(new_name, new_email): Update user profile in database
    delete_account(): Delete user account from database
    create_account(account_type, *args, **kwargs): Create an account of specified type and add to portfolio
    add_asset_to_account(account_id, asset_type, *args, **kwargs): Add asset to account in portfolio
    view_portfolio_summary(): Display portfolio summary
'''
class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.logged_in = False
        self.portfolio = Portfolio()  # Composition: User owns a Portfolio. Stores Account objects which store Assets

    def register(self):
        #TODO: Register user to database
        pass

    def login(self, email, password):
        #TODO: Check if email and password match database
        # If match, set logged_in to True
        pass

    def update_profile(self, new_name, new_email):
        #TODO: Update user profile in database
        self.name = new_name
        self.email = new_email

    def delete_account(self):
        #TODO: Delete user account from database
        pass

    def create_account(self, account_type, *args, **kwargs):
        account = AccountFactory.create_account(account_type, *args, **kwargs)
        self.portfolio.add_account(account)
    
    def add_asset_to_account(self, account_id, asset_type, *args, **kwargs):
        asset = AssetFactory.create_asset(asset_type, *args, **kwargs)
        self.portfolio.accounts[account_id].add_asset(asset)

    def view_portfolio_summary(self):
        # TODO: Display portfolio summary
        self.portfolio.view_summary()

'''
Asset class. Abstract base class for different types of assets.

Attributes:
    name (str): Name of asset
    purchase_date (date): Date asset was purchased (set to today by default)

Methods:
    calculate_value(): Abstract method to calculate value of asset

Concrete Asset classes:
    Stock: Represents a stock asset
    RealEstate: Represents a real estate asset
    Crypto: Represents a cryptocurrency asset
    Cash: Represents a cash asset
'''
# NOTE: asset_id managed by Account.holdings dictionary
class Asset(ABC):
    def __init__(self, name):
        self.name = name
        self.purchase_date = date.today() # Store purchase date as date which it was added (today)

    @abstractmethod
    def calculate_value(self):
        pass

    # @abstractmethod
    # def update_value(self, new_value):
    #     pass


# Stock class
class Stock(Asset):
    def __init__(self, name, ticker, shares, purchase_price):
        super().__init__(name)
        self.ticker = ticker
        self.shares = shares
        self.purchase_price = purchase_price

    def get_current_stock_price(self):
        # TODO: Get price from stock API
        pass

    def calculate_value(self):
        # Calculate using current stock value
        #TODO: Implement after get_current_stock_price is implemented
        return self.purchase_price * self.shares

# RealEstate class
class RealEstate(Asset):
    def __init__(self, name, address, purchase_date, purchase_price, current_value):
        super().__init__(name)
        self.address = address
        self.purchase_date = purchase_date
        self.purchase_price = purchase_price
        self.current_value = current_value

    def calculate_value(self):
        # Use current value of property for now
        #TODO: Use zillow API to get current value
        return self.current_value

# Crypto class
class Crypto(Asset):
    def __init__(self, name, ticker, units_held, purchase_price):
        super().__init__(name)
        self.ticker = ticker
        self.units_held = units_held
        self.purchase_price = purchase_price

    def get_current_crypto_price(self):
        # TODO: Get current price from some crypto API
        pass  

    def calculate_value(self):
        # Get total value of crypto held
        #TODO: Implement once get current price is implemented
        return self.purchase_price * self.units_held

# Cash class
class Cash(Asset):
    def __init__(self, amount, name="Cash"):
        super().__init__(name)
        self.amount = amount

    def calculate_value(self):
        # Cash value is equal to amount
        return self.amount

'''
Account class. Abstract base class for different types of accounts.

Attributes:
    name (str): Name of account
    holdings (dict): Dictionary of assets held by this account, asset_id as key

Methods:
    calculate_value(): Abstract method to calculate total value of account
    add_asset(asset): Abstract method to add asset to account
    remove_asset(asset): Abstract method to remove asset from account
    view_account(): Display account details

Concrete Account classes:
    BankAccount: Represents a bank account
    CheckingAccount: Represents a checking account, derived from BankAccount
    SavingsAccount: Represents a savings account, derived from BankAccount
    StockAccount: Represents a stock trading account
    RealEstateAccount: Represents a real estate account
    CryptoAccount: Represents a cryptocurrency trading account
'''
class Account(ABC):
    def __init__(self, name):
        self.name = name
        self.holdings = {}  # Dictionary of assets held by this account, asset_id as key

    @abstractmethod
    def calculate_value(self):
        pass

    @abstractmethod
    def add_asset(self, asset):
        pass

    @abstractmethod
    def remove_asset(self, asset):
        pass

    def view_account(self):
        # Display account details
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

# Concrete Account classes.

# BankAccount class.
# Inherits from Account class
class BankAccount(Account):
    def __init__(self, name, bank_name):
        super().__init__(name)
        self.bank_name = bank_name
        self.balance = 0 # Default balance is 0
        self.add_asset(Cash(0))  # Add cash asset w/ amount 0 to bank account holdings

    def calculate_value(self):
        # For bank accounts, value is the balance
        return self.balance
    
    def add_asset(self, asset): 
        asset_id = 1
        self.holdings[asset_id] = asset # Add asset to holdings w/ asset id 1

    def remove_asset(self, asset):
        # remove asset from holdings dictionary
        self.holdings.pop(0)

    def deposit(self, amount):
        # Update balances
        self.balance += amount
        self.holdings[1].amount += amount # Update cash asset amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.holdings[1].amount -= amount # Update cash asset amount
            return
        print("Insufficient funds.")


# CheckingAccount class
class CheckingAccount(BankAccount):
    def __init__(self, name, bank_name, overdraft_limit):
        super().__init__(name, bank_name)
        self.account_type = "Checking"
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        # Override withdraw method to allow overdrafts.
        if amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            self.holdings[1].amount -= amount
            return
        print("Insufficient funds.") 

# SavingsAccount class
class SavingsAccount(BankAccount):
    def __init__(self, name, bank_name, interest_rate):
        super().__init__(name, bank_name)
        self.account_type = "Savings"
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance = self.balance * (1+self.interest_rate)
        self.holdings[1].amount = self.holdings[1].amount * (1+self.interest_rate)

# StockAccount class
class StockAccount(Account):
    def __init__(self, name, brokerage):
        super().__init__(name)
        self.account_type = "Stock"
        self.brokerage = brokerage

    def calculate_value(self):
        # Calculate total value of all stocks in account
        total_value = 0
        for asset in self.holdings.values():
            total_value += asset.calculate_value()
        return total_value

    def add_asset(self, asset : Stock):
        asset_id = len(self.holdings) + 1
        self.holdings[asset_id] = asset

    def remove_asset(self, asset_id):
        self.holdings.pop(asset_id)


# RealEstateAccount class
class RealEstateAccount(Account):
    def __init__(self, name):
        super().__init__(name)
        self.account_type = "Real Estate"
    
    def calculate_value(self):
        # Calculate total value of all real estate in account
        total_value = 0
        for asset in self.holdings.values():
            total_value += asset.calculate_value()
        return total_value

    def add_asset(self, asset : RealEstate):
        asset_id = len(self.holdings) + 1
        self.holdings[asset_id] = asset

    def remove_asset(self, asset_id):
        self.holdings.pop(asset_id)

# CryptoAccount class
class CryptoAccount(Account):
    def __init__(self, name, exchange):
        super().__init__(name)
        self.account_type = "Crypto"
        self.exchange = exchange
    
    def calculate_value(self):
        # Calculate total value of all crypto in account
        total_value = 0
        for asset in self.holdings.values():
            total_value += asset.calculate_value()
        return total_value

    def add_asset(self, asset : Crypto):
        asset_id = len(self.holdings) + 1
        self.holdings[asset_id] = asset

    def remove_asset(self, asset_id):
        self.holdings.pop(asset_id)

'''
Factory classes for creating Asset and Account objects.

Asset Factory Parameters:
    asset_type (str): Type of asset to create, must be one of 'stock', 'realestate', 'crypto', 'cash'

Account Factory Parameters:
    account_type (str): Type of account to create, must be one of 'stock', 'realestate', 'crypto', 'checking', 'savings'

Returns an instance of the specified class.
'''

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
            raise ValueError(f"Unknown asset type: {asset_type}. Must be one of 'stock', 'realestate', 'crypto', 'cash'")

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
            raise ValueError(f"Unknown account type: {account_type}. Must be one of 'stock', 'realestate', 'crypto', 'checking', 'savings'")


'''
Portfolio class. Represents a collection of accounts containing all the users assets.

Attributes:
    accounts (dict): Dictionary of accounts, account_id as key

Methods:
    add_account(account): Add account to portfolio
    remove_account(account_id): Remove account from portfolio
'''
class Portfolio:
    def __init__(self):
        self.accounts = {}  # Dictionary of accounts

    def add_account(self, account : Account):
        # Add Account to portfolio. Starting with account_id 1, increment by 1
        account_id = len(self.accounts) + 1
        self.accounts[account_id] = account

    def remove_account(self, account_id):
        # Remove account from portfolio
        del self.accounts[account_id]

    def view_accounts(self):
        # Display all accounts in portfolio
        for account_id, account in self.accounts.items():
            print(f"Account ID: {account_id}")
            print(f"Account Type: {account.name}")
            print("\n")
            #account.view_account()

    def view_summary(self):
        #TODO: Implement summary view
        pass

'''
Singleton class for managing database connection.
'''
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # TODO: add initialization code here
        return cls._instance
