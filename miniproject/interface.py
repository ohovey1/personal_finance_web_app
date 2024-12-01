from backend import *
'''
Interface class.

Handles User Interface for the application, for now a simple CLI, taking user input and displaying output.
'''
class Interface:
    def __init__(self):
        self.user = None
    
    def main_loop(self):
        while True:
            print('Welcome to Personal Finance Manager\n')
            print('Select an option:\n')
            print('1. Register\n')
            #TODO: Add more options
            
            # For now, only register as an option. Need to implement more User methods w/ DB integration
            option = input('Enter option: ')
            if option == '1':
                name = input('Enter your name: ')
                email = input('Enter your email: ')
                password = input('Enter your password: ')
                self.user = User(1, name, email, password)
                self.user.logged_in = True # For now, set logged_in to True after registration
                print(f'User {name} registered successfully!\n')
                self.user.display_user()
                break
            else:
                print('Invalid option. Please try again.\n')

        while True:
            print('Select an option:\n')
            print('1. Create Account')
            print('2. Add Asset to Account')
            print('3. Display Accounts')
            print('4. Display Portfolio')
            print('5. Exit\n')

            option = input('Enter option: \n')
            if option == '1':
                print('Select an account type:\n')
                print('1. Checkings Bank Account')
                print('2. Savings Bank Account')
                print('3. Stock')
                print('4. RealEstate')
                print('5. Crypto\n')
                account_type = input('Enter account type: ')

                if account_type == '1':
                    account_name = input('Enter account name: ')
                    bank_name = input('Enter bank name: ')
                    overdraft_limit = float(input('Enter overdraft limit: '))
                    self.user.create_account('checking', account_name, bank_name, overdraft_limit)
                elif account_type == '2':
                    account_name = input('Enter account name: ')
                    bank_name = input('Enter bank name: ')
                    interest_rate = input('Enter interest rate: ')
                    self.user.create_account('savings', account_name, bank_name, interest_rate)
                elif account_type == '3':
                    account_name = input('Enter account name: ')
                    brokerage = input('Enter brokerage: ')
                    self.user.create_account('stock', account_name, brokerage)
                elif account_type == '4':
                    account_name = input('Enter account name: ')
                    self.user.create_account('realestate', account_name)
                elif account_type == '5':
                    account_name = input('Enter account name: ')
                    brokerage = input('Enter brokerage: ')
                    self.user.create_account('crypto', account_name, brokerage)
                else:
                    print('Invalid account type. Please try again.\n')

                print('Account created successfully!\n')
            
            elif option == '2':
                self.user.display_accounts()
                account_id = input('Enter account ID: ')
                # Print selected account
                self.user.portfolio.accounts[int(account_id)].view_account()
                # If bank account (checking or savings), ask for deposit or withdrawal
                if self.user.portfolio.accounts[int(account_id)].account_type == 'Checking' or self.user.portfolio.accounts[int(account_id)].account_type == 'Savings':
                    transaction_type = input('Enter transaction type (deposit/withdrawal): ')
                    amount = float(input('Enter amount: '))
                    if transaction_type == 'deposit':
                        self.user.portfolio.accounts[int(account_id)].deposit(amount)
                    elif transaction_type == 'withdrawal':
                        self.user.portfolio.accounts[int(account_id)].withdraw(amount)
                    else:
                        print('Invalid transaction type. Please try again.\n')

                # If stock, real estate, or crypto, ask to add or remove asset
                elif self.user.portfolio.accounts[int(account_id)].account_type == 'Stock' or self.user.portfolio.accounts[int(account_id)].account_type == 'Real Estate' or self.user.portfolio.accounts[int(account_id)].account_type == 'Crypto':
                    asset_type = input('Enter asset type (stock/realestate/crypto): ')
                    if asset_type == 'stock':
                        name = input('Enter asset name: ')
                        ticker = input('Enter ticker: ')
                        shares = float(input('Enter amount of shares: '))
                        purchase_price = float(input('Enter purchase price: '))
                        self.user.add_asset_to_account(int(account_id), 'stock', name, ticker, shares, purchase_price)
                    elif asset_type == 'realestate':
                        name = input('Enter asset name: ')
                        address = input('Enter address: ')
                        purchase_date = input('Enter purchase date: ')
                        purchase_price = float(input('Enter purchase price: '))
                        current_value = float(input('Enter current value: '))
                        self.user.add_asset_to_account(int(account_id), 'realestate', name, address, purchase_date, purchase_price, current_value)
                    elif asset_type == 'crypto':
                        name = input('Enter asset name: ')
                        ticker = input('Enter ticker: ')
                        units_held = float(input('Enter units held: '))
                        purchase_price = float(input('Enter purchase price: '))
                        self.user.add_asset_to_account(int(account_id), 'crypto', name, ticker, units_held, purchase_price)
                    else:
                        print('Invalid asset type. Please try again.\n')
                else:
                    print('Invalid account type. Please try again.\n')
                
                print('Asset added successfully!\n')

            elif option == '3':
                self.user.display_accounts()
            
            elif option == '4':
                self.user.display_portfolio()

            elif option == '5':
                print('Exiting application. Goodbye!')
                break
            else:
                print('Invalid option. Please try again.\n')
                



            
    


