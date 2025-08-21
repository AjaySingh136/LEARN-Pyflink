-- MySQL init: demo schema and seed data
CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY,
  name VARCHAR(128) NOT NULL
);

INSERT INTO users (id, name) VALUES
  (1, 'Alice'),
  (2, 'Bob'),
  (3, 'Charlie')
ON DUPLICATE KEY UPDATE name=VALUES(name);