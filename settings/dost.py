# pylint: disable=C0111,W0614,W0401,R1705,W0702
from datetime import datetime, timedelta
import json
import requests
# from products import *
from dost_const import *
from NewSettings import *


class Dostavista:

    def __init__(self, prod_dict=None):
        self.orders_url = INIT_ORDERS_LIST_URL
        self.create_url = INIT_CREATE_URL
        self.calculate_url = INIT_CALCULATE_URL
        self.my_header = {}
        self.my_header[TOKEN_KEY] = INIT_TOKEN
        self.prod_dict = prod_dict

    def my_cards(self):
        url='https://robot.dostavista.ru/api/business/1.1/bank-cards'
        req = requests.get(url=url,headers=self.my_header)
        return req
    def get_orders(self):
        req = requests.get(url=self.orders_url, headers=self.my_header)
        return req

    @staticmethod
    def _get_krab_timestamp(date, time, finish):
        tmp = time.find('to')
        time = int(time[:tmp])
        timestamp = datetime.strptime(date, '%d.%m.%y')

        # if time == 10:
        #     if finish:
        #         timestamp += timedelta(hours=time + 1)
        #     else:
        #         timestamp += timedelta(hours=time, minutes=30)
        # else:
        if finish:
            timestamp += timedelta(hours=time)
        else:
            timestamp += timedelta(hours=time - 1, minutes=30)
        # X-0.5 to X
        return timestamp.isoformat() + '+03:00'

    def _get_krabby_point(self, user_info, order_id):
        krabby = {}
        krabby['address'] = KRAB_ADDRESS
        krabby['contact_person'] = {
            'phone': KRAB_PHONE,
            'name': KRAB_NAME
        }
        krabby['client_order_id'] = str(order_id)
        krabby['required_start_datetime'] = None
        krabby['required_finish_datetime'] = None
        krabby['invisible_mile_navigation_instructions'] = KRAB_INSTRUCT
        krabby['note'] = KRAB_NOTE

        krabby['packages'] = []

        date = user_info['delivery_date']
        time = user_info['delivery_time']

        krabby['required_start_datetime'] = self._get_krab_timestamp(
            date, time, finish=True)
        krabby['required_finish_datetime'] = self._get_krab_timestamp(
            date, time, finish=True)

        return krabby

    @staticmethod
    def _get_timestamp(date, time, finish):
        tmp = time.find('to')
        time = int(time[:tmp])

        timestamp = datetime.strptime(date, '%d.%m.%y')

        if finish:
            timestamp += timedelta(hours=time + 1, minutes=30)
        else:
            timestamp += timedelta(hours=time)
        # X to X+1.5
        return timestamp.isoformat() + '+03:00'

    def _get_point_from_user(self, user_info, order_id):
        user = {}
        user['address'] = user_info['address']
        user['contact_person'] = {
            'phone': user_info['phone'],
            'name': user_info['name'],
        }
        user['client_order_id'] = str(order_id)
        user['required_start_datetime'] = self._get_timestamp(
            date=user_info['delivery_date'], time=user_info['delivery_time'], finish=False)
        user['required_finish_datetime'] = self._get_timestamp(
            date=user_info['delivery_date'], time=user_info['delivery_time'], finish=True)
        user['invisible_mile_navigation_instructions'] = USER_INSTRUCT
        user['note'] = user_info['comment']
        return user

    def _creator_points_getter(self, user_info, order_id):
        data = []
        data.append(self._get_krabby_point(user_info, order_id))
        data.append(self._get_point_from_user(user_info, order_id))
        return data

    def _creator_getter(self, user_info, order_id):
        data = {}
        data['matter'] = 'морепродукты'

        key_mas = {}
        for elem in self.prod_dict:
            key_mas[elem] = self.prod_dict[elem]['pack_size']

        basket = user_info['basket']
        # data['total_weight_kg'] = sum([el['mass'] for el in basket if 'prod'
        # in el['key'] else el['mass']*key_mas[el['key']]])
        data['total_weight_kg'] = 0
        for elem in basket:
            if 'prod' in elem['key']:
                data['total_weight_kg'] += elem['amount']
            else:
                data['total_weight_kg'] += elem['amount'] * \
                    key_mas[elem['key']]

        if 1 < data['total_weight_kg'] <= 1.5:
            data['total_weight_kg'] = 0
        elif 4 < data['total_weight_kg'] <= 5.5:
            data['total_weight_kg'] = 4
        elif 9 < data['total_weight_kg'] <= 11:
            data['total_weight_kg'] = 9
        elif 14 < data['total_weight_kg'] <= 16.5:
            data['total_weight_kg'] = 14

        data['total_weight_kg'] = round(data['total_weight_kg'])

        if 16.5 < data['total_weight_kg'] < 52:
            data['vehicle_type_id'] = 7
        elif data['total_weight_kg'] <= 17:
            data['vehicle_type_id'] = 6

        data['insurance_amount'] = INSURANCE_AMOUNT
        data['is_client_notification_enabled'] = True
        data['is_contact_person_notification_enabled'] = True
        data['loaders_count'] = 0
        data['points'] = []
        data['points'] = self._creator_points_getter(user_info, order_id)

        return data

    def create_order(self, user_info, order_id):
        user_data = self._creator_getter(user_info, order_id)
        user_data['payment_method'] = 'bank_card'
        user_data['bank_card_id']   = '1371784'
        # if user_info['id'] in testers_id_list:
        #     print('TESTER!')
        #     return 'OK', 200, (37.5412046, 55.738195)

        req = requests.post(url=self.create_url,
                            json=user_data, headers=self.my_header)

        status = req.reason
        if status == 'OK':
            order = json.loads(req.text)['order']
            destination = order['points'][-1]

            price = order['payment_amount']
            coords = (destination['longitude'], destination['latitude'])
            if price is not None:
                price = int(float(price))

            return status, price, coords

        else:
            price = None
            coords = None
            error = json.loads(req.text)
            status = 'error: ' + error['errors'][0]
            try:
                status += self.get_errors(error)
            except:
                pass
        return status, price, coords

    def calculate_order_price(self, user_info, order_id):
        user_info['delivery_time'] = '12to15'
        user_data = self._creator_getter(user_info, order_id)

        test_header = {TOKEN_KEY: TEST_TOKEN}
        req = requests.post(url=self.calculate_url,
                            json=user_data, headers=test_header)

        status = req.reason
        if status == 'OK':
            order = json.loads(req.text)['order']
            destination = order['points'][-1]

            price = order['payment_amount']
            coords = (destination['longitude'], destination['latitude'])
            return status, int(float(price)), coords

        else:
            price = None
            coords = None
            return status, price, coords

    @staticmethod
    def get_errors(source):
        if 'parameter_errors' in source:
            return source['parameter_errors']
        elif 'parameter_warnings' in source:
            return source['parameter_warnings']
        return None

if __name__ == '__main__':
    DOST = Dostavista()

    t = requests.get(url='https://robot.dostavista.ru/api/business/1.1/deliveries',
        headers=DOST.my_header)

    # USER_INFO = json.loads(input('input json: '))
    # TEST = DOST.create_order(USER_INFO, 89)
    # with open('d.json', 'w') as f:
    #     f.write(TEST)
