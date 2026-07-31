-- TABLES CREATION
CREATE TABLE IF NOT EXISTS customers (
	customer_id SERIAL PRIMARY KEY,
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	age INT,
	country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS orders (
	order_id SERIAL PRIMARY KEY,
	item VARCHAR(100),
	amount INT,
	customer_id INT,
	-- Explicitly named constraint
	CONSTRAINT fk_order_customer
		FOREIGN KEY (customer_id)
		REFERENCES customers(customer_id)
);

CREATE TABLE shippings (
    shipping_id SERIAL PRIMARY KEY,
    status VARCHAR(50),
	-- Inline Foreign Key
    customer_id INT REFERENCES customers(customer_id)
);

-- RECORD INSERT
-- In PostgreSQL, single quotes are strictly used for text strings (literals), while double quotes are strictly used for database object names (identifiers) like tables and columns.
INSERT INTO customers (first_name, last_name, age, country)
VALUES
('John', 'Doe', 31, 'USA'),
('Robert', 'Luna', 22, 'USA'),
('David', 'Robinson', 22, 'UK'),
('John', 'Reinhardt', 25, 'UK'),
('Betty', 'Doe', 28, 'UAE');

INSERT INTO orders (item, amount, customer_id)
VALUES
('Keyboard', 400, 4),
('Mouse', 300, 4),
('Monitor', 12000, 3),
('Keyboard', 400, 1),
('Mousepad', 250, 2);

INSERT INTO shippings (status, customer_id)
VALUES
('Pending', 2),
('Pending', 4),
('Delivered', 3),
('Pending', 5),
('Delivered', 1);

DROP TABLE IF EXISTS customer;

-----------------------

-- SELECT
SELECT * FROM customers;
SELECT DISTINCT country FROM customers;
SELECT COUNT(DISTINCT country) FROM customers;
SELECT COUNT(*) AS "No of Rows" FROM customers;
SELECT COUNT(*) AS "No of Countries" FROM (SELECT DISTINCT country FROM customers); -- Nested Query
SELECT * FROM customers WHERE country = 'USA' AND age >= 30 AND last_name = 'Doe';
SELECT * FROM customers WHERE country <> 'UAE'; -- !=

SELECT amount FROM orders ORDER BY amount; -- ASC
SELECT * FROM orders ORDER BY amount DESC;
SELECT * FROM orders ORDER BY customer_id, item; -- Multi-Column Sorting: left to right
SELECT * FROM orders ORDER BY amount ASC, item DESC;