DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS currencies;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS records;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE currencies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name CHAR(255) NOT NULL
);

CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name CHAR(255) NOT NULL
);

CREATE TABLE records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  currency_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  cost INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (currency_id) REFERENCES currencies (id),
  FOREIGN KEY (category_id) REFERENCES categories (id)
);

INSERT INTO currencies(name)
VALUES 
('UAH'),
('USD'),
('EUR'),
('CHF');

INSERT INTO categories(name)
VALUES 
('Food'),
('Clothes'),
('Drugs'),
('Vacation');

INSERT INTO users(username, password)
VALUES
('admin', 'admin'),
('sofiia', 'is-01');

INSERT INTO records(user_id, currency_id, category_id, cost)
VALUES
(1, 1, 1, 300),
(1, 2, 2, 400),
(2, 3, 3, 500),
(2, 1, 1, 2000);



