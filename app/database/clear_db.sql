-- Remove all data from tables (in correct order due to foreign key constraints)
TRUNCATE TABLE assets CASCADE;
TRUNCATE TABLE accounts CASCADE;
TRUNCATE TABLE portfolios CASCADE;
TRUNCATE TABLE users CASCADE;