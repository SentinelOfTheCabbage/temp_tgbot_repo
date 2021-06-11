# pylint: disable=C0111
import re


class User:

    def __init__(self, user_id=None, message_id=None, kwargs=None):
        self.basket = []
        self.branches_stack = []

        self.address = None
        self.name = None
        self.phone = None
        self.id = user_id
        self.delivery_price = None
        self.delivery_date = None
        self.delivery_cost = None
        self.delivery_time = None
        self.answer_status = False
        self.last_message = None
        self.comment = None
        self.referal_id = None
        self.pay_by_bonuses = 0
        self.promocode = None
        self.bonuses = None
        self.discount = 1
        self.rating = []

        if kwargs is not None:
            for key in kwargs:
                setattr(self, key, str(kwargs[key]))
                # exec(f'self.{key} = \'{kwargs[key]}\'')

        if ('last_message_content' in kwargs) and ('predef' in kwargs['last_message_content']):
            self.predef_prod = kwargs['last_message_content'][14:]
            self.phase = 1

    def append_basket(self, product):
        product_keys = [i['key'] for i in user.basket]
        if product['key'] in product_keys:
            pos = product_keys.index(product['key'])
            self.basket = self.basket[
                :pos] + self.basket[pos + 1:] + self.basket[pos:pos + 1]
        else:
            self.basket.append(product)

    def get_referal(self):
        return user.promocode
        pass

    def get_phase(self):
        return self.phase

    def __str__(self):
        data = {}
        data['name'] = self.name
        data['phone'] = self.phone
        data['delivery_date'] = self.delivery_date
        data['address'] = self.address
        data['comment'] = self.comment
        data['delivery_time'] = self.delivery_time
        data['delivery_price'] = self.delivery_price
        data['delivery_cost'] = self.delivery_cost
        data['referal_id'] = self.referal_id
        data['id'] = self.id
        data['basket'] = self.basket
        data['discount'] = self.discount
        keys = data.keys()
        result = ''
        for elem in keys:
            if elem != 'basket':
                result += f'{elem}:\t {data[elem]}\n'
            else:
                result += f'\n{elem}:\n'
                for e in data[elem]:
                    name = e['title'][:6] + '...'
                    amount = f"[x{e['amount']}]"
                    price = f"-{e['price']}"
                    result += f'\t{name}{amount}{price}\n'
                result += '\n'

        return result

    def __dict__(self):
        data = {}
        # data['phase'] = self.phase
        data['name'] = self.name
        data['basket'] = self.basket
        data['phone'] = self.phone
        data['delivery_date'] = self.delivery_date
        data['address'] = self.address
        data['delivery_price'] = self.delivery_price
        data['delivery_cost'] = self.delivery_cost
        data['last_message'] = self.last_message
        data['discount'] = self.discount
        data['delivery_time'] = self.delivery_time
        data['referal_id'] = self.referal_id if self.referal_id else 0
        data['id'] = self.id
        data['comment'] = self.comment
        # data['bonuses'] = getattr(self, 'bonuses', 0)
        data['promocode'] = getattr(self, 'promocode', 'null')
        data['pay_by_bonuses'] = getattr(self, 'pay_by_bonuses', 0)
        return data

    def sum_prod_price(self) -> int:
        return sum([product['price'] for product in self.basket])

    def result_price(self) -> int:
        return self.sum_prod_price() * self.getattr('promocode_reducing', 1) - \
            self.getattr('used_bonuses', 0)

    def add_promocode(self, promocode):
        pass

    def is_addr_free(self):
        addr = self.address.lower()
        if re.findall('[Кк]утузовск.*[^0-9]32[^0-9]*[к|корпус|/].*1[^0-9]*', addr):
            return True
        elif re.findall('[Пп]окло[н]{1,2}ая.*3[^0-9]*[к|корпус|/].*[12][^0-9]*', addr):
            return True
        else:
            return False

    def create_by_pattern(self):
        self.phase = 1

    def push_branch(self, branch_key, start_phase):
        self.branches_stack.append(BranchPosition(branch_key, start_phase))

    def pop_branch(self):
        self.branches_stack.pop()

    def get_branch(self):
        return self.branches_stack[-1].get_branch()

    def update_answer_status(self):
        self.answer_status = True

    def update_last_message(self, message):
        self.last_message = message.id

    def set_phase(self, new_value):
        self.branches_stack[-1].phase = new_value

    def get_phase(self):
        return self.branches_stack[-1].get_phase()

    def is_answered(self):
        return self.answer_status


class BranchPosition:

    def __init__(self, branch_key, phase):
        self.branch_key = branch_key
        self.phase = phase

    def get_branch(self):
        return self.branch_key

    def get_phase(self):
        return self.phase

    def get_branch(self):
        return self.branch_key

    def up_phase(self):
        self.phase += 1

    def down_phase(self):
        if self.phase != 0:
            self.phase -= 1

if __name__ == '__main__':
    u = User(123, 123)
    u.append_basket({'price': 500})
    print('Loaded')
