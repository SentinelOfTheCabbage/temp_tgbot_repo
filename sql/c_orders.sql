CREATE TABLE orders(
	order_id SERIAL NOT NULL PRIMARY KEY,
	client_id NUMERIC(13),
	create_time TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
	destination VARCHAR(100) NOT NULL,
	dest_date TIMESTAMP NOT NULL,
	dest_time VARCHAR(5),
	dest_stat VARCHAR(3),
	pay_stat VARCHAR(3) NOT NULL,
	result_price NUMERIC(6) NOT NULL,
	dest_price NUMERIC(4) NOT NULL,
	dest_cost NUMERIC(4) NOT NULL,
	is_rewrite INTEGER REFERENCES orders(order_id),
	pay_by_bonus NUMERIC(6),
	promo_id VARCHAR(5)
);