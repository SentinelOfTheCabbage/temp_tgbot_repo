CREATE TABLE products(
	product_key VARCHAR(15) NOT NULL PRIMARY KEY,
	title VARCHAR(50) NOT NULL,
	description VARCHAR(150) NOT NULL,
	pack_size NUMERIC(8,2) NOT NULL,
	pack_price NUMERIC(6,1) NOT NULL,
	availability BOOLEAN,
	in_stock NUMERIC(9,2) NOT NULL,
	discount NUMERIC(7,3),
	keeping_rules VARCHAR(1000)
);

CREATE TABLE supply(
	supply_id SERIAL NOT NULL PRIMARY KEY,
	supplier_id SERIAL NOT NULL REFERENCES supplier.supplier_id,
	product_key VARCHAR(15) NOT NULL REFERENCES products.product_key,
	dtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	sup_size NUMERIC(7),
	price NUMERIC(7)
);

CREATE TABLE supplier(
	supplier_id SERIAL NOT NULL PRIMARY KEY,
	address VARCHAR(150),
	phone VARCHAR(20) ,
	name VARCHAR(30)
);

ALTER TABLE orders ADD name VARCHAR(30), phone VARCHAR(20);

INSERT INTO products (product_key, title,description,min_pack_size,pack_price,availability,amount,discount,keeping_rules)