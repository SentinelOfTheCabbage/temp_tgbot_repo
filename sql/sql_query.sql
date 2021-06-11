CREATE TABLE orders(
	order_id SERIAL NOT NULL PRIMARY KEY,
	user_id NUMERIC(13),
	create_time DATE NOT NULL DEFAULT CURRENT_DATE,
	destination VARCHAR(100) NOT NULL,
	dest_date DATE NOT NULL,
	dest_time VARCHAR(3),
	dest_stat VARCHAR(3),
	pay_stat VARCHAR(3) NOT NULL,
	result_price NUMERIC(6) NOT NULL,
	dest_price NUMERIC(4) NOT NULL,
	dest_cost NUMERIC(4) NOT NULL,
	is_rewrite INTEGER REFERENCES orders(order_id),
	pay_by_bonus NUMERIC(6),
	promo_id VARCHAR(5)
);