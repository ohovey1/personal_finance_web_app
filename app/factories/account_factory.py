from ..models.account import Account, StockAccount, CryptoAccount, BankAccount

class AccountFactory:
    @staticmethod
    def create_account(account_type: str, name: str):
        """
        Create an account of specified type.
        
        Args:
            account_type: Type of account ('stock', 'crypto', 'bank')
            name: Name of the account
        """
        try:
            if account_type == "stock":
                return StockAccount(name)
            elif account_type == "crypto":
                return CryptoAccount(name)
            elif account_type == "bank":
                return BankAccount(name)
            else:
                raise ValueError(f"Unknown account type: {account_type}")
        except Exception as e:
            print(f"Error creating account: {str(e)}")
            return None