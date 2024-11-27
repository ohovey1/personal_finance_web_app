from ..models.account import (BankAccount, CheckingAccount, 
                            SavingsAccount, StockAccount, 
                            RealEstateAccount, CryptoAccount)

class AccountFactory:
    @staticmethod
    def create_account(account_type, *args, **kwargs):
        accounts = {
            "stock": StockAccount,
            "realestate": RealEstateAccount,
            "crypto": CryptoAccount,
            "checking": CheckingAccount,
            "savings": SavingsAccount
        }
        
        account_class = accounts.get(account_type)
        if not account_class:
            raise ValueError(f"Unknown account type: {account_type}")
            
        return account_class(*args, **kwargs)