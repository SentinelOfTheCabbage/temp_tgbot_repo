CREATE TABLE feedback{
	feedback_id SERIAL NOT NULL PRIMARY KEY,
	client_id REFERENCE clients.client_id,
	product_key VARCHAR(12) NOT NULL,
	datetime TIMESTAMP NOT NULL,

}
