CREATE TABLE clients(
	client_id NUMERIC(13) NOT NULL PRIMARY KEY,
	refer_from NUMERIC(13),
	phone NUMERIC(15) NOT NULL,
	name VARCHAR(15),
	FIO VARCHAR(45),
	address VARCHAR(75),
	bonuses NUMERIC(5)
);