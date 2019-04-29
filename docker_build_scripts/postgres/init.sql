CREATE DATABASE football_stats;

CREATE USER some_db_user WITH PASSWORD 'some_secure_password';

ALTER ROLE some_db_user SET client_encoding TO 'utf8';
ALTER ROLE some_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE some_db_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE football_stats TO some_db_user;