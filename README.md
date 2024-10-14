# Personal Finance Web Application

## Proposal

The idea is for a system which allows users to create accounts before entering information
pertaining to stock portfolios, real estate, crypto, etc. while processing and organizing this data
via OOP logic. The focus for the mini project would be on the OOP portion for working with the
various categories of financial data. For instance, a class of for stock portfolios along with an
interface class for stocks which are then employed for specific company stocks being added to
the system to effectively allow for efficient scaling to consider more companies without altering
the base logic. The additional areas of financial data would be handled in an analogous manner
with specific alterations to handle the unique nature of each category. As we move to build this,
it is highly probable this will be expanded upon with the specific implementation of OOP being
adapted as we progress into the project.

## OOP Design

Classes are broken down into the following

1. User class - 
2. Portfolio class - 
3. Account parent class (abstract), with following subclasses 
    - StockAccount
    - RealEstateAccount
    - CryptoAccount
    - BankAccount
4. Asset parent class (abstract), with following subclasses
    - Stock
    - RealEstate
    - Crypto
    - Cash
5. DBManager class (singleton)
6. Interface class