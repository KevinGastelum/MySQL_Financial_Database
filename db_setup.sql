-- db_setup.sql
CREATE TABLE IF NOT EXISTS top_gainers (
    ticker VARCHAR PRIMARY KEY,
    price DECIMAL,
    change_amount DECIMAL,
    change_percentage DECIMAL,
    volume BIGINT
);

CREATE TABLE IF NOT EXISTS top_losers (
    ticker VARCHAR PRIMARY KEY,
    price DECIMAL,
    change_amount DECIMAL,
    change_percentage DECIMAL,
    volume BIGINT
);

CREATE TABLE IF NOT EXISTS most_actively_traded (
    ticker VARCHAR PRIMARY KEY,
    price DECIMAL,
    change_amount DECIMAL,
    change_percentage DECIMAL,
    volume BIGINT
);
