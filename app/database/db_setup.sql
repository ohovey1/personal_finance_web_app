-- Users table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Portfolios table
CREATE TABLE Portfolios (
    portfolio_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accounts table
CREATE TABLE Accounts (
    account_id SERIAL PRIMARY KEY,
    portfolio_id INTEGER REFERENCES Portfolios(portfolio_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    institution VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_account_type CHECK (
        account_type IN ('checking', 'savings', 'stock', 'crypto', 'realestate')
    )
);

-- Assets table
CREATE TABLE Assets (
    asset_id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES Accounts(account_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(50) NOT NULL,
    purchase_price DECIMAL(19,4) NOT NULL,
    current_value DECIMAL(19,4),
    purchase_date TIMESTAMP NOT NULL,
    metadata JSONB,
    CONSTRAINT valid_asset_type CHECK (
        asset_type IN ('stock', 'realestate', 'crypto', 'cash')
    )
);