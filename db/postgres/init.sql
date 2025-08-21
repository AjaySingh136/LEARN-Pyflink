-- Postgres init: demo schema and seed data

CREATE TABLE IF NOT EXISTS word_counts_jdbc (
  word TEXT PRIMARY KEY,
  cnt BIGINT
);

CREATE TABLE IF NOT EXISTS transactions (
  txn_id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  amount NUMERIC(12,2) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO transactions (user_id, amount) VALUES
  (1, 10.50), (2, 22.00), (1, 5.25), (3, 99.99);