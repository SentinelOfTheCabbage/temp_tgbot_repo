# pylint: disable=C0111,W0614,W0401,R0914
from datetime import datetime, timedelta
import psycopg2
from NewSettings import *


class DbTeller:
    connect = None

    def __init__(self):
        # DATABASE CONST REQUIRED !
        self.connect = None
        self.host = ''
        self.database = ''
        self.user = ''
        self.port = ''
        self.password = ''

    def __connect__(self):
        self.connect = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            port=self.port,
            password=self.password
        )

    @staticmethod
    def _orders_get_query(client_id, destination, dest_date, dest_time, dest_stat, pay_stat, result_price, dest_price, dest_cost, bonuses, promocode, name, phone, comment):
        pattern = 'orders (client_id, destination, dest_date, dest_time, dest_stat'
        pattern += ', pay_stat, result_price, dest_price, dest_cost, pay_by_bonus, promo_id, name,phone,comment)'

        new_val = f'({client_id},{destination},{dest_date},{dest_time},{dest_stat},'
        new_val += f'{pay_stat},{result_price},{dest_price},{dest_cost},{bonuses},{promocode},{name},{phone},{comment})'

        query = f'INSERT INTO {pattern} VALUES {new_val} RETURNING order_id'.replace('None', 'NULL')

        return query

    @staticmethod
    def _orders_cont_get_query(order_id, basket):
        pattern = 'orders_content (order_id,product_key,amount,price)'

        vals = []
        for product in basket:
            product_key = f"'{product['key']}'"
            amount = product['amount']
            price = product['price']
            new_val = f'({order_id}, {product_key}, {amount}, {price})'
            vals.append(new_val)
        vals = ', '.join(vals)
        query = f'INSERT INTO {pattern} VALUES {vals}'.replace('None', ' NULL')

        return query

    @staticmethod
    def _clients_get_query(client_id, refer_from, phone, name, address, bonuses, comment):
        pattern = 'clients (client_id,refer_from,phone,name,address,bonuses,comment)'
        phone = ''.join([i for i in phone if i in list(map(str, range(10)))])
        vals = f'({client_id}, {refer_from}, {phone}, {name}, {address}, {bonuses},{comment})'
        query = f'INSERT INTO {pattern} VALUES {vals}'.replace('None', ' NULL')

        return query

    @staticmethod
    def _client_check_query(client_id, phone, name, address):
        query = f"""
            SELECT * FROM clients
                WHERE (
                    (client_id = {client_id}) and
                    (phone = {phone}) and
                    (name = {name}) and
                    (address = {address}))
        """
        return query

    def on_finish(self, client_info):
        keys = client_info.keys()
        for key in keys:
            if isinstance(client_info[key], str):
                client_info[key] = client_info[key].replace("'", "''")
                client_info[key] = f"'{client_info[key]}'"

        client_id = client_info['id']
        address = client_info['address']
        dest_date = f"to_date({client_info['delivery_date']},'DD.MM.YY')"
        dest_time = client_info['delivery_time']
        # if not dest_time is None:
        #     dest_time = f'\'{dest_time}\''

        dest_stat = "'No'"
        pay_stat = "'No'"
        result_price = sum([i['price'] for i in client_info['basket']])
        dest_price = client_info['delivery_price']
        if dest_price is None:
            dest_price = 0
        dest_cost = client_info['delivery_cost']
        refer_from = client_info['referal_id']
        phone = ''.join([i for i in list(client_info['phone'])
                         if i in list(map(str, range(10)))])
        phone = f"'{phone}'"
        name = client_info['name']
        bonuses = client_info['pay_by_bonuses']
        promocode = client_info['promocode']
        if promocode != 'null':
            result_price *= client_info['discount']
        comment = client_info['comment']

        if len(comment) > 250:
            comment = comment[:240]

        query = self._orders_get_query(
            client_id, address, dest_date, dest_time,
            dest_stat, pay_stat, result_price,
            dest_price, dest_cost, bonuses, promocode, name, phone, comment
        )
        print(query)
        if 'pay_by_bonuses' in client_info and client_info['pay_by_bonuses'] > 0:
            query = f'''
                UPDATE bonuses
                SET bonuses_amount = bonuses_amount - {client_info['pay_by_bonuses']}
                WHERE client_id = {client_id};
            ''' + query
        try:
            order_id = self.execute(query, client_id)[0][0]
            orders_content = self._orders_cont_get_query(
                order_id, client_info['basket'])
            self.execute(orders_content, client_id)
        except:  # pylint: disable=W0702
            order_id = 999

        check_client = self._client_check_query(
            client_id, phone, name, address)
        answer = self.execute(check_client)
        if not answer:
            add_to_clients = self._clients_get_query(
                client_id, refer_from, phone, name, address, bonuses, comment)
            self.execute(add_to_clients)

    def to_log(self, user, message=None, reaction=None):
        dtime = f"TIMESTAMP '{str(datetime.now()+timedelta(hours=3))}'"
        user_id = user.id
        content = message.content.replace('\'', '\'\'')
        if len(content) > 50:
            content = content[:50]

        is_button = (message.type == 'callback')

        print(f'[{user_id}]: {reaction}')

        query = f"""
            INSERT INTO logs
                VALUES (
                    {user_id},{1},{dtime},
                    {is_button},'{content}','{reaction}'
                )
        """

        self.execute(query)

    def get_last_order_id(self):
        query = 'SELECT last_value FROM orders_order_id_seq;'

        self.__connect__()

        cursor = self.connect.cursor()
        cursor.execute(query)

        sql_return_tuple = cursor.fetchone()

        self.connect.commit()
        cursor.close()
        self.connect.close()

        return sql_return_tuple[0]

    def execute(self, cmd, user_id=None):
        self.__connect__()

        # if user_id in testers_id_list:
        #     return 0

        cursor = self.connect.cursor()
        cursor.execute(cmd)

        answer = None
        try:
            answer = cursor.fetchall()
        except:  # pylint: disable=W0702
            pass

        self.connect.commit()
        cursor.close()
        self.connect.close()
        return answer

    # def update_stock(self, key, weight, user):
    #     query = f'UPDATE products SET in_stock = in_stock - {weight} WHERE product_key = \'{key}\''
    #     self.execute(query, user.id)

    def get_products_list(self) -> dict:
        query = 'SELECT * FROM products WHERE availability = true'
        # query = 'SELECT * FROM products'
        answer = self.execute(query)
        keys = [e[0] for e in answer]
        titles = [e[1] for e in answer]
        descriptions = [e[2] for e in answer]
        pack_sizes = [float(e[3]) for e in answer]
        prices = [float(e[4]) for e in answer]
        in_stock = [float(e[6]) for e in answer]
        amounts = []

        for pos, key in enumerate(keys):
            if 'prod' in key:
                pack_size = pack_sizes[pos]
                amounts.append([i * pack_size for i in range(1, 7)])
            elif ('pack' in key) or ('fish' in key):
                amounts.append([i for i in range(1, 7)])
            elif 'oyster' in key:
                amounts.append([i for i in range(6, 12)])

        prod_info = {}
        for pos, key in enumerate(keys):
            main_info = {}
            main_info['key'] = key
            main_info['title'] = titles[pos]
            main_info['description'] = descriptions[pos]

            if ('prod' in key) or ('fish' in key):
                price_desk = str(int(prices[pos] / pack_sizes[pos])) + 'р/кг'
            elif 'pack' in key:
                if 'mask' not in key:
                    price_desk = f'{int(prices[pos])}р/шт'
                else:
                    price_desk = str(int(prices[pos])) + 'р/упак.'

            if ('oyster' in key) or ('knife' in key):
                price_desk = f'{int(prices[pos])}р/шт'

            main_info['price_desk'] = price_desk
            main_info['price'] = prices[pos]
            main_info['in_stock'] = in_stock[pos]
            main_info['pack_size'] = pack_sizes[pos]
            main_info['amounts'] = amounts[pos]
            main_info['availability'] = True
            main_info['amount'] = 0
            prod_info[key] = main_info

        return prod_info
        # return

    def update_order_feedback_status(self, order_id):
        query = f'UPDATE orders SET feedback_status = true WHERE order_id = {order_id}'
        self.execute(query)

    def get_products_from_order(self, order_id=None):
        query = f"""SELECT DISTINCT p.title, oc.product_key
            FROM products p
            LEFT JOIN orders_content oc
            ON p.product_key = oc.product_key
            WHERE
                order_id = {order_id}
        """
        return self.execute(query)

    def get_user_last_phone(self, user_id):
        query = f"""SELECT DISTINCT order_id, phone
            FROM orders
            WHERE (
            client_id = {user_id}
            )
            ORDER BY order_id DESC
            LIMIT 1;
        """
        return self.execute(query)

    def get_user_last_address(self, user_id):
        query = f"""SELECT DISTINCT order_id, destination
            FROM orders
            WHERE (
            client_id = {user_id}
            )
            ORDER BY order_id DESC
            LIMIT 1;
        """
        return self.execute(query)

    def get_user_last_name(self, user_id):
        query = f"""SELECT DISTINCT order_id, name
            FROM orders
            WHERE (
            client_id = {user_id}
            )
            ORDER BY order_id DESC
            LIMIT 1;
        """
        return self.execute(query)

    def get_user_last_comment(self, user_id):
        query = f"""SELECT DISTINCT order_id, comment
            FROM orders
            WHERE (
            client_id = {user_id} AND
            comment is not null
            )
            ORDER BY order_id DESC
            LIMIT 1;
        """
        return self.execute(query)

    def get_bonuses(self, user_id):
        query = f"""SELECT bonuses_amount
            FROM bonuses
            WHERE client_id = {user_id}
        """
        return self.execute(query)

    def get_user_bonus_code(self, user_id):
        query = f"""SELECT bonus_code
            FROM bonuses
            WHERE client_id = {user_id}
        """
        return self.execute(query)

    def is_bonus_code_existing(self, bonus_code: str, user_id: int):
        query = f"""SELECT bonus_type
            FROM bonuses
            WHERE (
                bonus_code = '{bonus_code}' AND
                client_id != {user_id}
            )
        """
        return self.execute(query)

    def create_bonus_code(self, user_id, bonus_code: str):
        query = f"""INSERT INTO bonuses (bonus_code,bonus_type,bonuses_amount,client_id)
            VALUES ('{bonus_code}',1,0,{user_id})
        """
        return self.execute(query)

    def give_revard_by_promo(self, bonus_code: str):
        def get_revard_size(self, bonus_code: str):
            query = f"""SELECT returns
                FROM bonus_types
                WHERE type_id = (SELECT bonus_type
                    FROM bonuses
                    WHERE bonus_code = '{bonus_code}'
                )
            """
            return self.execute(query)

        # revard_size = int(get_revard_size(self, bonus_code)[0][0])
        query = f"""
        UPDATE bonuses
            SET
            bonuses_amount = bonuses_amount +
                (
                SELECT returns
                    FROM bonus_types
                    WHERE type_id =
                        (
                        SELECT bonus_type
                            FROM bonuses
                            WHERE bonus_code = '{bonus_code}'
                        )
                )
            WHERE bonus_code = '{bonus_code}'
        """
        return self.execute(query)

    def update_uses(self, user_id: str):
        query = f"""INSERT INTO bonus_uses (bonus_type,client_id)
            VALUES(1,{user_id})
        """
        return self.execute(query)

    def update_bonuses(self, user_id: str, bonuses: int):
        query = f"""UPDATE bonuses
            SET bonuses_amount = bonuses_amount - {bonuses}
            WHERE client_id = {user_id}
        """
        self.execute(query)

    def is_uses_available(self, user_id: str) -> bool:
        # query = """SELECT max_uses
        #     FROM bonus_types
        #     WHERE type_id = 1
        # """
        # max_uses = self.execute(query)[0][0]
        query = f"""SELECT COUNT(*)
            FROM clients
            WHERE client_id = {user_id}
        """
        cur_uses = self.execute(query)[0][0]
        return (cur_uses == 0)

    def get_order_id_list(self, delta=0):
        today = datetime.strptime(
            str((datetime.now().date() + timedelta(days=delta)).isoformat()), '%Y-%m-%d')
        tomorrow = (today + timedelta(days=1)).date()
        today = today.date()
        # print(today, tomorrow)
        query = f"SELECT order_id, dest_time, destination, name, phone FROM orders WHERE ((to_date('{today}','YYYY-MM-DD') <= dest_date) AND (dest_date < to_date('{tomorrow}','YYYY-MM-DD')))"
        return self.execute(query)

    def get_products_by_order_id(self, order_id):
        query = f"SELECT p.title,p.product_key, p.pack_size, o.amount FROM products p LEFT JOIN orders_content o ON p.product_key = o.product_key WHERE o.order_id = {order_id};"

        return self.execute(query)

    def create_supply(self, basket):
        query = f'INSERT INTO supply(supplier_id, product_key, sup_size, in_stock, price) VALUES '
        P = []
        for product in basket:
            P.append(f'(1,\'{product["key"]}\',{product["amount"]},{product["amount"]},{round(product["price"])})')
        query += ', '.join(P)
        print(query)
        return self.execute(query)

    def is_code_works(self, promocode: str, user_id: int) -> bool:
        query = f'''
            SELECT
            (LOWER('{promocode}') in
                (SELECT LOWER(bonus_code) FROM bonuses WHERE client_id != {user_id})
            )
            AND
            ({user_id} not in (SELECT client_id FROM clients))
        ,
            ROUND((100 - (SELECT percent FROM bonus_types WHERE type_id = 2))/100,2)
        ,
            (SELECT returns
                FROM bonus_types
                WHERE type_id = (
                    SELECT bonus_type FROM bonuses WHERE LOWER('{promocode}') = LOWER(bonus_code)
                )
            )
        '''
        return self.execute(query)[0]

if __name__ == '__main__':
    print('Done')
