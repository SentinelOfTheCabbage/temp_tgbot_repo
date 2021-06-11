import psycopg2

print('[CONNECTION]')
connect = psycopg2.connect(
	host='',
	database='',
	user='',
	port='',
	password='',
)


print('[CURSOR]')
cursor = connect.cursor()

# with open('c_orders.sql','r') as file:
# 	print('[CMD ORDERS]')
# 	cursor.execute('DROP TABLE orders')
# 	cursor.execute(file.read())

# with open('c_ord_content.sql','r') as file:
# 	print('[CMD ORDER CONTENT]')
# 	cursor.execute('DROP TABLE order_content')
# 	cursor.execute(file.read())


# with open('clients.sql','r') as file:
# 	print('[CMD CLIENTS]')
# 	cursor.execute(file.read())

# with open('logs.sql','r') as file:
# 	print('[CMD LOGS]')
# 	cursor.execute('DROP TABLE logs;')
# 	cursor.execute(file.read())

# cursor.execute('ALTER TABLE logs ALTER COLUMN content TYPE varchar(150);')
# cursor.execute('ALTER TABLE orders ALTER COLUMN dest_time TYPE varchar(6);')

# ('SGPKUPW8',1,0,308775151), ('AMPMCVNG',1,0,928330879), ('PB4APEW8',1,0,215508813), ('PQWQCJAG',1,0,525609301), ('HUCX9HRM',1,0,885629577), ('4FQTZMXN',1,0,131624493), ('B6R5ELKA',1,0,396252844), ('6BASLYK3',1,0,317760602), ('FFDB2LD7',1,0,207393132), ('DPY4G3EC',1,0,590085247), ('9BLY2V2R',1,0,295932236), ('HBL4VXCV',1,0,387060593),


print('[COMMIT]')
connect.commit()
print('[CLOSE]')
cursor.close()
connect.close()
# python db_creator.py
