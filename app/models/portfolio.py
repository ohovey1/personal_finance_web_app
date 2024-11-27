'''
Portfolio class. Represents a collection of accounts containing all the users assets.

Attributes:
    accounts (dict): Dictionary of accounts, account_id as key

Methods:
    add_account(account): Add account to portfolio
    remove_account(account_id): Remove account from portfolio
'''
from ..database.db_connection import DatabaseConnection

class Portfolio:
    def __init__(self, portfolio_id=None, user_id=None, name="Default Portfolio"):
        self.portfolio_id = portfolio_id
        self.user_id = user_id
        self.name = name
        self.accounts = {}  # Dictionary to store accounts
        self.db = DatabaseConnection()

    def save(self):
        """Save portfolio to database"""
        query = """
        INSERT INTO Portfolios (user_id, name, created_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        RETURNING portfolio_id;
        """
        result = self.db.execute_query(query, (self.user_id, self.name))
        if result:
            self.portfolio_id = result[0]['portfolio_id']
            return True
        return False

    @classmethod
    def get_by_user_id(cls, user_id):
        """Get portfolio by user ID"""
        db = DatabaseConnection()
        query = "SELECT portfolio_id, name FROM Portfolios WHERE user_id = %s;"
        result = db.execute_query(query, (user_id,))
        if result:
            portfolio_data = result[0]
            return cls(
                portfolio_id=portfolio_data['portfolio_id'],
                user_id=user_id,
                name=portfolio_data['name']
            )
        return None

    def add_account(self, account):
        """Add account to portfolio and database"""
        # First save account to database
        query = """
        INSERT INTO Accounts (portfolio_id, name, account_type, institution)
        VALUES (%s, %s, %s, %s)
        RETURNING account_id;
        """
        result = self.db.execute_query(
            query, 
            (self.portfolio_id, account.name, account.account_type, account.institution)
        )
        if result:
            account_id = result[0]['account_id']
            self.accounts[account_id] = account
            account.account_id = account_id  # Set the account's ID
            return account_id
        return None

    def remove_account(self, account_id):
        """Remove account from portfolio and database"""
        query = "DELETE FROM Accounts WHERE account_id = %s AND portfolio_id = %s;"
        self.db.execute_query(query, (account_id, self.portfolio_id))
        if account_id in self.accounts:
            del self.accounts[account_id]

    def get_accounts(self):
        """Get all accounts from database"""
        query = """
        SELECT account_id, name, account_type, institution 
        FROM Accounts 
        WHERE portfolio_id = %s;
        """
        results = self.db.execute_query(query, (self.portfolio_id,))
        self.accounts = {}
        if results:
            for result in results:
                # Use AccountFactory to create appropriate account type
                from ..factories.account_factory import AccountFactory
                account = AccountFactory.create_account(
                    result['account_type'],
                    result['name'],
                    result['institution']
                )
                account.account_id = result['account_id']
                self.accounts[account.account_id] = account
        return self.accounts

    def calculate_total_value(self):
        """Calculate total portfolio value"""
        total_value = 0
        for account in self.accounts.values():
            total_value += account.calculate_value()
        return total_value

    def view_accounts(self):
        """Display all accounts in portfolio"""
        accounts = self.get_accounts()  # Refresh accounts from database
        for account_id, account in accounts.items():
            print(f"Account ID: {account_id}")
            print(f"Account Type: {account.account_type}")
            print(f"Account Name: {account.name}")

    def view_detailed_summary(self):
        """Display detailed portfolio summary"""
        accounts = self.get_accounts()  # Refresh accounts from database
        for account_id, account in accounts.items():
            print(f"Account ID: {account_id}")
            account.view_account()
        print(f"Total Portfolio Value: {self.calculate_total_value()}\n")