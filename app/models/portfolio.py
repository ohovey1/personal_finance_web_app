'''
Portfolio class. Represents a collection of accounts containing all the users assets.

Attributes:
    accounts (dict): Dictionary of accounts, account_id as key

Methods:
    add_account(account): Add account to portfolio
    remove_account(account_id): Remove account from portfolio
'''
from typing import Dict, Optional
from ..database.db_connection import DatabaseConnection
from .account import Account
from ..factories.account_factory import AccountFactory

class Portfolio:
    def __init__(self, user_id: Optional[int] = None):
        self.portfolio_id = None
        self.user_id = user_id
        self.accounts: Dict[int, Account] = {}
        self.db = DatabaseConnection()

    def add_account(self, account: Account) -> Optional[int]:
        """Add account to portfolio and save to database"""
        query = """
        INSERT INTO Accounts (portfolio_id, name, account_type)
        VALUES (%s, %s, %s)
        RETURNING account_id;
        """
        result = self.db.execute_query(
            query,
            (self.portfolio_id, account.name, account.account_type)
        )
        if result:
            account_id = result[0]['account_id']
            account.account_id = account_id
            self.accounts[account_id] = account
            return account_id
        return None

    def get_accounts(self) -> Dict[int, Account]:
        """Load accounts from database"""
        query = "SELECT * FROM Accounts WHERE portfolio_id = %s;"
        results = self.db.execute_query(query, (self.portfolio_id,))
        
        if results:
            for result in results:
                # Create account using factory
                account = AccountFactory.create_account(
                    result['account_type'],
                    name=result['name']
                )
                account.account_id = result['account_id']
                account.get_assets()  # Load account's assets
                self.accounts[account.account_id] = account
        
        return self.accounts

    def calculate_total_value(self) -> float:
        """Calculate total portfolio value"""
        return sum(account.calculate_total_value() for account in self.accounts.values())

    def save(self) -> bool:
        """Save portfolio to database"""
        if not self.user_id:
            return False
            
        query = """
        INSERT INTO Portfolios (user_id)
        VALUES (%s)
        RETURNING portfolio_id;
        """
        result = self.db.execute_query(query, (self.user_id,))
        if result:
            self.portfolio_id = result[0]['portfolio_id']
            return True
        return False

    @classmethod
    def get_by_user_id(cls, user_id: int) -> Optional['Portfolio']:
        """Get portfolio by user ID"""
        db = DatabaseConnection()
        query = "SELECT portfolio_id FROM Portfolios WHERE user_id = %s;"
        result = db.execute_query(query, (user_id,))
        
        if result:
            portfolio = cls(user_id)
            portfolio.portfolio_id = result[0]['portfolio_id']
            portfolio.get_accounts()  # Load accounts and their assets
            return portfolio
        return None