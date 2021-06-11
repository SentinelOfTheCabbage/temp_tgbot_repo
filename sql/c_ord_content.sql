CREATE TABLE orders_content(
	order_id INTEGER NOT NULL REFERENCES orders (order_id),
	product_key VARCHAR(12) NOT NULL,
	amount NUMERIC NOT NULL,
	price NUMERIC NOT NULL,
	markup INTEGER
);