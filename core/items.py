import math
import random

from core.errors import InvalidItemPriceError, InvalidItemNameError,\
                         InvalidItemPoolError, DuplicateItemError, NonExistingItemError

class Item:
    def __init__(self, name, price):
        try:
            if type(name) != str or not name:
                raise InvalidItemNameError(name)
            self.name = name
            if not isinstance(price, (float, int)) or not price > 0:
                raise InvalidItemPriceError(price)
            self.price = round(price, 2)
        except InvalidItemNameError(name):
            print(f'Invalid item name: "{name}".')
        except InvalidItemPriceError(price):
            print(f'Could not convert string to float: "{price}".')


    def get_order(self):
        return math.floor(round(math.log(self.price, 10), 10))


    def get_price_str(self, quantity = None, hide_price = False, order = None):
        # price
        if order is None:
            order = self.get_order()
        prcStr = '${:0' + str(order + 4) + '.2f}'
        prcStr = prcStr.format(self.price * (quantity or 1))
        if hide_price:
            prcStr = f'${"?" * (order + 1)}.??'

        return f'{prcStr}'


    def get_list_item_str(self, quantity = None, leading_dash = True):
        # quantity
        if quantity is None:
            qnt_str = ''
        else:
            qnt_str = f' ({quantity}x)'

        # dash
        dash = ''
        if leading_dash:
            dash = '- '
        return f'{dash}{self.name}{qnt_str}'

    
    def __repr__(self):
        return f'Item({self.name}, {self.price})'
    

    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name\
              and self.price == other.price
           

class ItemPool (Item):
    def __init__(self, items = None):
        try:
            if not items:
                items = {}
            if type(items) != dict:
                raise InvalidItemPoolError()
            for key, val in items.items():
                if type(key) != str or type(val) != Item:
                    raise InvalidItemPoolError()
            self.items = items
        except InvalidItemPoolError():
            print(f'Invalid item pool: "{items}".')
        

    def add_item(self, item):
        try:
            if type(item) != Item:
                raise InvalidItemPoolError()
            if item.name in self.items:
                raise DuplicateItemError()
            self.items[item.name] = item
        except InvalidItemPoolError():
            print(f'Invalid item: "{item}".')
        except DuplicateItemError():
            print(f'Duplicate item: "{item}".')


    def remove_item(self, item_name):
        try:
            if item_name not in self.items:
                raise NonExistingItemError(item_name)
            del self.items[item_name]
        except NonExistingItemError(item_name):
            print(f'Non-existing item: "{item_name}".')


    def get_size(self):
        return len(self.items)


    def sample_items(self, sample_size):
        return random.sample(list(self.items.values()),\
                              min(sample_size, len(self.items)))

    
    def __repr__(self):
        return f'ItemPool({self.items})'

    def __eq__(self, other):
        return isinstance(other, ItemPool) and self.items == other.items
