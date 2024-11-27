CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Portfolios (
    portfolio_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Accounts (
    account_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER REFERENCES Portfolios(portfolio_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL
);

CREATE TABLE Assets (
    asset_id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES Accounts(account_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(50) NOT NULL,
    units DECIMAL(19,8) NOT NULL,        -- For stocks/crypto: number of shares/coins
    purchase_price DECIMAL(19,4) NOT NULL, -- Price per unit when purchased
    current_price DECIMAL(19,4)           -- Current price (to be updated by API)
);